# Description
This README goes over the basics to setting up and running this project.
Although any of these command can be run maually, We use a Makefile to make all
of the commands much easier to run.

# Requirements
The only requirement is this is run on the same Kali VM the professor setup as
it was only tested here. The homework requires 2 Kali VMs - one attacker and
one defender.

# Quickstart
From the defending machine:
  * open a terminal
  * make
  * open a 2nd terminal
  * make watch
  * see snort alerts after running scans or attacks from attacking machine

# Data Analysis
See DataAnalysis/README.md for more details

# Description of Make targets
As mentioned above we have various make targets to run this project. If you just want
to run the project see Quickstart. This section will dive into what each target is doing.

all:
If you just type "make" without any arguments it will run the "all" target. This is simply
a wrapper target to run clean, protect, webapp, and run-snort.

protect:
This target will run the protect.sh script. This script will do the following:
  * flush existing iptables rules
  * setup iptables rules as per hw5
  * display a message on seeing the newly generated  rules

webapp:
This target will simply run the modified gruyere webapp that was provided by hw5.

run-snort:
This target will run snort with all of our local config files and rules. Note we are
using configuration provided in the local snort subdirectory. Our snort rules are defined
here: 'snort/rules/hw5-snort.rules'

watch:
Runs a simple tail -f command on the snort alert log so you can watch anything snort detects.

clean:
This target will remove the snort logs, iptables, and kill the gruyere and snort processes.

scan:
Usually run from the attacking machine. This is a wrapper target to run nmap scans on the
defending machine. It includes: ping-scan udp-scan, xmas-scan, fin-scan, and null-scan.

ping-scan:
Usually run from the attacking machine. This runs a ping scan on the <defender ip>.

udp-scan:
Usually run from the attacking machine. This runs a udp scan on the <defender ip>.

xmas-scan:
Usually run from the attacking machine. This runs a xmas scan on the <defender ip>.

fin-scan:
Usually run from the attacking machine. This runs a fin scan on the <defender ip>.

null-scan:
Usually run from the attacking machine. This runs a null scan on the <defender ip>.



