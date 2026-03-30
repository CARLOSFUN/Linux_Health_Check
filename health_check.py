#!/usr/bin/env python3

"""Linux Health Check Script"""

import datetime
import os 
import subprocess
import io
import sys
import argparse
import logging



# Set up logging - writes to a log file with timestamps
logging.basicConfig(
    filename="health_check.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def print_header():
    """Print the report title and timestamp."""
    now = datetime.datetime.now()
    print("=" * 50)
    print("    LINUX HEALTH CHECK REPORT")
    print("=" * 50)
    print(f"Report generated: {now}")
    print(f"Hostname: {os.uname().nodename}")
    print("")
    logging.info("Health check started")

def check_disk_usage():
 
    """Check disk usage and warn if any partition is over 80%"""                            
    print("--- DISK USAGE ---")
    result  =subprocess.run(["df", "-h"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")

    print(lines[0])
    print("-" * 60)

    for line in lines[1:]:
        print(line)
        columns = line.split()
        try:
            usage = int(columns[4].replace("%", ""))
            if usage > 80:
                print(f"  *** WARNING: {columns[5]} is {usage}% full! ***")
        except (IndexError, ValueError):
            pass

    print("")


def check_memory():
    """Display memory usage."""
    print("--- MEMORY USAGE ---")
    try:
        result = subprocess.run(["free", "-h"], capture_output=True, text=True)
        print(result.stdout)
    except FileNotFoundError:
        print("Could not check memory - 'free' command not found")
        logging.error("'free' command not available")


def check_cpu_load():
    """Display CPU load average."""
    print("--- CPU load ---")
    try:
        with open("/proc/loadavg", "r") as f:
            load = f.read()
        print(f"load average: {load}")
    except FileNotFoundError:
        print("Could not reat CPU load")
        logging.error("Failed to read /proc/loadavg")


def check_uptime():
    """Display system uptime"""
    print("--- UPTIME ---")
    try:
        result = subprocess.run(["uptime", "-p"], capture_output=True, text=True)
        print(result.stdout)
    except FileNotFoundError:
        print("Could not check uptime - 'uptime' command not found")
        logging.error("'uptime' command not available")

    


def check_failed_services():
    """Check for any failed systemd servides"""
    print("--- Failed Services ---")
    try:
        result = subprocess.run(["systemctl", "list-units", "--failed", "--no legend"], capture_output=True, text=True)
        if result.stdout.strip() == "":
            print("No failed services. All good!")
            logging.info("No failed services found")
        else:
            print(result.stdout)
        logging.warning(f"Failed services detected: {result.stdout.strip()}")
    except FileNotFoundError:
        print("Could not check services - 'systmectl' not available")
        logging.error("'systemctl' command not available")


def save_report(filename="health_report.txt"):
    """Run all check and save output to a file."""

    captured = io.StringIO()
    original_stdout = sys.stdout
    sys.stdout = captured
    

    print_header()
    check_disk_usage()
    check_memory()
    check_cpu_load()
    check_uptime()
    check_failed_services()
    print("=" * 50)
    print("    END OF REPORT")
    print("=" * 50)


 # Restore normal printing
    sys.stdout = original_stdout
    report_text = captured.getvalue()

    # Print to screen
    print(report_text)

    # Also save to file
    with open(filename, "w") as f:
        f.write(report_text)

    print(f"\nReport saved to: {filename}")
    logging.info(f"Report saved to {filename}")


def main():
    """Parse arguments and run the health check."""
    parser = argparse.ArgumentParser(
        description="linux health check script"
    )
    parser.add_argument(
        "-o", "--output",
        help="Save report to this filename",
        default="health_report.txt",
    )
    parser.add_argument(
        "-v", "--verbose",
        help="Show extra detail",
        action="store_true",
    )

    args = parser.parse_args()

    if args.verbose:
        print("[verbose mode enabled]")
        logging.info("Verbose mode enabled")

    save_report(filename=args.output)

# This means: only run main() when the script is executed directly 
if __name__ == "__main__":
    main()
