"""Construction sûre et déterministe des rapports destinés au catalogue public."""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

from .benchmarks import CATALOG, PROFILES
from .comparison import report_protocol
from .models import (
    BenchmarkReport,
    PublicBenchmarkReport,
    PublicBenchmarkResult,
    PublicSystemSnapshot,
)

PUBLIC_FORMAT_VERSION = 1
PUBLIC_LICENSE = "CC0-1.0"
SUPPORTED_PRIVATE_SCHEMA = 4
SUPPORTED_PROTOCOL = "0.3.0"
SUITE_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:\.dev\d+)?$")
PRIVATE_PATH_PATTERNS = (
    re.compile(r"/(?:Users|home)/[^/]+(?:/|$)", re.IGNORECASE),
    re.compile(r"[A-Z]:\\Users\\[^\\]+(?:\\|$)", re.IGNORECASE),
)
PUBLIC_RESULT_UNITS = {
    "application.json": "cycles/s",
    "application.sqlite": "lignes/s",
    "cpu.compression": "Mio/s",
    "cpu.float": "Mop/s",
    "cpu.hash": "Mio/s",
    "cpu.integer": "Mop/s",
    "cpu.multicore": "Mop/s",
    "gpu.compute-fp32": "GFLOP/s",
    "gpu.image-filter": "Mpixel/s",
    "gpu.memory": "Gio/s",
    "gpu.raster": "Mpixel/s",
    "memory.copy": "Mio/s",
    "storage.random-read": "IOPS",
    "storage.random-write": "IOPS",
    "storage.read": "Mio/s",
    "storage.write": "Mio/s",
}
PUBLIC_PARAMETERS_BY_BENCHMARK = {
    "application.json": frozenset({"document_size_bytes"}),
    "application.sqlite": frozenset({"rows"}),
    "cpu.compression": frozenset({"block_size_bytes", "compression_level"}),
    "cpu.float": frozenset({"workers"}),
    "cpu.hash": frozenset({"block_size_bytes"}),
    "cpu.integer": frozenset({"workers"}),
    "cpu.multicore": frozenset({"workers"}),
    "gpu.compute-fp32": frozenset(
        {
            "element_count",
            "gpu_adapter_type",
            "gpu_backend",
            "gpu_device",
            "gpu_index",
            "operations_per_element",
            "wgpu_version",
        }
    ),
    "gpu.image-filter": frozenset(
        {
            "gpu_adapter_type",
            "gpu_backend",
            "gpu_device",
            "gpu_index",
            "height",
            "samples_per_pixel",
            "wgpu_version",
            "width",
        }
    ),
    "gpu.memory": frozenset(
        {
            "buffer_size_bytes",
            "bytes_counted_per_element",
            "gpu_adapter_type",
            "gpu_backend",
            "gpu_device",
            "gpu_index",
            "wgpu_version",
        }
    ),
    "gpu.raster": frozenset(
        {
            "color_format",
            "gpu_adapter_type",
            "gpu_backend",
            "gpu_device",
            "gpu_index",
            "height",
            "wgpu_version",
            "width",
        }
    ),
    "memory.copy": frozenset({"buffer_size_bytes"}),
    "storage.random-read": frozenset({"block_size_bytes", "operations"}),
    "storage.random-write": frozenset({"block_size_bytes", "operations"}),
    "storage.read": frozenset({"file_size_bytes"}),
    "storage.write": frozenset({"file_size_bytes"}),
}


def _clean_public_text(value: str, *, field: str, maximum: int = 200) -> str:
    """Refuse les chaînes ambiguës plutôt que de publier une valeur inattendue."""
    normalized = " ".join(value.split())
    if not normalized or len(normalized) > maximum:
        raise ValueError(f"Valeur publique invalide pour {field}.")
    if any(character in normalized for character in ("\x00", "\r", "\n")):
        raise ValueError(f"Valeur publique invalide pour {field}.")
    if any(pattern.search(normalized) for pattern in PRIVATE_PATH_PATTERNS):
        raise ValueError(f"Chemin privé détecté dans {field}.")
    return normalized


