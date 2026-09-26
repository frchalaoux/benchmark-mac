from pathlib import Path

from test_repository import sample_report
from typer.testing import CliRunner

from benchmark_mac import __version__
from benchmark_mac.cli import app
from benchmark_mac.repository import JsonReportRepository

runner = CliRunner()


def test_version_option_displays_installed_version() -> None:
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert result.stdout.strip() == f"benchmark-mac {__version__}"


def test_list_displays_groups_profiles_and_individual_benchmarks() -> None:
    result = runner.invoke(app, ["list"])

    assert result.exit_code == 0
    assert "GROUPES" in result.stdout
    assert "thorough" in result.stdout
    assert "cpu.integer" in result.stdout
    assert "storage.random-write" in result.stdout
    assert "gpu.compute-fp32" in result.stdout
    assert "gpu.raster" in result.stdout


def test_history_is_empty_in_an_isolated_directory(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["history"])

    assert result.exit_code == 0
    assert "Aucun benchmark archivé" in result.stdout


def test_describe_displays_method_limits_and_references() -> None:
    result = runner.invoke(app, ["describe", "cpu.hash"])

    assert result.exit_code == 0
    assert "Méthode" in result.stdout
    assert "Limites" in result.stdout
    assert "FIPS PUB 180-4" in result.stdout


def test_compare_uses_first_report_as_baseline(tmp_path: Path) -> None:
    first = JsonReportRepository(tmp_path / "first").save(sample_report())
    second = JsonReportRepository(tmp_path / "second").save(
        sample_report(value=15, label="PC test")
    )

    result = runner.invoke(app, ["compare", str(first), str(second)])

    assert result.exit_code == 0
    assert "Mac test" in result.stdout
    assert "PC test" in result.stdout
    assert "+50.0 %" in result.stdout


def test_compare_displays_a_conclusion_for_each_candidate(tmp_path: Path) -> None:
    baseline = JsonReportRepository(tmp_path / "baseline").save(sample_report())
    faster = JsonReportRepository(tmp_path / "faster").save(
        sample_report(value=15, label="PC rapide")
    )
    slower = JsonReportRepository(tmp_path / "slower").save(sample_report(value=8, label="PC lent"))

    result = runner.invoke(app, ["compare", str(baseline), str(faster), str(slower)])

    assert result.exit_code == 0
    assert "Mac test 100 (référence)" in result.stdout
    assert "PC rapide 150 (+50.0 % ; différence importante en faveur de cette machine)" in (
        result.stdout
    )
    assert "PC lent 80 (-20.0 % ; différence nette en sa défaveur)" in result.stdout


def test_compare_writes_a_weighted_autonomous_html_report(tmp_path: Path) -> None:
    first = JsonReportRepository(tmp_path / "first").save(sample_report())
    second = JsonReportRepository(tmp_path / "second").save(
        sample_report(value=12, label="PC test")
    )
    output = tmp_path / "comparaison.html"

    result = runner.invoke(
        app,
        [
            "compare",
            str(first),
            str(second),
            "--weight",
            "quotidien=1",
            "--html",
            str(output),
        ],
    )

    assert result.exit_code == 0
    assert "Rapport HTML" in result.stdout
    assert output.exists()
    assert "Carte thermique" in output.read_text(encoding="utf-8")
