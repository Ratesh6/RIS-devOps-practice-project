#!/bin/bash

# Set log file name with timestamp
LOGFILE="healthlog.txt"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "===================================" >> $LOGFILE
echo "Health Check - $TIMESTAMP" >> $LOGFILE
echo "===================================" >> $LOGFILE

# System Date and Time
echo "System Date and Time:" >> $LOGFILE
date >> $LOGFILE
echo "" >> $LOGFILE

# Uptime
echo "System Uptime:" >> $LOGFILE
uptime >> $LOGFILE
echo "" >> $LOGFILE

# CPU Load
echo "CPU Load:" >> $LOGFILE
uptime | awk -F'load average:' '{ print $2 }' >> $LOGFILE
echo "" >> $LOGFILE

# Memory Usage
echo "Memory Usage (in MB):" >> $LOGFILE
free -m >> $LOGFILE
echo "" >> $LOGFILE

# Disk Usage
echo "Disk Usage:" >> $LOGFILE
df -h >> $LOGFILE
echo "" >> $LOGFILE

# Top 5 Memory-Consuming Processes
echo "Top 5 Memory-Consuming Processes:" >> $LOGFILE
ps aux --sort=-%mem | head -n 6 >> $LOGFILE
echo "" >> $LOGFILE

# Check Services (from command-line arguments)
if [ "$#" -eq 0 ]; then
    echo "No services were specified to check." >> $LOGFILE
else
    echo "Service Status:" >> $LOGFILE
    for SERVICE in "$@"; do
        STATUS=$(systemctl is-active $SERVICE 2>/dev/null)
        if [ "$STATUS" == "active" ]; then
            echo "$SERVICE: running" >> $LOGFILE
        elif [ "$STATUS" == "inactive" ]; then
            echo "$SERVICE: not running" >> $LOGFILE
        elif [ "$STATUS" == "unknown" ]; then
            echo "$SERVICE: unknown service" >> $LOGFILE
        else
            echo "$SERVICE: $STATUS" >> $LOGFILE
        fi
    done
fi

echo "" >> $LOGFILE
echo "Health check complete." >> $LOGFILE
echo "" >> $LOGFILE
