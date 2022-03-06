param(
	[string]$PathToCache = "D:\Code\Classes\csci-5742\hw3\PowerShell\RegistryCache.herestring",
	[string]$PathToLog = "D:\Code\Classes\csci-5742\hw3\PowerShell\Homework3_Powershell.log"
)
#
# Homework 3 - Powershell: Finding Programs that start on boot
#



# Globals
$globalDictionary = @{}
$inputKeys = @{}
$state = [ScriptState]::Initialized

# Definitions
enum ScriptState {
	First = 0 # Script has never been run, no cache exists
	Initialized = 1 # Cache exists
}

enum CacheEntryState {
	New = 0 # Has never been seen
	Old = 1 # Has been seen at least once
}

# Function Definitions

<#####
 # Logging function, appends to a file at the variable LogLocation
 # Appends the current time with millisecond resolution
 #############>
function logInfo {
	param (
	    $text,
		$LogLocation
	)
	$currentTime = Get-Date -UFormat %s
	echo "[$currentTime] $text"|Out-File -FilePath $LogLocation -Append
	 
}

<#####
# Persist the services in hashtable as a text file
#####>
function writeDictionaryAsString {
	param (
	    $dictionary,
		$fileCacheLocation
	)
	$outString=""
	#Copy key value pairs into string separated by crlf
	foreach ($key in $dictionary.keys) {
		$outString += $key + " = " +  $dictionary[$key] + "`r`n"
	}
	Out-File -FilePath $fileCacheLocation -InputObject $outString
}

<#####
 # Look for key in dictionary and alert if key is new, but only if not the first time run (i.e. a cache exists)
 #############>
function checkDictionary {
	param (
		[string]$DictionaryKey,
		[string]$logPath
	)
	#add to dictionary for O(1) check later.
	$inputKeys.add($DictionaryKey, "")
	if($state -eq [ScriptState]::Initialized) {
		if($globalDictionary.ContainsKey($DictionaryKey)) {
			$keyState = $globalDictionary[$DictionaryKey]
			if($keyState -eq [CacheEntryState]::New) {
				$globalDictionary[$DictionaryKey] = [CacheEntryState]::Old
			}
		} else {
			$errorString = "[WARNING] New service that starts on boot was detected: " + $DictionaryKey
			logInfo -text $errorString -LogLocation $logPath

			$globalDictionary[$DictionaryKey] = [CacheEntryState]::New
		}
	} else {
		$globalDictionary.add($DictionaryKey, [CacheEntryState]::New)
	}
}


<#####
# Check if there are processes that were seen previously that are not seen this time.
#  Only necessary if this isn't the first run.
############>
function checkDictionaryForLostKeys {
	param (
		[string]$logPath
	)
	if($state -ne [ScriptState]::First) {
	    foreach($key in ($globalDictionary).keys) {
		    if( -not ($inputKeys.ContainsKey($key))) {
				
				$logString = "[WARNING] key: " + $key + " not found, was service removed? Key state was: " + $globalDictionary[$key]
				($globalDictionary).Remove($key)
			    logInfo -text $logString -LogLocation $logPath
		    }
	    }
	}
}

<#####
# Strips whitespace and = from the input key,
# As equal is used when parsing entries for the hashtable, they must be transformed.
# In this case we are url (percent) encoding it
############>
function stripKey {
	param (
	$key
	)
	
	$key = $key -replace '\s',''
	$key = $key -replace '=', '%3d'
	return $key
}

##############################################################################################
########################################### MAIN #############################################

# Load all of the Registry locations into an array
# File is assumed to have a Registry location per line
logInfo -text "[Info] Checking registry Locations" -LogLocation $PathToLog

try {
    $cachedDictionaryString = Get-Content $PathToCache -Raw 
} catch {
	logInfo -text "Cache Location Not Found" -LogLocation $PathToLog
}

# If dictionary string isn't empty, load into global dictionary, otherwise, assume this is the first run 
if($cachedDictionaryString) {
	$globalDictionary = ConvertFrom-StringData $cachedDictionaryString
} else {
	$state = [ScriptState]::First
}

# Get Services that start on boot
$BootServices = (get-ciminstance Win32_StartupCommand)| select-object Name,Command
foreach ($service in $BootServices) {
	#dictionary key will be of the form "Name;Command"
	$DictionaryKey = "bootservice-" + ($service).Name + ";" + ($service).Command
	$DictionaryKey = stripKey -key $DictionaryKey
	checkDictionary -DictionaryKey $DictionaryKey -logPath $PathToLog
}

# Get scheduled tasks that are either Running or Ready to Run.
$TaskList = (get-scheduledtask).where{($_.State -CEQ "Ready" -or $_.State -CEQ "Running")}|select-object TaskName, TaskPath
foreach ($task in $TaskList) {
	# Concatenate the Task name and Task Path separated by a semicolon
	$DictionaryKey = "scheduledtask-" + ($task).taskName + ";" + ($task).taskPath
	$DictionaryKey = stripKey -key $DictionaryKey
	checkDictionary -DictionaryKey $DictionaryKey -logPath $PathToLog
}

checkDictionaryForLostKeys -logPath $PathToLog

#Save dictionary to cache
writeDictionaryAsString -dictionary $globalDictionary -fileCacheLocation $PathToCache