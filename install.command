#!/bin/sh
# Lance l'installation POSIX par double-clic depuis le Finder.
set -eu
cd -- "$(dirname -- "$0")"
if [ -f release-version.txt ]; then
    IFS= read -r bundle_version < release-version.txt
    PERFCOMPARATOR_VERSION="${PERFCOMPARATOR_VERSION:-$bundle_version}"
    export PERFCOMPARATOR_VERSION
fi
exec /bin/sh "$PWD/install.sh"
