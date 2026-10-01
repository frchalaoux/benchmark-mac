#!/bin/sh
# Lance l'installation POSIX depuis l'archive Linux téléchargée.
set -eu
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ -f "$script_dir/release-version.txt" ]; then
    IFS= read -r bundle_version < "$script_dir/release-version.txt"
    PERFCOMPARATOR_VERSION="${PERFCOMPARATOR_VERSION:-$bundle_version}"
    export PERFCOMPARATOR_VERSION
fi
exec /bin/sh "$script_dir/install.sh"
