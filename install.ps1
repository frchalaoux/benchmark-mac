# Installe benchmark-mac pour le compte courant (Windows PowerShell).
# Python n'a pas besoin d'être déjà installé : uv gère la version reproductible.
$ErrorActionPreference = "Stop"

$releaseVersion = if ($env:BENCHMARK_MAC_VERSION) {
    $env:BENCHMARK_MAC_VERSION
}
else {
    "v0.3.0.dev1"
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

function Install-CurrentUv {
    $installerPath = Join-Path ([IO.Path]::GetTempPath()) "uv-installer-$([guid]::NewGuid()).ps1"
    try {
        Invoke-WebRequest -UseBasicParsing https://astral.sh/uv/install.ps1 -OutFile $installerPath
        $powerShellExecutable = Join-Path $PSHOME "powershell.exe"
        if (-not (Test-Path $powerShellExecutable)) {
            $powerShellExecutable = Join-Path $PSHOME "pwsh.exe"
        }
        if (-not (Test-Path $powerShellExecutable)) {
            throw "Impossible de trouver l'exécutable PowerShell utilisé pour installer uv."
        }
        & $powerShellExecutable -NoProfile -ExecutionPolicy Bypass -File $installerPath
        if ($LASTEXITCODE -ne 0) {
            throw "L'installateur officiel de uv a échoué (code $LASTEXITCODE)."
        }
    }
    finally {
        Remove-Item -LiteralPath $installerPath -Force -ErrorAction SilentlyContinue
    }
}

if (Get-Command uv -ErrorAction SilentlyContinue) {
    $uvCommand = "uv"
}
else {
    Write-Host "Installation de uv..."
    Install-CurrentUv
    $uvPath = Join-Path $HOME ".local\bin\uv.exe"
    if (-not (Test-Path $uvPath)) {
        throw "uv est introuvable apres son installation."
    }
    $uvCommand = $uvPath
}

Write-Host "Installation de CPython $pythonVersion gere par uv..."
& $uvCommand python install $pythonVersion
if ($LASTEXITCODE -ne 0) {
    Write-Host "La version actuelle de uv ne trouve pas CPython $pythonVersion."
    Write-Host "Mise a niveau de uv depuis l'installateur officiel, puis nouvelle tentative..."
    Install-CurrentUv
    $updatedUvPath = Join-Path $HOME ".local\bin\uv.exe"
    if (-not (Test-Path $updatedUvPath)) {
        throw "La version mise a niveau de uv est introuvable dans $updatedUvPath."
    }
    $uvCommand = $updatedUvPath
    & $uvCommand python install $pythonVersion
    if ($LASTEXITCODE -ne 0) {
        throw "L'installation de Python $pythonVersion a encore échoué après la mise à niveau de uv (code $LASTEXITCODE)."
    }
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
