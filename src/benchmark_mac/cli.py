"""Interface en ligne de commande de benchmark-mac."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from . import __version__
from .benchmarks import (
    BENCHMARK_DOCUMENTATION,
    CATALOG,
    DEFINITIONS,
    GROUPS,
    PROFILES,
    REFERENCE_LIBRARY,
    resolve_benchmarks,
)
from .comparison import (
    CATEGORY_LABELS,
    SCENARIO_LABELS,
    analyze_reports,
    parse_scenario_weights,
)
from .gpu_benchmarks import gpu_adapters, selected_gpu_adapter
from .html_report import render_html
from .models import BenchmarkFailure, BenchmarkResult, ReadinessSnapshot
from .repository import JsonReportRepository
from .service import BenchmarkService
from .system_info import machine_readiness, system_snapshot

app = typer.Typer(
    no_args_is_help=True,
    help="Suite de benchmarks locale pour macOS, Windows et Linux.",
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"benchmark-mac {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            callback=_version_callback,
            is_eager=True,
            help="Affiche la version installée et quitte.",
        ),
    ] = False,
) -> None:
    """Suite de benchmarks locale pour macOS, Windows et Linux."""


def service(root: Path = Path("data/results")) -> BenchmarkService:
    return BenchmarkService(JsonReportRepository(root))


def _size(value: int | None) -> str:
    return "inconnue" if value is None else f"{value / 1_073_741_824:.1f} Gio"


@app.command("info")
def info() -> None:
    """Affiche le matériel et l'environnement qui accompagneront les scores."""
    snapshot = system_snapshot()
    typer.echo(f"Modèle : {snapshot.model}")
    typer.echo(f"Système : {snapshot.system} {snapshot.release} ({snapshot.machine})")
    typer.echo(f"Processeur : {snapshot.processor}")
    typer.echo(
        f"CPU : {snapshot.physical_cpu_count or '?'} cœurs physiques, "
        f"{snapshot.logical_cpu_count} logiques"
    )
    typer.echo(f"Mémoire : {_size(snapshot.memory_bytes)}")
    typer.echo(f"GPU : {', '.join(snapshot.gpu_devices) or 'inconnu'}")
    try:
        adapters = gpu_adapters()
    except Exception as error:  # noqa: BLE001 - le diagnostic doit rester utilisable
        typer.echo(f"Adaptateurs WebGPU : indisponibles ({error})")
    else:
        typer.echo("Adaptateurs WebGPU utilisables :")
        for adapter in adapters:
            typer.echo(
                f"  [{adapter.index}] {adapter.device} · {adapter.adapter_type} · {adapter.backend}"
            )
    typer.echo(f"Python : {snapshot.python_implementation} {snapshot.python_version}")


@app.command("list")
def list_benchmarks() -> None:
    """Liste les groupes, les profils et les identifiants exécutables."""
    typer.secho("GROUPES", bold=True)
    for group, benchmark_ids in GROUPS.items():
        typer.echo(f"  {group:<12} {', '.join(benchmark_ids)}")
    typer.secho("\nPROFILS", bold=True)
    for profile in PROFILES.values():
        typer.echo(f"  {profile.name:<12} durée de base {profile.duration_seconds:g} s")
    typer.secho("\nBENCHMARKS", bold=True)
    for definition in DEFINITIONS:
        typer.echo(f"  {definition.benchmark_id:<24} {definition.name} — {definition.description}")
    typer.echo("\nDétail : benchmark-mac describe IDENTIFIANT")


@app.command("describe")
def describe(benchmark_id: str) -> None:
    """Décrit précisément le protocole, ses limites et ses références."""
    if benchmark_id not in CATALOG:
        raise typer.BadParameter(f"Benchmark inconnu : {benchmark_id}")
    definition = CATALOG[benchmark_id]
    documentation = BENCHMARK_DOCUMENTATION[benchmark_id]
    typer.secho(f"{definition.name} ({benchmark_id})", bold=True)
    typer.echo(f"Groupe : {definition.group}")
    typer.echo(f"Objectif : {definition.description}")
    typer.echo(f"Méthode : {documentation.methodology}")
    typer.echo(f"Limites : {documentation.limitations}")
    typer.echo("Références :")
    for reference_id in documentation.reference_ids:
        typer.echo(f"  - {REFERENCE_LIBRARY[reference_id]}")


