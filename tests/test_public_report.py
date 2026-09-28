import json

import pytest
from test_repository import sample_report

from benchmark_mac.models import BenchmarkFailure, ProcessLoad, ReadinessSnapshot
from benchmark_mac.public_report import (
    export_public_report,
    load_public_report,
    public_report_to_benchmark_report,
    save_public_report,
)


def exportable_report():
    report = sample_report(label="Secret machine label").model_copy(
        update={
            "suite_version": "0.4.0.dev0",
            "protocol_version": "0.3.0",
            "requested_benchmarks": ["cpu.integer", "cpu.float"],
            "readiness": ReadinessSnapshot(
                sample_seconds=1,
                cpu_percent=20,
                memory_available_percent=50,
                memory_available_bytes=1_000,
                swap_percent=0,
                active_processes=[
                    ProcessLoad(
                        pid=4242,
                        name="private-process-name",
                        cpu_percent=20,
                        memory_percent=5,
                    )
                ],
                warnings=["private-process-name est actif dans /Users/alice/private"],
                suitable=False,
            ),
            "environment_warnings": ["Secret environment warning"],
            "failures": [
                BenchmarkFailure(
                    benchmark_id="cpu.float",
                    message="Failure in /Users/alice/private with PID 4242",
                )
            ],
        }
    )
    report.system.python_executable = "/Users/alice/private/.venv/bin/python"
    report.system.version = "private system version"
    report.system.release = "private release"
    report.results[0].parameters = {"workers": 1}
    report.results[0].sample_values = [10]
    report.results[0].minimum = 10
    report.results[0].maximum = 10
    report.results[0].relative_spread_percent = 0
    return report


def test_public_export_uses_a_strict_allowlist_and_hides_sensitive_values() -> None:
    exported = export_public_report(exportable_report())
    payload = exported.model_dump_json()

    assert "Secret machine label" not in payload
    assert "/Users/alice/private" not in payload
    assert "4242" not in payload
    assert "private-process-name" not in payload
    assert "Secret environment warning" not in payload
    assert "private system version" not in payload
    assert "private release" not in payload
    assert exported.failed_benchmarks == ["cpu.float"]
    assert exported.readiness_suitable is False


def test_public_export_is_deterministic(tmp_path) -> None:
    first = export_public_report(exportable_report())
    second = export_public_report(exportable_report())
    first_path = save_public_report(first, tmp_path / "first.json")
    second_path = save_public_report(second, tmp_path / "second.json")

    assert first.report_id == second.report_id
    assert first_path.read_bytes() == second_path.read_bytes()


def test_public_export_supports_schema_3_without_readiness_data() -> None:
    report = exportable_report().model_copy(update={"schema_version": 3, "readiness": None})

    exported = export_public_report(report)

    assert exported.source_schema_version == 3
    assert exported.readiness_suitable is None


def test_report_id_changes_with_comparative_content() -> None:
    first = export_public_report(exportable_report())
    changed = exportable_report()
    changed.results[0].value = 12
    changed.results[0].sample_values = [12]
    changed.results[0].minimum = 12
    changed.results[0].maximum = 12

    assert export_public_report(changed).report_id != first.report_id


def test_public_schema_rejects_unknown_fields() -> None:
    exported = export_public_report(exportable_report())
    payload = exported.model_dump(mode="json")
    payload["label"] = "must not be accepted"

    with pytest.raises(ValueError, match="Extra inputs are not permitted"):
        type(exported).model_validate(payload)


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"schema_version": 2}, "schéma privé 2"),
        ({"protocol_version": "0.2.0"}, "protocole 0.2.0"),
        ({"results": []}, "sans résultat"),
    ],
)
def test_public_export_rejects_unsupported_or_incomplete_reports(changes, message) -> None:
    report = exportable_report().model_copy(update=changes)

    with pytest.raises(ValueError, match=message):
        export_public_report(report)


def test_public_export_rejects_an_unknown_parameter() -> None:
    report = exportable_report()
    report.results[0].parameters = {"private_path": "/Users/alice/private"}

    with pytest.raises(ValueError, match="Paramètres incohérents"):
        export_public_report(report)


def test_public_export_rejects_a_private_path_in_allowed_text() -> None:
    report = exportable_report()
    report.system.processor = "CPU observed in /home/alice/private/file"

    with pytest.raises(ValueError, match="Chemin privé détecté"):
        export_public_report(report)


@pytest.mark.parametrize("operating_system", ["Darwin", "Linux", "Windows"])
def test_public_export_supports_each_target_operating_system(operating_system) -> None:
    report = exportable_report()
    report.system.system = operating_system

    assert export_public_report(report).system.operating_system == operating_system


def test_saved_public_report_is_valid_json(tmp_path) -> None:
    path = save_public_report(export_public_report(exportable_report()), tmp_path / "public.json")

    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["format"] == "perfcomparator-public-report"
    assert payload["license"] == "CC0-1.0"
    assert payload["verification"] == "community-unverified"


def test_saved_public_report_can_be_loaded_and_fully_validated(tmp_path) -> None:
    exported = export_public_report(exportable_report())
    path = save_public_report(exported, tmp_path / "public.json")

    assert load_public_report(path) == exported


def test_public_report_can_be_adapted_without_reintroducing_private_data() -> None:
    exported = export_public_report(exportable_report())

    comparable = public_report_to_benchmark_report(exported)

    assert comparable.label == "Apple M4"
    assert comparable.protocol_version == "0.3.0"
    assert comparable.results[0].value == 10
    assert comparable.results[0].parameters == {"workers": 1}
    assert comparable.failures[0].message == "Échec déclaré dans le rapport public."
    assert "Secret machine label" not in comparable.model_dump_json()
    assert "/Users/alice/private" not in comparable.model_dump_json()


def test_public_validation_rejects_tampered_content(tmp_path) -> None:
    exported = export_public_report(exportable_report())
    path = save_public_report(exported, tmp_path / "public.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["results"][0]["value"] = 999
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="Médiane incohérente"):
        load_public_report(path)


def test_public_validation_rejects_a_wrong_content_id(tmp_path) -> None:
    exported = export_public_report(exportable_report())
    path = save_public_report(exported, tmp_path / "public.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["report_id"] = f"sha256:{'0' * 64}"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="identifiant ne correspond pas"):
        load_public_report(path)


def test_public_validation_rejects_oversized_files(tmp_path) -> None:
    path = tmp_path / "public.json"
    path.write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match="dépasse la limite"):
        load_public_report(path, maximum_bytes=1)
