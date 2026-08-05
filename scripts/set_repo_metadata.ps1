# Elite repo metadata: homepage + topics
# Prerequisites:
#   1) winget install GitHub.cli
#   2) gh auth login   (browser once)
#   3) Run this script:  powershell -ExecutionPolicy Bypass -File .\scripts\set_repo_metadata.ps1

$ErrorActionPreference = "Stop"
$owner = "nikhilamaragani-jpg"
$homepage = "https://nikhilamaragani-jpg.github.io/"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
  Write-Error "GitHub CLI (gh) not found. Install: winget install GitHub.cli"
}

gh auth status | Out-Null

$repos = @(
  @{ name = "ai-driven-chatbot-smart-tourism"; topics = @("python","nlp","chatbot","conversational-ai","machine-learning","tourism"); desc = "B.Tech Major: AI chatbot for smart tourism | Intent routing, knowledge base, SQLite logging" },
  @{ name = "detection-of-fake-accounts-on-social-media"; topics = @("python","machine-learning","scikit-learn","classification","trust-and-safety"); desc = "B.Tech ML: Fake account detection | Multi-model comparison, F1 metrics, audit logs" },
  @{ name = "blockchain-autonomous-notarization-e-id"; topics = @("python","blockchain","cryptography","digital-identity","security"); desc = "B.Tech Mini + industry: Blockchain notarization + national eID | SHA-256, ledger, verify" },
  @{ name = "id-detection-and-penalty-mechanism"; topics = @("python","computer-vision","automation","compliance"); desc = "ID detection & penalty automation | Rules engine, audit logging, CV-ready design" },
  @{ name = "certificates-achievements"; topics = @("portfolio","certificates","career"); desc = "Certificates, internships, workshops | Amaragani Nikhil Sai" },
  @{ name = "portfolio"; topics = @("portfolio","github-pages","html","css"); desc = "Professional portfolio website | Applied AI · ML" },
  @{ name = "nikhilamaragani-jpg.github.io"; topics = @("portfolio","github-pages","personal-site"); desc = "Personal site | Amaragani Nikhil Sai" },
  @{ name = "nikhilamaragani-jpg"; topics = @("profile","readme","portfolio"); desc = "Profile README | Applied AI & ML" }
)

foreach ($r in $repos) {
  Write-Host "Updating $($r.name)..." -ForegroundColor Cyan
  gh api -X PATCH "repos/$owner/$($r.name)" -f homepage="$homepage" -f description="$($r.desc)" | Out-Null
  $json = @{ names = $r.topics } | ConvertTo-Json -Compress
  $json | gh api -X PUT "repos/$owner/$($r.name)/topics" -H "Accept: application/vnd.github+json" --input - | Out-Null
  Write-Host "  OK" -ForegroundColor Green
}

Write-Host "`nAll set. Hard-refresh github.com/$owner" -ForegroundColor Green
