SNORT_LOG=./DataAnalysis/snort_log
SNORT_DIR=/etc/snort

protect:
	sudo ./protect.sh

snort:
	rm -rf $(SNORT_LOG)
	mkdir $(SNORT_LOG)
	sudo snort -l $(SNORT_LOG) -b -c $(SNORT_DIR)/snort.conf

clean:
	sudo rm -f $(SNORT_DIR)t/rules/hw5-snort.rules
	sudo rm -rf $(SNORT_LOG)
	sudo iptables -F
