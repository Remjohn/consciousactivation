param(
  [string]$Target = "."
)

$requiredDirs = @(
  "src/core-skills",
  "src/bmm-skills",
  "src/scripts",
  "tools",
  "docs"
)

foreach ($d in $requiredDirs) {
  if (-not (Test-Path (Join-Path $Target $d))) {
    throw "FAIL: missing mandatory original directory: $d"
  }
}

$requiredFiles = @(
  "src/core-skills/bmad-help/SKILL.md",
  "src/core-skills/bmad-deep-recon/SKILL.md",
  "src/core-skills/bmad-advanced-elicitation/SKILL.md",
  "src/core-skills/bmad-review/SKILL.md",
  "src/core-skills/bmad-customize/SKILL.md",
  "src/core-skills/bmad-brainstorming/SKILL.md",
  "src/core-skills/bmad-forge-idea/SKILL.md",
  "src/core-skills/bmad-party-mode/SKILL.md"
)

foreach ($f in $requiredFiles) {
  if (-not (Test-Path (Join-Path $Target $f))) {
    throw "FAIL: missing mandatory original skill: $f"
  }
}

function Check-Any([string]$Label, [string[]]$Patterns) {
  foreach ($pattern in $Patterns) {
    $found = Get-ChildItem (Join-Path $Target "src/bmm-skills") -Recurse -Filter "SKILL.md" |
      Where-Object { $_.FullName -like "*$pattern*" } |
      Select-Object -First 1
    if ($found) {
      Write-Host "OK: $Label"
      return
    }
  }
  throw "FAIL: missing BMM capability: $Label"
}

Check-Any "Product Brief" @("bmad-product-brief", "bmad-create-product-brief")
Check-Any "PRD" @("bmad-prd")
Check-Any "UX" @("bmad-ux", "bmad-create-ux-design")
Check-Any "Architecture" @("bmad-architecture", "bmad-create-architecture")
Check-Any "Epics and Stories" @("bmad-create-epics-and-stories")
Check-Any "Implementation Story" @("bmad-create-story")
Check-Any "Development Story" @("bmad-dev-story")
Check-Any "Code Review" @("bmad-code-review")
Check-Any "Project Context" @("bmad-project-context")

Write-Host "PASS: mandatory BMAD upstream structure is present."
