<#
Install Elastic Beanstalk CLI (awsebcli) for the current user on Windows.

Usage:
  - Open PowerShell and run (recommended):
      .\scripts\install_eb.ps1
  - To also add the user Scripts directory to your USER PATH permanently run:
      .\scripts\install_eb.ps1 -AddUserPath

This script uses the Python launcher `py` to install the package into the
current user's site-packages and Scripts directory (no admin required).
#>

param(
    [switch]$AddUserPath
)

Write-Host "Checking for Python launcher 'py'..."
$py = Get-Command py -ErrorAction SilentlyContinue
if (-not $py) {
    Write-Error "Python launcher 'py' not found. Install Python 3 from https://www.python.org/ and ensure 'py' is on PATH."
    exit 1
}

Write-Host "Ensuring pip is available..."
& py -3 -m ensurepip --upgrade 2>&1 | Out-Null

Write-Host "Installing/Upgrading AWS EB CLI (awsebcli) for current user..."
& py -3 -m pip install --upgrade --user awsebcli

Write-Host "Resolving user Scripts directory..."
$userBase = & py -3 -c "import site, sys; print(site.USER_BASE)"
if (-not $userBase) {
    Write-Warning "Could not resolve site.USER_BASE. Falling back to default Roaming path."
    $scripts = Join-Path $env:USERPROFILE "AppData\Roaming\Python\Scripts"
} else {
    $scripts = Join-Path $userBase "Scripts"
}

Write-Host "Scripts directory: $scripts"

if (Test-Path (Join-Path $scripts "eb.exe")) {
    Write-Host "Found 'eb' at: $(Join-Path $scripts 'eb.exe')"
} else {
    Write-Warning "'eb.exe' not found in expected location. Verify installation output above."
}

Write-Host "Temporarily adding $scripts to PATH for this PowerShell session..."
$env:PATH = "$scripts;$env:PATH"
Write-Host "You can now run: eb --version"

if ($AddUserPath) {
    Write-Host "Adding Scripts folder to USER PATH (permanent)..."
    try {
        $old = [Environment]::GetEnvironmentVariable('PATH', 'User')
        if ($old -notlike "*${scripts}*") {
            [Environment]::SetEnvironmentVariable('PATH', "$old;$scripts", 'User')
            Write-Host "User PATH updated. Restart your shell or sign out/in for changes to take effect."
        } else {
            Write-Host "User PATH already contains Scripts path."
        }
    } catch {
        Write-Warning "Failed to update User PATH. You can add $scripts to your user PATH manually via Windows Settings -> Environment Variables."
    }
}

Write-Host "Installation script finished. Run 'eb --version' to verify."
