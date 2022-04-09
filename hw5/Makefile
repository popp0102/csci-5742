# comment line if called from attacking machine
DEFENDER_IP=$(shell hostname -I) 

# uncomment and fill in DEFENDER if called from attacking machine
#DEFENDER_IP=DEFENDER

# Directory Variables
SNORT_DIR=./snort
SNORT_LOG_DIR=$(SNORT_DIR)/log
WEBAPP_DIR=gruyere-code-remoteaccess

all: clean protect webapp run-snort

protect:
	sudo ./protect.sh

webapp:
	cd $(WEBAPP_DIR) && python2 gruyere.py&

run-snort:
	sudo rm -rf $(SNORT_LOG_DIR)
	sudo mkdir -p $(SNORT_LOG_DIR)
	sudo snort -l $(SNORT_LOG_DIR) -b -c $(SNORT_DIR)/snort.conf -k none

scan: ping-scan udp-scan xmas-scan fin-scan null-scan

ping-scan:
	sudo nmap -sP $(DEFENDER_IP) --disable-arp-ping

xmas-scan:
	sudo nmap -sX $(DEFENDER_IP)

fin-scan:
	sudo nmap -sF $(DEFENDER_IP)

null-scan:
	sudo nmap -sN $(DEFENDER_IP)

udp-scan:
	sudo nmap -sU $(DEFENDER_IP)

watch:
	tail -f $(SNORT_LOG_DIR)/alert

clean:
	sudo rm -rf $(SNORT_LOG_DIR)
	sudo iptables -F
	-sudo killall -9 snort || true
	-sudo pkill -f "python2 gruyere.py" || true

