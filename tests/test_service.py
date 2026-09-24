from test_repository import sample_report

from benchmark_mac import benchmarks as benchmark_module
from benchmark_mac.benchmarks import BenchmarkDefinition
from benchmark_mac.models import BenchmarkResult, EnvironmentSnapshot
from benchmark_mac.repository import JsonReportRepository
from benchmark_mac.service import BenchmarkService, _environment_warnings


def test_service_aggregates_repetitions_with_the_median(tmp_path, monkeypatch) -> None:
    values = iter([10.0, 30.0, 20.0])

    def fake_runner(_context):
        return BenchmarkResult(
            benchmark_id="test.fake",
            group="test",
            name="Test",
            description="Test",
            value=next(values),
            unit="unités/s",
            elapsed_seconds=0.1,
        )

    definition = BenchmarkDefinition("test.fake", "test", "Test", "Test", fake_runner)
    monkeypatch.setitem(benchmark_module.CATALOG, "test.fake", definition)
    monkeypatch.setattr(
        "benchmark_mac.service.system_snapshot", lambda _path: sample_report().system
    )

    report, _ = BenchmarkService(JsonReportRepository(tmp_path / "results")).run(
        names=["test.fake"],
        profile_name="quick",
        work_dir=tmp_path,
        repetitions=3,
    )

    measured = report.results[0]
    assert measured.value == 20
    assert measured.minimum == 10
    assert measured.maximum == 30
    assert measured.relative_spread_percent == 100
    assert measured.sample_values == [10, 30, 20]
    assert report.repetitions == 3


def test_environment_warnings_detect_battery_thermal_limit_and_temperature() -> None:
    warnings = _environment_warnings(
        EnvironmentSnapshot(
            power_source="Battery Power",
            thermal_limit_percent=100,
            temperature_celsius=60,
        ),
        EnvironmentSnapshot(
            power_source="Battery Power",
            thermal_limit_percent=80,
            temperature_celsius=86,
        ),
    )

    assert any("batterie" in warning for warning in warnings)
    assert any("80 %" in warning for warning in warnings)
    assert any("26.0 °C" in warning for warning in warnings)
    assert any("86.0 °C" in warning for warning in warnings)
