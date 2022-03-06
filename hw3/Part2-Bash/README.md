# Running Part 2 - Bash Scripting
The following steps can be used to run the network change monitor for part 2:

* ./network-change-monitor.sh "192.168.10.0/24"
* cat $HOME/network-log.txt

This will log to a file called network-log.txt in the $HOME directory. All info
can be seen there. If you want to watch it in real time simply invoke: `tail -f
$HOME/network-log.txt`. Also note it keeps track of which hosts/ports have been
opened since hte last scan in $HOME/host-db.txt

