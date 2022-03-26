#!/bin/bash

##############################################################################
# Function: setup_firewall_rules()
#
# Sets up firewall rules using iptables as described in HW5.
##############################################################################
setup_firewall_rules() {
  echo "IP TABLES RULES!"
}

##############################################################################
# Function: setup_ids_rules()
#
# Sets up intrusion detection rules using snort as described in HW5.
##############################################################################
setup_ids_rules() {
  echo "SNORT RULES!"
}

##############################################################################
# Function: main()
#
# <description>
##############################################################################
main() {
  setup_firewall_rules
  setup_ids_rules
}

main

