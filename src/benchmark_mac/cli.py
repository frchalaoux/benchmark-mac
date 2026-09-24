"""Interface en ligne de commande de benchmark-mac."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from .benchmarks import (
    BENCHMARK_DOCUMENTATION,
    CATALOG,
    DEFINITIONS,
    GROUPS,
    PROFILES,
    REFERENCE_LIBRARY,
)
from .models import BenchmarkFailure, BenchmarkResult
from .repository import JsonReportRepository
from .service import BenchmarkService
from .system_info import system_snapshot

app = typer.Typer(
    no_args_is_help=True,
    help="Suite de benchmarks locale pour macOS, Windows et Linux.",
)


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
        typer.secho(f" {outcome.value:.2f} {outcome.unit}", fg=typer.colors.GREEN)


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
) -> None:
    """Exécute toute la suite, un ou plusieurs groupes, ou des tests nommés."""
    try:
        report, path = service().run(
            benchmarks,
            groups,
            profile_name=profile,
            label=label,
            work_dir=work_dir,
            progress=_progress,
        )
    except ValueError as error:
        typer.secho(f"Erreur : {error}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from error
    typer.secho(
        f"\n{len(report.results)} benchmark(s) terminé(s), {len(report.failures)} échec(s).",
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
            f"{report.profile} · {len(report.results)} résultats"
        )


@app.command("compare")
def compare(
    reports: Annotated[list[Path], typer.Argument(exists=True, readable=True)],
) -> None:
    """Compare des rapports JSON ; le premier sert de référence."""
    if len(reports) < 2:
        raise typer.BadParameter("Indiquez au moins deux rapports.")
    loaded = [JsonReportRepository.load_path(path) for path in reports]
    reference = loaded[0]
    for report in loaded[1:]:
        if report.suite_version != reference.suite_version:
            raise typer.BadParameter("Les rapports doivent utiliser la même version de la suite.")
        if report.profile != reference.profile:
            raise typer.BadParameter("Les rapports doivent utiliser le même profil.")
        if report.system.python_version != reference.system.python_version:
            raise typer.BadParameter("Les rapports doivent utiliser la même version de Python.")
    result_maps = [{result.benchmark_id: result for result in report.results} for report in loaded]
    common = set(result_maps[0]).intersection(*(set(results) for results in result_maps[1:]))
    labels = [report.label or report.system.model for report in loaded]
    typer.echo("Benchmark | " + " | ".join(labels))
    typer.echo("-" * min(120, 14 + sum(len(label) + 3 for label in labels)))
    for benchmark_id in sorted(common):
        baseline = result_maps[0][benchmark_id].value
        values = []
        for result_map in result_maps:
            result = result_map[benchmark_id]
            difference = (result.value / baseline - 1) * 100
            values.append(f"{result.value:.2f} {result.unit} ({difference:+.1f} %)")
        typer.echo(f"{benchmark_id} | " + " | ".join(values))


if __name__ == "__main__":
    app()
