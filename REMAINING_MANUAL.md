# Final checklist after elite automation

## Confirmed done (live)

- [x] Bio updated
- [x] Location: Hyderabad, India
- [x] Website: https://nikhilamaragani-jpg.github.io/
- [x] Portfolio site live with full HTML design
- [x] Profile README + all project docs
- [x] Pins (you completed 1–7)

## Still only possible on your side (2 minutes)

### 1) Profile photo (required for elite look)
Use: `OneDrive\Documents\PASSPHOTO\Nikhil passphoto 100kb.jpg`  
Path: https://github.com/settings/profile → upload photo

### 2) Repo topics + homepage (one script)
Open PowerShell:

```powershell
winget install GitHub.cli   # if needed
gh auth login               # browser login once
cd $env:USERPROFILE
gh api user --jq .login    # should print nikhilamaragani-jpg
# then run the script from the profile repo after cloning, OR paste commands from scripts/set_repo_metadata.ps1
```

Or set manually on each repo → ⚙️ About → Website = `https://nikhilamaragani-jpg.github.io/` + topics from the script.

### 3) LinkedIn (copy from LINKEDIN_COPY_PASTE.md)
- Paste Headline + About
- Add Featured links

### 4) Optional: Available for hire
https://github.com/settings/profile → check if shown

### 5) Optional: Upload PDFs to docs/reports/
Via GitHub website “Add file” on each project.

---

**Nothing else is required for a professional student profile.** Content and live site are elite-ready.
