"""Archivage JSON atomique des résultats de benchmark."""

from __future__ import annotations

import json
from pathlib import Path

from .models import BenchmarkReport


class JsonReportRepository:
    """Persiste et relit les rapports sous forme de fichiers indépendants."""

    def __init__(self, root: Path | str = "data/results") -> None:
        self.root = Path(root)

    def save(self, report: BenchmarkReport) -> Path:
        """Écrit un rapport sans exposer de fichier partiel."""
        self.root.mkdir(parents=True, exist_ok=True)
        stamp = report.recorded_at.astimezone().strftime("%Y%m%d_%H%M%S_%f")
        path = self.root / f"benchmark_{stamp}.json"
        temporary = path.with_suffix(".tmp")
        temporary.write_text(report.model_dump_json(indent=2), encoding="utf-8")
        temporary.replace(path)
        return path

    def reports(self) -> list[BenchmarkReport]:
        """Retourne les archives lisibles, de la plus récente à la plus ancienne."""
        if not self.root.exists():
            return []
        reports: list[BenchmarkReport] = []
        for path in sorted(self.root.glob("benchmark_*.json"), reverse=True):
            try:
                reports.append(
                    BenchmarkReport.model_validate_json(path.read_text(encoding="utf-8"))
                )
            except OSError, json.JSONDecodeError, ValueError:
                continue
        return reports

    @staticmethod
    def load_path(path: Path | str) -> BenchmarkReport:
        """Charge un rapport explicite, notamment pour une comparaison."""
        source = Path(path)
        return BenchmarkReport.model_validate_json(source.read_text(encoding="utf-8"))
