param(
  [string]$Target = (Get-Location).Path
)

$BundleDir = Split-Path -Parent $PSScriptRoot

& "$PSScriptRoot/validate_upstream.ps1" -Target $Target

$dest = Join-Path $Target ".caebmad"
New-Item -ItemType Directory -Force -Path $dest | Out-Null

$names = @("module","docs","skills","templates","research")
foreach ($name in $names) {
  $d = Join-Path $dest $name
  if (Test-Path $d) { Remove-Item -Recurse -Force $d }
  Copy-Item -Recurse -Force (Join-Path $BundleDir $name) $d
}

$configDir = Join-Path $dest "_config"
New-Item -ItemType Directory -Force -Path $configDir | Out-Null

Push-Location $Target
$commit = (git rev-parse HEAD).Trim()
$remote = (git remote get-url origin 2>$null).Trim()
Pop-Location

@"
source_url: "$remote"
source_commit: "$commit"
caebmad_version: "1.0.0"
original_bmad_preserved: true
"@ | Set-Content (Join-Path $configDir "upstream-manifest.yaml")

Write-Host "CAE-BMAD installed. Original BMAD files preserved."
Write-Host "Next: caebmad-product-reconstruction"
