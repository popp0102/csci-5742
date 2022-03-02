#!/bin/bash

##############################################################################
# Function: scan_network()
#
# This method scans the network using nmap on the passed in subnet. It will
# check all ports from 1-65535 on each host in the subnet. After running nmap
# the output is parsed and processed line by line. It first captures the host
# it finds in the list. Then the open ports will follow. This method assumes
# nmap output will always be of the same form (host then ports displayed).
# It uses the regexes provided below to parse and capture the relevant host
# and port numbers. It then places them in an associative array to be later
# processed.
##############################################################################
scan_network() {
  subnet=$1

  log_message "Scanning $subnet"
  nmapscan=`nmap -p 1-65535 $subnet`

  ip_regex='^Nmap scan report for (.*)$'
  port_regex='^([0-9]+)/[A-Za-z]+.*'

  current_host=''
  while read line
  do
    if [[ $line =~ $ip_regex ]]; then
      current_host=${BASH_REMATCH[1]}
    fi

    if [[ $line =~ $port_regex ]]; then
      port=${BASH_REMATCH[1]}
      SCANNED_HOSTS[$current_host:$port]=open
    fi
  done <<< $nmapscan
}

##############################################################################
# Function: display_network_differences()
#
# This method checks the differences from the last scan and the scan from the
# current run. It does this by cycling through the last scanned hosts and checks
# if it's in the current scanned hosts. If it's not in the scanned hosts, that
# means it was recently opened. In either case we can remove the host_port 
# combo from the SCANNED_HOSTS list because of this check and whatever is left
# over in this scanne hosts port list must be new host/port pairs that were opened.
##############################################################################
display_network_differences() {
  for host_port in "${!LAST_SCAN_HOSTS[@]}"
  do
    if ! [[ ${SCANNED_HOSTS["$host_port"]} == open ]]; then
      log_message "CLOSE on $host_port"
    fi

    unset SCANNED_HOSTS["$host_port"]
  done

  for host_port in "${!SCANNED_HOSTS[@]}"
  do
    log_message "OPEN on $host_port"
  done
}

##############################################################################
# Function: save_scanned_network()
#
# This  method simply saves the scanned hosts to a text file located in the
# HOST_DB_FILE variable.
##############################################################################
save_scanned_network() {
  log_message "Saving scanned hosts to $HOST_DB_FILE"
  for host_port in "${!SCANNED_HOSTS[@]}"
  do
    echo $host_port >> $HOST_DB_FILE
  done
}

##############################################################################
# Function: load_last_scan()
#
# This method will read in the last scanned hosts. This will be later used to
# check differences in the current scan. Note this method will rm the file as
# it will be created later when it gets saved.
##############################################################################
load_last_scan() {
  if ! [ -f $HOST_DB_FILE ]; then
    log_message "No host db file, running first scan..."
    return
  fi

  log_message "Loading scan file $HOST_DB_FILE"
  while IFS= read line
  do
    LAST_SCAN_HOSTS[$line]=open
  done < $HOST_DB_FILE

  rm $HOST_DB_FILE
}

##############################################################################
# Function: log_message()
#
# A helper method to log messages. This centralizes logging to one place.
##############################################################################
log_message() {
  message=$1
  echo `date`" | $message" >> $LOGFILE
}

##############################################################################
# Function: main()
#
# Entrypoint method to setup variables and run the high level methods. First
# we load the last scan, scan the current network, save that scan, then detect
# and display any differences. The method takes one argument which is a CIDR
# subnet string (eg 192.168.86.0/24).
##############################################################################
main() {
  LOGFILE='network-log.txt'
  HOST_DB_FILE='./host-db.txt'
  declare -A SCANNED_HOSTS
  declare -A LAST_SCAN_HOSTS

  load_last_scan
  scan_network $1
  save_scanned_network
  display_network_differences
}

main "192.168.86.0/24"
#main "127.0.0.1"

