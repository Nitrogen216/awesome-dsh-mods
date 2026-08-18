[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidatePattern('^[a-z0-9][a-z0-9-]*$')]
    [string]$Mode,

    [switch]$Replace
)

$ErrorActionPreference = 'Stop'

$RepoRoot = Split-Path -Parent $PSScriptRoot
$SourceDir = Join-Path (Join-Path $RepoRoot 'modes') $Mode
$Composition = Join-Path $SourceDir 'agent.cordis.yml'

if (-not (Test-Path -LiteralPath $Composition -PathType Leaf)) {
    throw "install-mode: unknown or incomplete mode: $Mode"
}

if ([string]::IsNullOrWhiteSpace($env:DSH_HOME)) {
    $DshHome = Join-Path $HOME '.dsh'
} else {
    $DshHome = $env:DSH_HOME
}

$TargetRoot = Join-Path $DshHome '.agent-presets'
$Target = Join-Path $TargetRoot $Mode

if ((Test-Path -LiteralPath $Target) -and -not $Replace) {
    throw "install-mode: $Target already exists; rerun with -Replace after reviewing local changes"
}

New-Item -ItemType Directory -Path $TargetRoot -Force | Out-Null
$Stage = Join-Path $TargetRoot ('.{0}.install.{1}' -f $Mode, [guid]::NewGuid().ToString('N'))
$Backup = $null

try {
    New-Item -ItemType Directory -Path $Stage | Out-Null
    Get-ChildItem -LiteralPath $SourceDir -Force | Copy-Item -Destination $Stage -Recurse -Force

    if (Test-Path -LiteralPath $Target) {
        $Timestamp = Get-Date -Format 'yyyyMMddHHmmssfff'
        $Backup = "$Target.backup.$Timestamp"
        Move-Item -LiteralPath $Target -Destination $Backup
    }

    try {
        Move-Item -LiteralPath $Stage -Destination $Target
        $Stage = $null
    } catch {
        if ($null -ne $Backup -and -not (Test-Path -LiteralPath $Target)) {
            Move-Item -LiteralPath $Backup -Destination $Target
        }
        throw
    }
} finally {
    if ($null -ne $Stage -and (Test-Path -LiteralPath $Stage)) {
        Remove-Item -LiteralPath $Stage -Recurse -Force
    }
}

Write-Host "Installed $Mode at $Target"
if ($null -ne $Backup) {
    Write-Host "Previous copy saved at $Backup"
}
