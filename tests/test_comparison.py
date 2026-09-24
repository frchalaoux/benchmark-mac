import pytest
from test_repository import sample_report

from benchmark_mac.comparison import (
    SCENARIOS,
    analyze_reports,
    difference_label,
    equivalent_duration,
    parse_scenario_weights,
)
from benchmark_mac.html_report import render_html
from benchmark_mac.models import BenchmarkResult


def result(
    benchmark_id: str,
    group: str,
    value: float,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
) -> BenchmarkResult:
    return BenchmarkResult(
        benchmark_id=benchmark_id,
        group=group,
        name=benchmark_id,
        description="Test",
        value=value,
        unit="unités/s",
        elapsed_seconds=1,
        repetitions=3,
        sample_values=[minimum or value, value, maximum or value],
        minimum=minimum or value,
        maximum=maximum or value,
        relative_spread_percent=(maximum - minimum) / value * 100
        if minimum is not None and maximum is not None
        else 0,
    )


def complete_report(label: str, multiplier: float):
    report = sample_report(label=label)
    results = [
        result(benchmark_id, benchmark_id.split(".", 1)[0], 100 * multiplier)
        for benchmark_id in {
            benchmark_id for weights in SCENARIOS.values() for benchmark_id in weights
        }
    ]
    return report.model_copy(
        update={
            "suite_version": "0.2.0.dev1",
            "repetitions": 3,
            "requested_benchmarks": [item.benchmark_id for item in results],
            "results": results,
        }
    )


def test_parse_scenario_weights_normalizes_user_priorities() -> None:
    weights = parse_scenario_weights(["developpement=50", "creation=30", "quotidien=20"])

    assert weights == {"developpement": 0.5, "creation": 0.3, "quotidien": 0.2}


def test_analysis_translates_ratios_to_indices_and_durations() -> None:
    analysis = analyze_reports(
        [complete_report("Référence", 1), complete_report("Candidate", 1.5)],
        parse_scenario_weights(["developpement=1"]),
    )

    candidate = analysis.machines[1]
    assert candidate.overall_index == pytest.approx(150)
    assert candidate.scenarios["developpement"] == pytest.approx(150)
    assert equivalent_duration(1_800, 150) == 1_200
    assert "+50 %" in candidate.narrative


def test_overlapping_ranges_make_a_difference_inconclusive() -> None:
    baseline = complete_report("Référence", 1)
    candidate = complete_report("Candidate", 1.1)
    baseline_result = result("cpu.integer", "cpu", 100, minimum=95, maximum=110)
    candidate_result = result("cpu.integer", "cpu", 110, minimum=105, maximum=115)
    baseline = baseline.model_copy(update={"results": [baseline_result]})
    candidate = candidate.model_copy(update={"results": [candidate_result]})

    analysis = analyze_reports([baseline, candidate], parse_scenario_weights(["quotidien=1"]))

    assert analysis.machines[1].metrics["cpu.integer"].conclusion == ("différence non concluante")


def test_human_thresholds_cover_all_proposed_levels() -> None:
    assert difference_label(3, inconclusive=False) == "sensiblement équivalent"
    assert "légère" in difference_label(8, inconclusive=False)
    assert "nette" in difference_label(20, inconclusive=False)
    assert "importante" in difference_label(40, inconclusive=False)
    assert "changement de catégorie" in difference_label(70, inconclusive=False)


def test_comparison_rejects_different_benchmark_parameters() -> None:
    baseline = complete_report("Référence", 1)
    candidate = complete_report("Candidate", 1.2)
    changed = candidate.results[0].model_copy(update={"parameters": {"size": 42}})
    candidate = candidate.model_copy(update={"results": [changed, *candidate.results[1:]]})

    with pytest.raises(ValueError, match="Paramètres incohérents"):
        analyze_reports([baseline, candidate], parse_scenario_weights(None))


def test_html_report_is_autonomous_and_contains_all_visual_sections() -> None:
    analysis = analyze_reports(
        [complete_report("Référence", 1), complete_report("Candidate", 1.25)],
        parse_scenario_weights(None),
    )

    document = render_html(analysis)

    assert "Scénarios d'usage" in document
    assert "Catégories techniques" in document
    assert "Carte thermique" in document
    assert "Temps équivalents" in document
    assert "class='dumbbell'" in document
    assert "https://" not in document


def test_heatmap_supports_more_than_two_machines() -> None:
    analysis = analyze_reports(
        [
            complete_report("Référence", 1),
            complete_report("Machine B", 1.25),
            complete_report("Machine C", 0.8),
        ],
        parse_scenario_weights(None),
    )

    document = render_html(analysis)

    assert "Machine B" in document
    assert "Machine C" in document
    assert "class='dumbbell'" not in document
