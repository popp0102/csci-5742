#!/bin/bash

##############################################################################
# Function: scan_network()
#
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
      HOSTS+=$current_host
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
##############################################################################
display_network_differences() {
  for host_port in "${!LAST_SCAN_HOSTS[@]}"
  do
    if ! [[ ${SCANNED_HOSTS["$host_port"]} == open ]]; then
      log_message "OPEN on $host_port"
    fi

    unset SCANNED_HOSTS["$host_port"]
  done

  for host_port in "${!SCANNED_HOSTS[@]}"
  do
    log_message "CLOSE on $host_port"
  done
}

##############################################################################
# Function: save_scanned_network()
#
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

