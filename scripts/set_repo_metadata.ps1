# Run ONCE on your PC after: gh auth login
# Sets homepage + topics for all portfolio repos (elite discoverability)

$ErrorActionPreference = "Stop"
$owner = "nikhilamaragani-jpg"
$homepage = "https://nikhilamaragani-jpg.github.io/"

$repos = @(
  @{ name = "ai-driven-chatbot-smart-tourism"; topics = @("python","nlp","chatbot","conversational-ai","machine-learning","tourism"); desc = "B.Tech Major: AI chatbot for smart tourism | Intent routing, knowledge base, SQLite logging" },
  @{ name = "detection-of-fake-accounts-on-social-media"; topics = @("python","machine-learning","scikit-learn","classification","trust-and-safety"); desc = "B.Tech ML: Fake account detection | Feature engineering, multi-model comparison, F1 metrics" },
  @{ name = "blockchain-autonomous-notarization-e-id"; topics = @("python","blockchain","cryptography","digital-identity","security"); desc = "B.Tech Mini + industry: Blockchain notarization using national eID | SHA-256, ledger, verification" },
  @{ name = "id-detection-and-penalty-mechanism"; topics = @("python","computer-vision","automation","compliance"); desc = "ID detection & penalty automation | Rules engine, audit logging, CV-ready architecture" },
  @{ name = "certificates-achievements"; topics = @("portfolio","certificates","career"); desc = "Certificates, internships, workshops | Amaragani Nikhil Sai" },
  @{ name = "portfolio"; topics = @("portfolio","github-pages","html","css"); desc = "Professional portfolio website | B.Tech CSE · Applied AI · ML" },
  @{ name = "nikhilamaragani-jpg.github.io"; topics = @("portfolio","github-pages","personal-site"); desc = "Personal site | Amaragani Nikhil Sai" },
  @{ name = "nikhilamaragani-jpg"; topics = @("profile","readme","portfolio"); desc = "Profile README | Amaragani Nikhil Sai — Applied AI & ML" }
)

foreach ($r in $repos) {
  Write-Host "Updating $($r.name)..." -ForegroundColor Cyan
  gh api -X PATCH "repos/$owner/$($r.name)" -f homepage="$homepage" -f description="$($r.desc)" | Out-Null
  $names = ($r.topics | ForEach-Object { "`"$_`"" }) -join ","
  gh api -X PUT "repos/$owner/$($r.name)/topics" -H "Accept: application/vnd.github.mercy-preview+json" --input - <<< "{`"names`":[$names]}" 2>$null
  # Windows-friendly topics update:
  $body = @{ names = $r.topics } | ConvertTo-Json -Compress
  $body | gh api -X PUT "repos/$owner/$($r.name)/topics" -H "Accept: application/vnd.github.mercy-preview+json" --input - | Out-Null
  Write-Host "  OK" -ForegroundColor Green
}

Write-Host "`nDone. Refresh your GitHub profile." -ForegroundColor Green
