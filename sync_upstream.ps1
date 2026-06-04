param(
	[switch]$CleanupMain
)

$ErrorActionPreference = "Stop"

function Invoke-Git {
	param(
		[Parameter(Mandatory = $true)]
		[string[]]$Arguments
	)

	& git @Arguments
	if ($LASTEXITCODE -ne 0) {
		throw "git $($Arguments -join ' ') failed with exit code $LASTEXITCODE."
	}
}

function Get-GitOutput {
	param(
		[Parameter(Mandatory = $true)]
		[string[]]$Arguments
	)

	$output = & git @Arguments
	if ($LASTEXITCODE -ne 0) {
		throw "git $($Arguments -join ' ') failed with exit code $LASTEXITCODE."
	}

	return $output
}

function Test-GitAncestor {
	param(
		[Parameter(Mandatory = $true)]
		[string]$Ancestor,
		[Parameter(Mandatory = $true)]
		[string]$Descendant
	)

	& git merge-base --is-ancestor $Ancestor $Descendant 2>$null
	switch ($LASTEXITCODE) {
		0 { return $true }
		1 { return $false }
		default {
			throw "git merge-base --is-ancestor $Ancestor $Descendant failed with exit code $LASTEXITCODE."
		}
	}
}

function Assert-GitRemoteExists {
	param(
		[Parameter(Mandatory = $true)]
		[string]$RemoteName
	)

	& git remote get-url $RemoteName 1>$null 2>$null
	if ($LASTEXITCODE -ne 0) {
		throw "Git remote '$RemoteName' is not configured. Add it before running sync_upstream.ps1."
	}
}

function Assert-CleanWorktree {
	$status = Get-GitOutput @("status", "--porcelain")
	if ($status) {
		throw "Working tree is not clean. Commit, stash, or discard changes before running sync_upstream.ps1."
	}
}

Write-Host "Syncing with upstream..."

Assert-CleanWorktree
Assert-GitRemoteExists "origin"
Assert-GitRemoteExists "upstream"
Invoke-Git @("fetch", "origin")
Invoke-Git @("fetch", "upstream")
Invoke-Git @("checkout", "main")

if ($CleanupMain) {
	Write-Host "Cleanup mode enabled: resetting main to upstream/main."
	Invoke-Git @("reset", "--hard", "upstream/main")
	Invoke-Git @("push", "origin", "main", "--force-with-lease")
}
else {
	if (-not (Test-GitAncestor "main" "upstream/main")) {
		throw "main cannot be fast-forwarded to upstream/main. Run .\sync_upstream.ps1 -CleanupMain once to realign main with upstream."
	}

	Invoke-Git @("merge", "--ff-only", "upstream/main")
	Invoke-Git @("push", "origin", "main")
}

Invoke-Git @("checkout", "my-notes")
Invoke-Git @("rebase", "main")
Invoke-Git @("push", "origin", "my-notes", "--force-with-lease")

Write-Host "Done. main is synced and my-notes is rebased onto it."
