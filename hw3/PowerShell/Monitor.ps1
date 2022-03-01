
#
# Homework 3 - Powershell: Finding Programs that start on boot
#
# Path: 'D:\Code\Classes\csci-5742\hw3\TestLocations'

<#####
 # Logging function, appends to a file at the variable LogLocation
 # Appends the current time with millisecond resolution
 #############>
function logInfo {
	param (
	    $text
	)
	$LogLocation = 'D:\Code\Classes\csci-5742\hw3\Homework3_Powershell.log'
	$currentTime = Get-Date -UFormat %s
	echo "[$currentTime] $text"|Out-File -FilePath $LogLocation -Append
	 
}

function writeDictionaryAsHereString {
	param (
	    $dictionary
	)
	$data="" #'@"' + "`r`n"
	foreach ($key in $dictionary.keys) {
		$data += $key + " = " +  $dictionary[$key] + "`r`n"
	}
	$fileCacheLocation = 'D:\Code\Classes\csci-5742\hw3\RegistryCache.herestring'
	$outString=$data #+ '"@'
	Out-File -FilePath $fileCacheLocation -InputObject $outString
}

# Load all of the Registry locations into an array
# File is assumed to have a Registry location per line

$PathToLocations = $args[0]
$globalDictionary = @{}
$cachedDictionaryString = Get-Content D:\Code\Classes\csci-5742\hw3\RegistryCache.herestring -Raw 
if($cachedDictionaryString) {
	$globalDictionary = ConvertFrom-StringData $cachedDictionaryString
}
echo $globalDictionary
$arrayOfLocationsToCheck = [IO.File]::ReadAllLines($PathToLocations)
foreach ($line in $arrayOfLocationsToCheck){
    logInfo -text $line
}


$testKey = "Goodnight"
$testValue = "Moon"
try {
    $globalDictionary.add($testKey, $testValue)
} catch { "yerrr" }
writeDictionaryAsHereString $globalDictionary
