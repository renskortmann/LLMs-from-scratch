$ErrorActionPreference = "Stop"

Write-Host "Syncing with upstream..."

git checkout main
git fetch upstream
git merge upstream/main
git push origin main

git checkout my-notes
git rebase main

Write-Host "Done. Your my-notes branch is up to date with upstream."
