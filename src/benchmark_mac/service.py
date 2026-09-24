"""Orchestration, isolation des échecs et archivage de la suite."""

from __future__ import annotations

import os
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

from . import __version__
from .benchmarks import CATALOG, PROFILES, BenchmarkContext, resolve_benchmarks
from .models import BenchmarkFailure, BenchmarkReport, BenchmarkResult
from .repository import JsonReportRepository
from .system_info import system_snapshot

ProgressCallback = Callable[[str, BenchmarkResult | BenchmarkFailure | None], None]


class BenchmarkService:
    """Exécute une sélection reproductible sans dépendre de la CLI."""

    def __init__(self, repository: JsonReportRepository) -> None:
        self.repository = repository

    def run(
        self,
        names: list[str] | None = None,
        groups: list[str] | None = None,
        *,
        profile_name: str = "standard",
        label: str | None = None,
        work_dir: Path | str = ".",
        workers: int | None = None,
        progress: ProgressCallback | None = None,
    ) -> tuple[BenchmarkReport, Path]:
        """Exécute chaque test demandé et conserve les éventuels échecs isolés."""
        if profile_name not in PROFILES:
            raise ValueError(f"Profil inconnu : {profile_name}")
        selected = resolve_benchmarks(names, groups)
        Path(work_dir).mkdir(parents=True, exist_ok=True)
        context = BenchmarkContext(
            profile=PROFILES[profile_name],
            work_dir=Path(work_dir).resolve(),
            workers=workers or (os.cpu_count() or 1),
        )
        results: list[BenchmarkResult] = []
        failures: list[BenchmarkFailure] = []
        for benchmark_id in selected:
            if progress:
                progress(benchmark_id, None)
            try:
                result = CATALOG[benchmark_id].runner(context)
            # L'isolation est volontaire : un test matériel peut échouer de façon imprévisible.
            except Exception as error:  # noqa: BLE001
                failure = BenchmarkFailure(benchmark_id=benchmark_id, message=str(error))
                failures.append(failure)
                if progress:
                    progress(benchmark_id, failure)
            else:
                results.append(result)
                if progress:
                    progress(benchmark_id, result)
        report = BenchmarkReport(
            suite_version=__version__,
            recorded_at=datetime.now(UTC),
            label=label,
            profile=profile_name,
            requested_benchmarks=selected,
            system=system_snapshot(context.work_dir),
            results=results,
            failures=failures,
        )
        return report, self.repository.save(report)
