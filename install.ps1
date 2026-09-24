# Installe benchmark-mac pour le compte courant (Windows PowerShell).
# Python n'a pas besoin d'être déjà installé : uv gère la version reproductible.
$ErrorActionPreference = "Stop"

$releaseVersion = if ($env:BENCHMARK_MAC_VERSION) {
    $env:BENCHMARK_MAC_VERSION
}
else {
    "v0.2.1"
}
$pythonVersion = "3.14.4"
$sourceUrl = if ($env:BENCHMARK_MAC_SOURCE) {
    $env:BENCHMARK_MAC_SOURCE
}
else {
    "https://github.com/frchalaoux/benchmark-mac/archive/refs/tags/$releaseVersion.tar.gz"
}

if ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot "pyproject.toml"))) {
    $sourceUrl = $PSScriptRoot
}

if (Get-Command uv -ErrorAction SilentlyContinue) {
    $uvCommand = "uv"
}
else {
    Write-Host "Installation de uv..."
    irm https://astral.sh/uv/install.ps1 | iex
    $uvPath = Join-Path $HOME ".local\bin\uv.exe"
    if (-not (Test-Path $uvPath)) {
        throw "uv est introuvable apres son installation."
    }
    $uvCommand = $uvPath
}

Write-Host "Installation de CPython $pythonVersion gere par uv..."
& $uvCommand python install $pythonVersion
if ($LASTEXITCODE -ne 0) {
    throw "L'installation de Python $pythonVersion a échoué (code $LASTEXITCODE)."
}

Write-Host "Installation de benchmark-mac $releaseVersion..."
& $uvCommand tool install --managed-python --python $pythonVersion --reinstall $sourceUrl
if ($LASTEXITCODE -ne 0) {
    throw "L'installation de benchmark-mac a échoué (code $LASTEXITCODE)."
}

Write-Host ""
if (Get-Command benchmark-mac -ErrorAction SilentlyContinue) {
    Write-Host "benchmark-mac est installe. Lancez : benchmark-mac list"
}
else {
    Write-Host "benchmark-mac est installe. Fermez et rouvrez PowerShell, puis lancez : benchmark-mac list"
}
