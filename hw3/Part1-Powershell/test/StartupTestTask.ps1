$cwd = Get-Location
$fileName = "\HelloWorld.ps1"
$completePath = "$cwd" + $fileName
powershell -windowstyle hidden $completePath