def _public_result(report_result) -> PublicBenchmarkResult:
    definition = CATALOG.get(report_result.benchmark_id)
    if definition is None:
        raise ValueError(f"Benchmark inconnu : {report_result.benchmark_id}")
    if report_result.group != definition.group:
        raise ValueError(f"Groupe incohérent pour {report_result.benchmark_id}.")
    if report_result.unit != PUBLIC_RESULT_UNITS[report_result.benchmark_id]:
        raise ValueError(f"Unité incohérente pour {report_result.benchmark_id}.")
    if not report_result.higher_is_better:
        raise ValueError(f"Sens de mesure incohérent pour {report_result.benchmark_id}.")
    expected_parameters = PUBLIC_PARAMETERS_BY_BENCHMARK[report_result.benchmark_id]
    if set(report_result.parameters) != expected_parameters:
        raise ValueError(f"Paramètres incohérents pour {report_result.benchmark_id}.")
    parameters: dict[str, int | float | str] = {}
    for name, value in sorted(report_result.parameters.items()):
        clean_name = _clean_public_text(name, field="parameters", maximum=80)
        if isinstance(value, int | float) and not math.isfinite(value):
            raise ValueError(f"Paramètre non fini pour {report_result.benchmark_id}.")
        parameters[clean_name] = (
            _clean_public_text(value, field=f"parameters.{clean_name}")
            if isinstance(value, str)
            else value
        )
    return PublicBenchmarkResult(
        benchmark_id=definition.benchmark_id,
        group=definition.group,
        name=definition.name,
        value=report_result.value,
        unit=_clean_public_text(report_result.unit, field="unit", maximum=40),
        higher_is_better=report_result.higher_is_better,
        parameters=parameters,
        repetitions=report_result.repetitions,
        sample_values=report_result.sample_values,
        minimum=report_result.minimum,
        maximum=report_result.maximum,
        relative_spread_percent=report_result.relative_spread_percent,
    )


def _content_id(payload: dict[str, object]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return f"sha256:{hashlib.sha256(canonical).hexdigest()}"


def export_public_report(report: BenchmarkReport) -> PublicBenchmarkReport:
    """Reconstruit un rapport public depuis une liste blanche de champs."""
    if report.schema_version != SUPPORTED_PRIVATE_SCHEMA:
        raise ValueError(
            f"Le schéma privé {report.schema_version} ne peut pas être exporté sûrement."
        )
    protocol = report_protocol(report)
    if protocol != SUPPORTED_PROTOCOL:
        raise ValueError(f"Le protocole {protocol} ne peut pas être exporté sûrement.")
    if not report.results:
        raise ValueError("Un rapport sans résultat ne peut pas être exporté.")
    if not SUITE_VERSION_PATTERN.fullmatch(report.suite_version):
        raise ValueError("La version de la suite n'est pas reconnue.")
    if report.profile not in PROFILES:
        raise ValueError(f"Profil inconnu : {report.profile}")

    result_ids = [result.benchmark_id for result in report.results]
    if len(result_ids) != len(set(result_ids)):
        raise ValueError("Le rapport contient des résultats dupliqués.")
    unknown_requests = set(report.requested_benchmarks) - set(CATALOG)
    if unknown_requests:
        raise ValueError("Le rapport demande au moins un benchmark inconnu.")

    public_system = PublicSystemSnapshot(
        operating_system=_clean_public_text(report.system.system, field="operating_system"),
        architecture=_clean_public_text(report.system.machine, field="architecture"),
        processor=_clean_public_text(report.system.processor, field="processor"),
        physical_cpu_count=report.system.physical_cpu_count,
        logical_cpu_count=report.system.logical_cpu_count,
        memory_bytes=report.system.memory_bytes,
        gpu_devices=[
            _clean_public_text(device, field="gpu_devices") for device in report.system.gpu_devices
        ],
        python_version=_clean_public_text(report.system.python_version, field="python_version"),
        python_implementation=_clean_public_text(
            report.system.python_implementation,
            field="python_implementation",
        ),
    )
    public_results = [_public_result(result) for result in report.results]
    failed = sorted({failure.benchmark_id for failure in report.failures})
    if any(benchmark_id not in CATALOG for benchmark_id in failed):
        raise ValueError("Le rapport contient l'échec d'un benchmark inconnu.")
    requested = set(report.requested_benchmarks)
    if set(result_ids) & set(failed) or set(result_ids) | set(failed) != requested:
        raise ValueError("Résultats et échecs incohérents avec les benchmarks demandés.")
    if any(result.repetitions != report.repetitions for result in report.results):
        raise ValueError("Nombre de passages incohérent dans les résultats.")

    content: dict[str, object] = {
        "format": "perfcomparator-public-report",
        "format_version": PUBLIC_FORMAT_VERSION,
        "license": PUBLIC_LICENSE,
        "verification": "community-unverified",
        "source_schema_version": report.schema_version,
        "suite_version": report.suite_version,
        "protocol_version": protocol,
        "profile": report.profile,
        "repetitions": report.repetitions,
        "requested_benchmarks": report.requested_benchmarks,
        "system": public_system.model_dump(mode="json"),
        "readiness_suitable": report.readiness.suitable if report.readiness else None,
        "results": [result.model_dump(mode="json") for result in public_results],
        "failed_benchmarks": failed,
    }
    return PublicBenchmarkReport(report_id=_content_id(content), **content)


def save_public_report(report: PublicBenchmarkReport, path: Path | str) -> Path:
    """Écrit atomiquement un rapport public avec un ordre de champs stable."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    payload = json.dumps(
        report.model_dump(mode="json"),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )
    temporary.write_text(payload + "\n", encoding="utf-8")
    temporary.replace(destination)
    return destination
