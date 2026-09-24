"""Contrats validés utilisés par la suite et les archives JSON."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class SystemSnapshot(BaseModel):
    """Machine et environnement logiciel associés à chaque mesure."""

    system: str
    release: str
    version: str
    machine: str
    model: str
    processor: str
    physical_cpu_count: int | None = Field(default=None, gt=0)
    logical_cpu_count: int = Field(gt=0)
    memory_bytes: int | None = Field(default=None, gt=0)
    gpu_devices: list[str] = Field(default_factory=list)
    python_version: str
    python_implementation: str
    python_executable: str
    disk_total_bytes: int = Field(gt=0)
    disk_free_bytes: int = Field(ge=0)


class EnvironmentSnapshot(BaseModel):
    """Conditions susceptibles d'influencer une campagne de mesures."""

    power_source: str | None = None
    thermal_limit_percent: int | None = Field(default=None, ge=0, le=100)
    temperature_celsius: float | None = Field(default=None, ge=-20, le=150)


class BenchmarkResult(BaseModel):
    """Mesure principale normalisée d'un benchmark."""

    benchmark_id: str
    group: str
    name: str
    description: str
    value: float = Field(gt=0)
    unit: str
    higher_is_better: bool = True
    elapsed_seconds: float = Field(gt=0)
    parameters: dict[str, int | float | str] = Field(default_factory=dict)
    methodology: str = ""
    limitations: str = ""
    references: list[str] = Field(default_factory=list)
    repetitions: int = Field(default=1, gt=0)
    sample_values: list[float] = Field(default_factory=list)
    minimum: float | None = Field(default=None, gt=0)
    maximum: float | None = Field(default=None, gt=0)
    relative_spread_percent: float | None = Field(default=None, ge=0)


class BenchmarkFailure(BaseModel):
    """Échec isolé qui n'empêche pas les autres mesures de s'exécuter."""

    benchmark_id: str
    message: str


class BenchmarkReport(BaseModel):
    """Rapport complet, portable et comparable d'une exécution."""

    schema_version: int = 3
    suite_version: str
    recorded_at: datetime
    label: str | None = None
    profile: str
    repetitions: int = Field(default=1, gt=0)
    requested_benchmarks: list[str]
    system: SystemSnapshot
    environment_start: EnvironmentSnapshot | None = None
    environment_end: EnvironmentSnapshot | None = None
    environment_warnings: list[str] = Field(default_factory=list)
    results: list[BenchmarkResult]
    failures: list[BenchmarkFailure] = Field(default_factory=list)
