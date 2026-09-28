#!/bin/sh
# Installe PerfComparator pour le compte courant (macOS ou Linux).
# Python n'a pas besoin d'être déjà installé : uv gère la version reproductible.
set -eu

release_version="${PERFCOMPARATOR_VERSION:-${BENCHMARK_MAC_VERSION:-v0.4.0.dev2}}"
python_version="3.14.4"
source_url="${PERFCOMPARATOR_SOURCE:-${BENCHMARK_MAC_SOURCE:-https://github.com/frchalaoux/perfcomparator/archive/refs/tags/${release_version}.tar.gz}}"
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
if ! "$uv_command" python install "$python_version"; then
    echo "La version actuelle de uv ne trouve pas CPython ${python_version}."
    echo "Mise a niveau de uv depuis l'installateur officiel, puis nouvelle tentative..."
    if command -v curl >/dev/null 2>&1; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
    elif command -v wget >/dev/null 2>&1; then
        wget -qO- https://astral.sh/uv/install.sh | sh
    else
        echo "Erreur : curl ou wget est necessaire pour mettre uv a niveau." >&2
        exit 1
    fi
    uv_command="$HOME/.local/bin/uv"
    if [ ! -x "$uv_command" ]; then
        echo "Erreur : la version mise a niveau de uv est introuvable." >&2
        exit 1
    fi
    if ! "$uv_command" python install "$python_version"; then
        echo "Erreur : CPython ${python_version} reste indisponible apres la mise a niveau de uv." >&2
        exit 1
    fi
fi
legacy_tool_installed=false
if "$uv_command" tool list 2>/dev/null | grep -q '^benchmark-mac v'; then
    legacy_tool_installed=true
fi
if [ "$legacy_tool_installed" = true ]; then
    echo "Nettoyage de l'ancien enregistrement benchmark-mac..."
    "$uv_command" tool uninstall benchmark-mac
fi
echo "Installation de PerfComparator ${release_version}..."
"$uv_command" tool install --managed-python --python "$python_version" --force --reinstall "$source_url"

tool_bin_dir=$("$uv_command" tool dir --bin)
perfcomparator_command="${tool_bin_dir}/perfcomparator"
if [ -x "$perfcomparator_command" ]; then
    echo "Preparation de la contribution guidee..."
    if ! "$perfcomparator_command" setup-contribution --yes; then
        echo "Avertissement : GitHub CLI sera repropose lors de la premiere contribution." >&2
    fi
fi

echo
if command -v perfcomparator >/dev/null 2>&1; then
    echo "PerfComparator est installe. Lancez : perfcomparator list"
else
    echo "PerfComparator est installe. Fermez et rouvrez le terminal, puis lancez : perfcomparator list"
fi
