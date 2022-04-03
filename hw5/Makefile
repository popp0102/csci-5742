DEFENDER_IP=192.168.10.128
SNORT_LOG=./DataAnalysis/snort_log
SNORT_DIR=/etc/snort
WEBAPP_DIR=gruyere-code-remoteaccess

all: clean protect webapp snort

protect:
	sudo ./protect.sh

webapp:
	cd $(WEBAPP_DIR) && python2 gruyere.py&

snort:
	rm -rf $(SNORT_LOG)
	mkdir $(SNORT_LOG)
	sudo snort -l $(SNORT_LOG) -b -c $(SNORT_DIR)/snort.conf -k none

scan: ping-scan udp-scan xmas-scan fin-scan null-scan

ping-scan:
	sudo nmap –sP $(DEFENDER_IP) --disable-arp-ping

xmas-scan:
	sudo nmap -sX $(DEFENDER_IP)

fin-scan:
	sudo nmap -sF $(DEFENDER_IP)

null-scan:
	sudo nmap -sN $(DEFENDER_IP)

udp-scan:
	sudo nmap -sU $(DEFENDER_IP)

clean:
	sudo rm -f $(SNORT_DIR)/rules/hw5-snort.rules
	sudo rm -rf $(SNORT_LOG)
	sudo iptables -F
	-sudo killall -9 snort || true
	-sudo pkill -f "python2 gruyere.py" || true

