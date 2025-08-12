#  System Health Check Script

A simple Bash script that performs basic system health checks and logs the results to a file with a timestamp.

## Features

- Displays:
  - Current system date and time
  - System uptime
  - CPU load
  - Memory usage
  - Disk usage
  - Top 5 memory-consuming processes
- Checks the status of services passed as command-line arguments
- Logs all output to `healthlog.txt` with a timestamp

## 📜 Script: `healthcheck.sh`

This script collects system health information and optionally checks if specific services are running.

###  Requirements

- Linux system with `bash` shell
- Permissions to run system commands like `systemctl`, `ps`, etc.

## 🚀 How to Use

### 1. Make the script executable:

```bash
chmod +x healthcheck.sh
```

## 2. Run the Script

You can specify any number of services (e.g., `nginx`, `ssh`, `mysql`, `docker`) as arguments:

```bash
./healthcheck.sh nginx ssh mysql
```

