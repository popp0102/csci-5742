$action = New-ScheduledTaskAction -Execute 'notepad.exe'
$trigger = New-ScheduledTaskTrigger -Once -At 0am  -RepetitionInterval  (New-TimeSpan -Minutes 30)
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "ScheduledTestTask" -Description "A test for monitor"