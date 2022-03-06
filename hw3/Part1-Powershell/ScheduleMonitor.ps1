$atStartupPeriodicTrigger = New-JobTrigger -once -At $(get-date) -RepetitionInterval $([timespan]::FromMinutes("1")) -RepeatIndefinitely
$cwd = Get-Location
$fileName = "\Monitor.ps1"
$completePath = "$cwd" + $fileName
Register-ScheduledJob -Name "CSCI_5742_Task_Monitor" -FilePath $completePath -Trigger $atStartupPeriodicTrigger