def _progress(benchmark_id: str, outcome: BenchmarkResult | BenchmarkFailure | None) -> None:
    if outcome is None:
        typer.echo(f"{benchmark_id}...", nl=False)
    elif isinstance(outcome, BenchmarkFailure):
        typer.secho(f" échec ({outcome.message})", fg=typer.colors.RED)
    else:
        spread = outcome.relative_spread_percent or 0
        typer.secho(
            f" {outcome.value:.2f} {outcome.unit} · médiane de {outcome.repetitions} "
            f"· dispersion {spread:.1f} %",
            fg=typer.colors.GREEN,
        )


def _show_readiness(snapshot: ReadinessSnapshot) -> None:
    typer.secho("CONTRÔLE AVANT MESURE", bold=True)
    typer.echo(
        f"  CPU utilisé : {snapshot.cpu_percent:.1f} % · mémoire disponible : "
        f"{snapshot.memory_available_percent:.1f} % · échange : {snapshot.swap_percent:.1f} %"
    )
    for process in snapshot.active_processes[:5]:
        typer.echo(
            f"  processus : {process.name} (PID {process.pid}) · CPU "
            f"{process.cpu_percent:.1f} % · mémoire {process.memory_percent:.1f} %"
        )
    if snapshot.suitable:
        typer.secho(
            "  État de départ satisfaisant selon ce contrôle ponctuel.\n",
            fg=typer.colors.GREEN,
        )
    else:
        for warning in snapshot.warnings:
            typer.secho(f"  Attention : {warning}", fg=typer.colors.YELLOW)
        typer.echo(
            "  Les mesures vont continuer, mais elles peuvent sous-estimer les performances "
            "atteignables au repos.\n"
        )


