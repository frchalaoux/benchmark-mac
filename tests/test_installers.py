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
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    versions = (ROOT / "docs" / "versions.md").read_text(encoding="utf-8")

    assert project["project"]["version"] == __version__
    assert EXPECTED_TAG in posix_installer
    assert EXPECTED_TAG in windows_installer
    assert "BENCHMARK_MAC_VERSION" in posix_installer
    assert "BENCHMARK_MAC_VERSION" in windows_installer
    assert "Install-CurrentUv" in windows_installer
    assert "-File $installerPath" in windows_installer
    assert "irm https://astral.sh/uv/install.ps1 | iex" not in windows_installer
    for document in (readme, versions):
        assert __version__ in document
        assert "/v0.3.0.dev0/install.sh" in document
        assert "/v0.3.0.dev0/install.ps1" in document
        assert f"/{EXPECTED_TAG}/install.sh" not in document
        assert f"/{EXPECTED_TAG}/install.ps1" not in document


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


def test_posix_installer_updates_uv_and_retries_when_python_is_unknown(tmp_path: Path) -> None:
    installer = tmp_path / "install.sh"
    installer.write_text((ROOT / "install.sh").read_text(encoding="utf-8"), encoding="utf-8")
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    managed_bin = tmp_path / ".local" / "bin"
    managed_bin.mkdir(parents=True)
    old_uv = fake_bin / "uv"
    old_uv.write_text(
        '#!/bin/sh\nprintf "%s\\n" "old:$*" >> "$UV_LOG"\n'
        'case "$*" in "python install "*) exit 2;; esac\n',
        encoding="utf-8",
    )
    old_uv.chmod(0o755)
    updated_uv = tmp_path / "updated-uv"
    updated_uv.write_text(
        '#!/bin/sh\nprintf "%s\\n" "updated:$*" >> "$UV_LOG"\n',
        encoding="utf-8",
    )
    updated_uv.chmod(0o755)
    curl = fake_bin / "curl"
    curl.write_text(
        "#!/bin/sh\n"
        "printf '%s\\n' "
        '\'cp "$FAKE_UPDATED_UV" "$HOME/.local/bin/uv"\' '
        "'chmod +x \"$HOME/.local/bin/uv\"'\n",
        encoding="utf-8",
    )
    curl.chmod(0o755)
    log = tmp_path / "uv.log"
    environment = os.environ | {
        "HOME": str(tmp_path),
        "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
        "FAKE_UPDATED_UV": str(updated_uv),
        "UV_LOG": str(log),
    }

    subprocess.run(["sh", str(installer)], check=True, env=environment, capture_output=True)

    calls = log.read_text(encoding="utf-8")
    assert "old:python install 3.14.4" in calls
    assert "updated:python install 3.14.4" in calls
    assert "updated:tool install" in calls
