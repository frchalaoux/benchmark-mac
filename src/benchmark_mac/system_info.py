"""Inventaire système portable, enrichi sans dépendance native."""

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from .models import SystemSnapshot


def _command(*command: str, timeout: float = 10) -> str:
    try:
        return subprocess.check_output(command, text=True, timeout=timeout).strip()
    except OSError, subprocess.SubprocessError:
        return ""


def _sysctl(name: str) -> str:
    return _command("sysctl", "-n", name)


def _memory_bytes() -> int | None:
    if sys.platform == "darwin":
        value = _sysctl("hw.memsize")
        return int(value) if value.isdigit() and int(value) > 0 else None
    if sys.platform.startswith("linux"):
        try:
            pages = os.sysconf("SC_PHYS_PAGES")
            page_size = os.sysconf("SC_PAGE_SIZE")
            return pages * page_size if pages > 0 and page_size > 0 else None
        except OSError, ValueError:
            return None
    if sys.platform == "win32":
        output = _command(
            "powershell",
            "-NoProfile",
            "-Command",
            "(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory",
        )
        return int(output) if output.isdigit() and int(output) > 0 else None
    return None


def _model() -> str:
    if sys.platform == "darwin":
        return _sysctl("hw.model") or platform.node() or "inconnu"
    if sys.platform == "win32":
        output = _command(
            "powershell",
            "-NoProfile",
            "-Command",
            "(Get-CimInstance Win32_ComputerSystem | Select-Object -ExpandProperty Model)",
        )
        return output or platform.node() or "inconnu"
    for candidate in (
        "/sys/devices/virtual/dmi/id/product_name",
        "/sys/firmware/devicetree/base/model",
    ):
        try:
            value = Path(candidate).read_text(encoding="utf-8").strip("\x00\n ")
        except OSError:
            continue
        if value:
            return value
    return platform.node() or "inconnu"


def _processor() -> str:
    if sys.platform == "darwin":
        return _sysctl("machdep.cpu.brand_string") or platform.processor() or "inconnu"
    if sys.platform == "win32":
        return platform.processor() or os.environ.get("PROCESSOR_IDENTIFIER", "inconnu")
    try:
        for line in Path("/proc/cpuinfo").read_text(encoding="utf-8").splitlines():
            if line.lower().startswith(("model name", "hardware")):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "inconnu"


def _physical_cpu_count() -> int | None:
    if sys.platform == "darwin":
        value = _sysctl("hw.physicalcpu")
        return int(value) if value.isdigit() and int(value) > 0 else None
    if sys.platform == "win32":
        value = _command(
            "powershell",
            "-NoProfile",
            "-Command",
            "(Get-CimInstance Win32_Processor | Measure-Object NumberOfCores -Sum).Sum",
        )
        return int(value) if value.isdigit() and int(value) > 0 else None
    try:
        physical_and_core: set[tuple[str, str]] = set()
        physical = core = "0"
        lines = Path("/proc/cpuinfo").read_text(encoding="utf-8").splitlines() + [""]
        for line in lines:
            if line.startswith("physical id"):
                physical = line.split(":", 1)[1].strip()
            elif line.startswith("core id"):
                core = line.split(":", 1)[1].strip()
            elif not line:
                physical_and_core.add((physical, core))
        return len(physical_and_core) or None
    except OSError:
        return None


def _gpu_devices() -> list[str]:
    if sys.platform == "darwin":
        output = _command("system_profiler", "SPDisplaysDataType", "-json")
        try:
            payload = json.loads(output)
            names = [item.get("sppci_model") for item in payload.get("SPDisplaysDataType", [])]
            return [name for name in names if isinstance(name, str)]
        except json.JSONDecodeError, AttributeError:
            return []
    if sys.platform == "win32":
        output = _command(
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name",
        )
        return [line.strip() for line in output.splitlines() if line.strip()]
    output = _command("lspci")
    return [
        line.split(": ", 1)[-1] for line in output.splitlines() if "VGA" in line or "3D" in line
    ]


def system_snapshot(work_dir: Path | str = ".") -> SystemSnapshot:
    """Capture le matériel, l'OS et l'interpréteur utilisés pour le rapport."""
    usage = shutil.disk_usage(Path(work_dir).resolve())
    return SystemSnapshot(
        system=platform.system(),
        release=platform.release(),
        version=platform.version(),
        machine=platform.machine(),
        model=_model(),
        processor=_processor(),
        physical_cpu_count=_physical_cpu_count(),
        logical_cpu_count=os.cpu_count() or 1,
        memory_bytes=_memory_bytes(),
        gpu_devices=_gpu_devices(),
        python_version=platform.python_version(),
        python_implementation=platform.python_implementation(),
        python_executable=sys.executable,
        disk_total_bytes=usage.total,
        disk_free_bytes=usage.free,
    )
