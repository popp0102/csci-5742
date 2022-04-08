#!/bin/bash

##############################################################################
# Function: log_message()
#
# A helper method to log messages. This centralizes logging to one place.
##############################################################################
log_message() {
  message=$1
  echo `date`" | $message"
}

##############################################################################
# Function: setup_firewall_rules()
#
# Sets up firewall rules using iptables as described in HW5. The rules are:
#  Rule 1: Allow TCP traffic on port 8008 using connection states
#  Rule 2: Allow DNS request and reply traffic
#  Rule 3: Allow for ssh traffic using connection states
#  Rule 4: Allow ICMP ping request/reply traffic
#  Rule 5: Block all other TCP Traffic
#  Rule 6: Block all other UDP Traffic
#  Rule 7: Block all other ICMP Traffic
#  Rule 8: Block from illegal addresses (private address spaces like 10.*.*.*, localhost, broadcast addresses, 0.0.0.0, your own IP address, sourceIP=destinationIP. )
##############################################################################
setup_firewall_rules() {
  log_message "Setting up firewall rules to iptables..."

  LOCAL_IP=`hostname -I`

  # Allows Web Clients to connect on port 8008, State is kept track of for New and Established connections
  iptables -A INPUT  -i eth0 -p tcp --dport 8008 -m state --state NEW,ESTABLISHED -j ACCEPT
  iptables -A OUTPUT -o eth0 -p tcp --sport 8008 -m state --state ESTABLISHED     -j ACCEPT

  # Allow DNS Traffic
  iptables -A OUTPUT -p udp -o eth0 --dport 53 -j ACCEPT
  iptables -A INPUT  -p udp -i eth0 --sport 53 -j ACCEPT

  # Allow SSH Traffic
  iptables -A INPUT  -i eth0 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
  iptables -A OUTPUT -o eth0 -p tcp --sport 22 -m state --state ESTABLISHED     -j ACCEPT

  # Allow ICMP Ping Packets
  iptables -A INPUT  -p icmp --icmp-type echo-request -j ACCEPT
  iptables -A OUTPUT -p icmp --icmp-type echo-reply   -j ACCEPT

  # Drop all other TCP Traffic
  iptables -A INPUT  -p tcp -j DROP
  iptables -A OUTPUT -p tcp -j DROP

  # Drop all other UDP Traffic
  iptables -A INPUT  -p udp -j DROP
  iptables -A OUTPUT -p udp -j DROP

  # Drop all other ICMP Traffic
  iptables -A INPUT  -p icmp -j DROP
  iptables -A OUTPUT -p icmp -j DROP

  # Drop all from illegal source addresses on the INPUT chain
  iptables -A INPUT -s $LOCAL_IP  -j DROP
  iptables -A INPUT -s localhost  -j DROP
  iptables -A INPUT -s 10.0.0.0/8 -j DROP
  iptables -A INPUT -s 0.0.0.0    -j DROP

  # Drop all from illegal source addresses on the OUTPUT chain
  iptables -A OUTPUT -s $LOCAL_IP  -j DROP
  iptables -A OUTPUT -s localhost  -j DROP
  iptables -A OUTPUT -s 10.0.0.0/8 -j DROP
  iptables -A OUTPUT -s 0.0.0.0    -j DROP
}

##############################################################################
# Function: flush_iptables()
#
# Flushes current version of iptables
##############################################################################
flush_iptables() {
  log_message "Flushing iptables..."
  iptables -F
}

##############################################################################
# Function: configure_snort()
#
# This method will add the necessary include line for snort if it doesn't exist
# and log if it already exists.
##############################################################################
configure_snort() {
  log_message "Configuring Snort..."
  echo $INCLUDE_LINE
  echo $RULE_PATH
  echo $RULES_FILE
  INCLUDE_LINE="include $RULE_PATH/$RULES_FILE"
  if [[ ! -z $(grep "$INCLUDE_LINE" $SNORT_CONF) ]]; then
    log_message "Found configuration '$INCLUDE_LINE' in $SNORT_CONF"
  else
    log_message "Adding configuration '$INCLUDE_LINE' to $SNORT_CONF"
    echo $INCLUDE_LINE | sudo tee -a $SNORT_CONF > /dev/null
  fi
}

##############################################################################
# Function: add_hw5_rules_to_snort()
#
# This method will add the necessary snort rules to the custom rules file added
# from configure_snort()
##############################################################################
add_hw5_rules_to_snort() {
  log_message "Adding Snort Rules $RULES_FILE to $SNORT_RULES_DIR"

  sudo cp "./rules/$RULES_FILE" $SNORT_RULES_DIR
  sudo chown root:root $SNORT_RULES_DIR/$RULES_FILE
}

##############################################################################
# Function: run_snort()
#
# This method will run snort. It will create a new snort_log directory each
# time it is run.
##############################################################################
run_snort() {
  SNORT_LOG_DIR='./snort_log'
  log_message "Creating $SNORT_LOG_DIR..."
  rm -rf "./$SNORT_LOG_DIR"
  mkdir -p "./$SNORT_LOG_DIR"

  SNORT_CMD="sudo snort -l $SNORT_LOG_DIR -b -c $SNORT_CONF"
  log_message "Run Snort with: $SNORT_CMD"
  exec $SNORT_CMD
}

##############################################################################
# Function: setup_ids_rules()
#
# Sets up intrusion detection rules using snort as described in HW5.
##############################################################################
setup_ids_rules() {
  SNORT_DIR=`pwd`
  SNORT_RULES_DIR="$SNORT_DIR/rules"
  echo $SNORT_RULES_DIR
  SNORT_CONF="$SNORT_DIR/snort.conf"
  RULES_FILE='hw5-snort.rules'

  configure_snort
 #add_hw5_rules_to_snort
}

##############################################################################
# Function: main()
#
# <description>
##############################################################################
main() {
  flush_iptables
  setup_firewall_rules
  #setup_ids_rules
}

main

