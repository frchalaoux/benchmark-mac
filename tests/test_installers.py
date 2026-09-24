import os
import subprocess
import tomllib
from pathlib import Path

from benchmark_mac import __version__

ROOT = Path(__file__).parents[1]
EXPECTED_TAG = f"v{__version__}"


def test_versions_are_consistent_across_package_and_installers() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    posix_installer = (ROOT / "install.sh").read_text(encoding="utf-8")
    windows_installer = (ROOT / "install.ps1").read_text(encoding="utf-8")

    assert project["project"]["version"] == __version__
    assert EXPECTED_TAG in posix_installer
    assert EXPECTED_TAG in windows_installer
    assert "BENCHMARK_MAC_VERSION" in posix_installer
    assert "BENCHMARK_MAC_VERSION" in windows_installer


def test_posix_installer_defaults_to_its_own_tag(tmp_path: Path) -> None:
    installer = tmp_path / "install.sh"
    installer.write_text((ROOT / "install.sh").read_text(encoding="utf-8"), encoding="utf-8")
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    uv = fake_bin / "uv"
    uv.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$UV_LOG"\n', encoding="utf-8")
    uv.chmod(0o755)
    log = tmp_path / "uv.log"
    environment = os.environ | {
        "HOME": str(tmp_path),
        "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
        "UV_LOG": str(log),
    }
    environment.pop("BENCHMARK_MAC_SOURCE", None)
    environment.pop("BENCHMARK_MAC_VERSION", None)

    subprocess.run(["sh", str(installer)], check=True, env=environment, capture_output=True)

    calls = log.read_text(encoding="utf-8")
    assert f"archive/refs/tags/{EXPECTED_TAG}.tar.gz" in calls
    assert "refs/tags/v0.1.0.tar.gz" not in calls


def test_posix_installer_honors_an_explicit_source(tmp_path: Path) -> None:
    installer = tmp_path / "install.sh"
    installer.write_text((ROOT / "install.sh").read_text(encoding="utf-8"), encoding="utf-8")
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    uv = fake_bin / "uv"
    uv.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$UV_LOG"\n', encoding="utf-8")
    uv.chmod(0o755)
    log = tmp_path / "uv.log"
    source = "https://example.invalid/benchmark-mac.tar.gz"
    environment = os.environ | {
        "BENCHMARK_MAC_SOURCE": source,
        "HOME": str(tmp_path),
        "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
        "UV_LOG": str(log),
    }

    subprocess.run(["sh", str(installer)], check=True, env=environment, capture_output=True)

    assert source in log.read_text(encoding="utf-8")
