# Linux Health Check Script

A Python script that checks the health of a Linux system and generates a report. Built as a hands-on project to learn Python for system administration and cybersecurity.

## What It Checks
- Disk usage (warns if any partition is over 80%)
- Memory usage
- CPU load average
- System uptime
- Failed systemd services

## How To Run
```
python3 health_check.py
```

## Options
- `-o filename` — save report to a custom file
- `-v` — enable verbose mode
- `--help` — show all options

## Example
```
python3 health_check.py -v -o my_report.txt
```

## Features
- Saves report to a text file
- Logs all checks to health_check.log with timestamps
- Error handling so the script won't crash on unexpected input

## Built With
- Python 3
- Standard library only (no external packages)
