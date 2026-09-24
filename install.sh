#!/bin/sh
# Installe benchmark-mac pour le compte courant (macOS ou Linux).
# Python n'a pas besoin d'être déjà installé : uv gère la version reproductible.
set -eu

release_version="${BENCHMARK_MAC_VERSION:-v0.2.1}"
python_version="3.14.4"
source_url="${BENCHMARK_MAC_SOURCE:-https://github.com/frchalaoux/benchmark-mac/archive/refs/tags/${release_version}.tar.gz}"
script_dir=""
if [ -f "$0" ]; then
    script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" 2>/dev/null && pwd || true)
fi

if [ -n "$script_dir" ] && [ -f "$script_dir/pyproject.toml" ]; then
    source_url="$script_dir"
fi

if command -v uv >/dev/null 2>&1; then
    uv_command="uv"
elif [ -x "$HOME/.local/bin/uv" ]; then
    uv_command="$HOME/.local/bin/uv"
else
    echo "Installation de uv..."
    if command -v curl >/dev/null 2>&1; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
    elif command -v wget >/dev/null 2>&1; then
        wget -qO- https://astral.sh/uv/install.sh | sh
    else
        echo "Erreur : curl ou wget est necessaire pour installer uv." >&2
        exit 1
    fi
    uv_command="$HOME/.local/bin/uv"
fi

if [ ! -x "$uv_command" ] && ! command -v "$uv_command" >/dev/null 2>&1; then
    echo "Erreur : uv est introuvable apres son installation." >&2
    exit 1
fi

echo "Installation de CPython ${python_version} gere par uv..."
"$uv_command" python install "$python_version"
echo "Installation de benchmark-mac ${release_version}..."
"$uv_command" tool install --managed-python --python "$python_version" --reinstall "$source_url"

echo
if command -v benchmark-mac >/dev/null 2>&1; then
    echo "benchmark-mac est installe. Lancez : benchmark-mac list"
else
    echo "benchmark-mac est installe. Fermez et rouvrez le terminal, puis lancez : benchmark-mac list"
fi
