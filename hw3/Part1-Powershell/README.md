# Powershell monitor

## Description
This script is made to check all of the currently registered tasks and programs that run at start up and check
if they have changed. The script logs a WARNING if a new task is registered or if a task that previously existed is removed.

## To run
`Monitor.ps1` can be run on its own with command line parameters:  
`-PathToCache` which tells the script where to store and read a cache file of all seen processes.  
`-PathToLog` which tells the script where to store the log file.  
or the script `ScheduleMonitor.ps1` can be run to register a periodic job that runs `Monitor.ps1` every 1 minute. Defaults
are used in this case, which are currently specific to the machine this was originally tested on. the params lines at the start
of `Monitor.ps1` would need to be changed to reflect the environment it was being run under. 

## Test
1)`cp .\StartupTestTask.ps1 'C:\Users\${USER}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\' Registers a new task on start
2)`.\TestScheduledTask.ps1` registers a periodic task that should be detected