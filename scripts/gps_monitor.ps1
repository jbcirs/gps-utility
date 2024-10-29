# gps_monitor.ps1
$pythonPath = "C:\Python310\python.exe"  # Update to your Python installation path
$scriptPath = "..\src\gps-utility.py"  # Update to your Python script path

if (Test-Path $pythonPath) {
    Write-Host "Running Python script..."
    & $pythonPath $scriptPath
} else {
    Write-Host "Python not found. Please check your Python installation path."
}
