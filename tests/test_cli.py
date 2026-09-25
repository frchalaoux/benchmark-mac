from pathlib import Path

from test_repository import sample_report
from typer.testing import CliRunner

from benchmark_mac.cli import app
from benchmark_mac.repository import JsonReportRepository

runner = CliRunner()


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
