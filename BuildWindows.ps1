if (-not $env:VIRTUAL_ENV) {
    $activateScript = ".\.venv\Scripts\Activate.ps1"
    
    if (Test-Path $activateScript) {
        & $activateScript
    } else {
        Write-Host "Error: Virtual environment activation script not found. Make sure the virtual environment is set up correctly."
        Exit 1
    }
}

$pyInstallerCommand = "PyInstaller --clean -y --dist ./dist/windows --workpath /tmp .\src\hamtare.spec"
Invoke-Expression $pyInstallerCommand