@app.command("run")
def run(
    benchmarks: Annotated[
        list[str] | None,
        typer.Argument(help="Identifiants individuels, par exemple cpu.integer memory.copy."),
    ] = None,
    groups: Annotated[
        list[str] | None,
        typer.Option("--group", "-g", help="Groupe à exécuter ; option répétable."),
    ] = None,
    profile: Annotated[
        str,
        typer.Option("--profile", "-p", help="Profil quick, standard ou thorough."),
    ] = "standard",
    label: Annotated[
        str | None,
        typer.Option(help="Nom libre de la machine ou de la configuration testée."),
    ] = None,
    work_dir: Annotated[
        Path,
        typer.Option(help="Disque et répertoire temporaire à tester."),
    ] = Path("."),
    repeat: Annotated[
        int,
        typer.Option("--repeat", "-r", min=1, max=9, help="Nombre de passages par test."),
    ] = 3,
    gpu: Annotated[
        int | None,
        typer.Option(
            "--gpu",
            min=0,
            help="Indice de l'adaptateur WebGPU affiché par `benchmark-mac info`.",
        ),
    ] = None,
) -> None:
    """Exécute toute la suite, un ou plusieurs groupes, ou des tests nommés."""
    try:
        selected = resolve_benchmarks(benchmarks, groups)
        if any(benchmark_id.startswith("gpu.") for benchmark_id in selected):
            adapter = selected_gpu_adapter(gpu)
            mode = "sélection automatique" if gpu is None else f"indice {gpu}"
            typer.echo(
                f"GPU mesuré ({mode}) : [{adapter.index}] {adapter.device} · "
                f"{adapter.adapter_type} · {adapter.backend}\n"
            )
            if adapter.adapter_type.casefold() == "cpu":
                typer.secho(
                    "Attention : cet adaptateur est un moteur de rendu logiciel exécuté "
                    "par le CPU. Les benchmarks GPU seront refusés, mais les autres "
                    "groupes continueront.\n",
                    fg=typer.colors.YELLOW,
                )
        readiness = machine_readiness()
        _show_readiness(readiness)
        report, path = service().run(
            benchmarks,
            groups,
            profile_name=profile,
            label=label,
            work_dir=work_dir,
            gpu_index=gpu,
            repetitions=repeat,
            readiness=readiness,
            progress=_progress,
        )
    except ValueError as error:
        typer.secho(f"Erreur : {error}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from error
    typer.secho(
        f"\n{len(report.results)} benchmark(s) terminé(s), {len(report.failures)} échec(s), "
        f"{report.repetitions} passage(s).",
        bold=True,
    )
    typer.echo(f"Rapport : {path}")


@app.command("history")
def history(
    limit: Annotated[int, typer.Option(min=1, max=100, help="Nombre maximal de rapports.")] = 10,
) -> None:
    """Liste les derniers rapports archivés."""
    reports = JsonReportRepository().reports()[:limit]
    if not reports:
        typer.echo("Aucun benchmark archivé.")
        return
    for report in reports:
        label = report.label or report.system.model
        typer.echo(
            f"{report.recorded_at.astimezone():%Y-%m-%d %H:%M:%S} · {label} · "
            f"{report.profile} · {report.repetitions} passages · {len(report.results)} résultats"
        )


@app.command("compare")
def compare(
    reports: Annotated[list[Path], typer.Argument(exists=True, readable=True)],
    html: Annotated[
        Path | None,
        typer.Option(help="Produit un rapport HTML autonome à ce chemin."),
    ] = None,
    weight: Annotated[
        list[str] | None,
        typer.Option(
            "--weight",
            "-w",
            help="Pondération scenario=nombre ; option répétable.",
        ),
    ] = None,
) -> None:
    """Compare humainement des rapports ; le premier sert de référence 100."""
    try:
        loaded = [JsonReportRepository.load_path(path) for path in reports]
        weights = parse_scenario_weights(weight)
        analysis = analyze_reports(loaded, weights)
    except (OSError, ValueError) as error:
        raise typer.BadParameter(str(error)) from error

    typer.secho(f"RÉFÉRENCE : {analysis.baseline_label} = 100", bold=True)
    typer.echo("\nINDICE GLOBAL PERSONNALISÉ")
    for machine in analysis.machines:
        typer.echo(f"  {machine.label:<28} {machine.overall_index:7.1f}")
    typer.echo("\nCATÉGORIES TECHNIQUES")
    for category in analysis.machines[0].categories:
        values = " · ".join(
            f"{machine.label} {machine.categories[category]:.0f}" for machine in analysis.machines
        )
        typer.echo(f"  {CATEGORY_LABELS.get(category, category)} : {values}")
    typer.echo("\nSCÉNARIOS")
    for scenario in analysis.scenario_weights:
        values = " · ".join(
            f"{machine.label} {machine.scenarios[scenario]:.0f}" for machine in analysis.machines
        )
        typer.echo(f"  {SCENARIO_LABELS[scenario]} : {values}")
    typer.echo("\nLECTURE")
    for machine in analysis.machines[1:]:
        typer.echo(f"  {machine.narrative}")
    typer.echo("\nDÉTAIL DES BENCHMARKS")
    for benchmark_id in analysis.common_benchmarks:
        values = [f"{analysis.machines[0].label} 100 (référence)"]
        for machine in analysis.machines[1:]:
            metric = machine.metrics[benchmark_id]
            values.append(
                f"{machine.label} {metric.index:.0f} "
                f"({metric.difference_percent:+.1f} % ; {metric.conclusion})"
            )
        typer.echo(f"  {benchmark_id} : {' · '.join(values)}")
    for warning in analysis.warnings:
        typer.secho(f"Attention : {warning}", fg=typer.colors.YELLOW)
    if html is not None:
        html.parent.mkdir(parents=True, exist_ok=True)
        html.write_text(render_html(analysis), encoding="utf-8")
        typer.secho(f"Rapport HTML : {html}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
