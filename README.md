# Linux Health Check Script — Beginner Python Guide

## Your Goal

Build a Python script that checks the health of a Linux system and generates a report.
By the end, you will have learned every Python fundamental you need to move on to
log analyzers and cybersecurity tools.

---

## Part 0 — Setting Up Your Azure Linux VM

### Create the VM

1. Log into the Azure Portal (portal.azure.com)
2. Click **Create a resource** → **Virtual Machine**
3. Choose these settings:
   - **Image:** Ubuntu Server 22.04 LTS or 24.04 LTS
   - **Size:** B1s or B2s (cheap, more than enough)
   - **Authentication:** SSH public key (recommended) or password
   - **Inbound ports:** Allow SSH (port 22)
4. Click **Review + Create** → **Create**
5. Once it deploys, grab the **public IP address** from the VM overview page

### Connect to Your VM

From your local terminal (or PowerShell on Windows):

```bash
ssh yourusername@your-vm-ip-address
```

### Verify Python Is Installed

```bash
python3 --version
```

You should see something like `Python 3.10.x` or `3.12.x`. If so, you are good to go.

### Create Your Project Folder

```bash
mkdir ~/health-check
cd ~/health-check
```

### Your Text Editor — Vim

You will be editing files directly on the VM using `vim`.
Vim is what many sysadmins use daily, so learning it now is extra practice for your career.

To create and edit your script:

```bash
vim health_check.py
```

#### Vim Survival Guide (just these basics to start)

Vim has two main modes:

- **Normal mode** — for navigating and commands (this is what opens first)
- **Insert mode** — for actually typing text

Here is all you need to know right now:

| Action              | Keys                                      |
|---------------------|-------------------------------------------|
| Enter insert mode   | Press `i`                                 |
| Exit insert mode    | Press `Esc`                               |
| Save the file       | Press `Esc`, then type `:w` and hit Enter |
| Quit vim            | Press `Esc`, then type `:q` and hit Enter |
| Save and quit       | Press `Esc`, then type `:wq` and hit Enter|
| Quit without saving | Press `Esc`, then type `:q!` and hit Enter|

Your workflow will be:

1. Open the file: `vim health_check.py`
2. Press `i` to start typing
3. Write your code
4. Press `Esc` when done typing
5. Type `:wq` and press Enter to save and exit

Do not worry about learning all of vim right now. These basics are enough.
You will naturally pick up more commands as you use it.

To run your script at any time:

```bash
python3 health_check.py
```

---

## Part 1 — Print a Header and Timestamp

### What you will learn

- print() function
- Importing a module
- Variables
- Strings

### What to write

Open your script file:

```bash
vim health_check.py
```

Press `i` to enter insert mode, then type this code:

```python
# health_check.py — Linux Health Check Script
# This is your first Python project

# 'import' loads extra tools into your script
# 'datetime' lets us work with dates and times
import datetime

# Get the current date and time, store it in a variable
now = datetime.datetime.now()

# Print a header for our report
print("=" * 50)
print("    LINUX HEALTH CHECK REPORT")
print("=" * 50)
print(f"Report generated: {now}")
print("")
```

### Run it

```bash
python3 health_check.py
```

### What just happened — line by line

- `import datetime` — You loaded Python's built-in date/time toolkit
- `now = datetime.datetime.now()` — You created a **variable** called `now` and stored the current time in it
- `print()` — Displays text to the screen
- `"=" * 50` — Repeats the `=` character 50 times (Python lets you multiply strings)
- `f"Report generated: {now}"` — This is an **f-string**, it lets you put variables inside curly braces within text

### Key concepts to understand before moving on

- A **variable** is just a name that holds a value: `now` holds the timestamp
- A **string** is text wrapped in quotes: `"hello"`
- A **module** is a collection of tools someone already wrote for you
- `import` is how you load those tools

---

## Part 2 — Show the Hostname

### What you will learn

- The `os` module (interacting with the operating system)
- Using module functions

### Add this below your existing code

```python
import os

# Get the hostname of this machine
hostname = os.uname().nodename

print(f"Hostname: {hostname}")
print("")
```

### Run it

```bash
python3 health_check.py
```

### What just happened

- `import os` — Loads Python's operating system module
- `os.uname()` — Gets system info (like running `uname` in the terminal)
- `.nodename` — Pulls out just the hostname from that info
- You stored it in a variable and printed it

### Tip

Move your `import os` line to the top of the file, next to `import datetime`.
It is standard practice to put all imports at the very top.

Your file should now start like this:

```python
import datetime
import os
```

---

## Part 3 — Check Disk Usage

### What you will learn

- The `subprocess` module (running Linux commands from Python)
- Capturing command output
- Working with the output as text

### Add this to your script

```python
import subprocess

print("--- DISK USAGE ---")

# subprocess.run() executes a Linux command
# capture_output=True saves the result instead of just printing it
# text=True gives us a normal string instead of raw bytes
result = subprocess.run(["df", "-h"], capture_output=True, text=True)

# result.stdout contains whatever the command printed
print(result.stdout)
```

### Run it

```bash
python3 health_check.py
```

### What just happened

- `subprocess.run()` is like typing a command in the terminal, but from Python
- `["df", "-h"]` — The command and its flags go in a **list** (square brackets)
- `capture_output=True` — Catches the output so we can use it in Python
- `text=True` — Converts the output to a readable string
- `result.stdout` — The actual text output of the command

### Important concept: Lists

`["df", "-h"]` is a **list**. Lists hold multiple items in order.
You will use lists constantly in Python. More on them soon.

---

## Part 4 — Check Memory Usage

### What you will learn

- Repetition and practice (this is how you build confidence)
- Running a different command with subprocess

### Add this to your script

```python
print("--- MEMORY USAGE ---")

result = subprocess.run(["free", "-h"], capture_output=True, text=True)
print(result.stdout)
```

### Run it

Notice this is almost identical to the disk check. You just changed the command.
That is normal. A lot of scripting is the same pattern with small changes.

---

## Part 5 — Check CPU Load

### Add this to your script

```python
print("--- CPU LOAD ---")

# Read the system load average from a special Linux file
# This file always exists on Linux and contains load info
with open("/proc/loadavg", "r") as f:
    load = f.read()

print(f"Load average: {load}")
```

### What you will learn

- Reading files with Python
- The `with open()` pattern
- The special `/proc` filesystem on Linux

### What just happened

- `open("/proc/loadavg", "r")` — Opens the file in **read** mode
- `with ... as f:` — This safely opens the file and automatically closes it when done
- `f.read()` — Reads the entire contents of the file into a string
- `/proc/loadavg` is a special Linux file that always has the current CPU load

### Why this matters

Reading files is one of the most important Python skills for your career path.
Log analysis, config auditing, and security scanning all revolve around reading files.

---

## Part 6 — Check System Uptime

### Add this to your script

```python
print("--- UPTIME ---")

result = subprocess.run(["uptime", "-p"], capture_output=True, text=True)
print(result.stdout)
```

Nothing new here, just more practice with subprocess.

---

## Part 7 — Check for Failed Services (systemd)

### Add this to your script

```python
print("--- FAILED SERVICES ---")

result = subprocess.run(
    ["systemctl", "list-units", "--failed", "--no-legend"],
    capture_output=True,
    text=True
)

if result.stdout.strip() == "":
    print("No failed services. All good!")
else:
    print(result.stdout)

print("")
```

### What you will learn

- **if/else statements** — Making decisions in code
- `.strip()` — Removing extra whitespace from strings

### What just happened

- We ran `systemctl list-units --failed` to find broken services
- `.strip()` removes blank spaces and newlines from the edges of text
- `if result.stdout.strip() == ""` checks if the output is empty
- If empty → no failed services, print a good message
- `else` → something failed, print what it is

### Key concept: if/else

```python
if some_condition:
    # do this
else:
    # do that
```

Python uses **indentation** (4 spaces) to know what code belongs inside each block.
This is different from many other languages. Indentation matters in Python.

---

## Part 8 — Add Disk Usage Warnings with Loops

This is where your script gets smarter.

### What you will learn

- **for loops** — Repeating actions for each item in a collection
- **Splitting strings** into pieces
- **Conditional logic** inside loops

### Replace your old disk usage section with this

```python
print("--- DISK USAGE ---")

result = subprocess.run(["df", "-h"], capture_output=True, text=True)

# Split the output into individual lines
lines = result.stdout.strip().split("\n")

# Print the header line (first line of df output)
print(lines[0])
print("-" * 60)

# Loop through each line AFTER the header
for line in lines[1:]:
    print(line)

    # Split the line into columns
    columns = line.split()

    # The 5th column (index 4) is the usage percentage
    # We remove the '%' sign and convert to a number
    try:
        usage = int(columns[4].replace("%", ""))
        if usage > 80:
            print(f"  *** WARNING: {columns[5]} is {usage}% full! ***")
    except (IndexError, ValueError):
        # Skip lines that do not have the expected format
        pass

print("")
```

### What just happened — this is a big step, take it slow

- `split("\n")` — Splits a big string into a **list** of lines
- `lines[0]` — Gets the first item in the list (Python counts from 0)
- `lines[1:]` — Gets everything AFTER the first item (a **slice**)
- `for line in lines[1:]:` — A **for loop** that goes through each line one at a time
- `line.split()` — Splits a line by whitespace into a list of words/columns
- `columns[4]` — Gets the 5th column (remember, Python counts from 0)
- `int()` — Converts a string to a number
- `.replace("%", "")` — Removes the percent sign so we can compare numbers

### Key concept: for loops

```python
for item in some_list:
    # do something with item
```

The loop runs once for each item. The variable `item` changes each time.

### Key concept: try/except

```python
try:
    # try to do something risky
except SomeError:
    # if it fails, do this instead
    pass  # 'pass' means "do nothing, just keep going"
```

This prevents your script from crashing if a line has unexpected formatting.

---

## Part 9 — Organize with Functions

Right now your script is one long sequence. Functions let you organize it into
named, reusable blocks.

### What you will learn

- **Defining functions** with `def`
- **Calling functions**
- Why functions make code easier to read and maintain

### Rewrite your script using functions

Here is the full restructured version of everything so far:

```python
#!/usr/bin/env python3
"""Linux Health Check Script — Your First Python Project"""

import datetime
import os
import subprocess


def print_header():
    """Print the report title and timestamp."""
    now = datetime.datetime.now()
    print("=" * 50)
    print("    LINUX HEALTH CHECK REPORT")
    print("=" * 50)
    print(f"Report generated: {now}")
    print(f"Hostname: {os.uname().nodename}")
    print("")


def check_disk_usage():
    """Check disk usage and warn if any partition is over 80%."""
    print("--- DISK USAGE ---")
    result = subprocess.run(["df", "-h"], capture_output=True, text=True)
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
    result = subprocess.run(["free", "-h"], capture_output=True, text=True)
    print(result.stdout)


def check_cpu_load():
    """Display CPU load average."""
    print("--- CPU LOAD ---")
    with open("/proc/loadavg", "r") as f:
        load = f.read()
    print(f"Load average: {load}")


def check_uptime():
    """Display system uptime."""
    print("--- UPTIME ---")
    result = subprocess.run(["uptime", "-p"], capture_output=True, text=True)
    print(result.stdout)


def check_failed_services():
    """Check for any failed systemd services."""
    print("--- FAILED SERVICES ---")
    result = subprocess.run(
        ["systemctl", "list-units", "--failed", "--no-legend"],
        capture_output=True,
        text=True,
    )
    if result.stdout.strip() == "":
        print("No failed services. All good!")
    else:
        print(result.stdout)
    print("")


# ---- Main execution ----
# This is where the script actually runs
# It calls each function in order

print_header()
check_disk_usage()
check_memory()
check_cpu_load()
check_uptime()
check_failed_services()

print("=" * 50)
print("    END OF REPORT")
print("=" * 50)
```

### What just happened

- `def function_name():` — Creates a named block of code
- The code inside the function only runs when you **call** it by name
- At the bottom, we call each function in order
- Now you can easily rearrange, add, or remove checks
- Each function has a **docstring** (the text in triple quotes) explaining what it does

### Why this matters

Every professional Python script uses functions. When your script is 200+ lines long,
functions keep it readable. Interviewers and hiring managers will look for this.

---

## Part 10 — Save the Report to a File

### What you will learn

- **Writing to files**
- Redirecting print output
- **Dictionaries** — a new data structure

### Add this function and modify main execution

```python
def save_report(filename="health_report.txt"):
    """Run all checks and save output to a file."""
    import io
    import sys

    # Capture all print output
    captured = io.StringIO()
    original_stdout = sys.stdout
    sys.stdout = captured

    # Run all checks (they will print to our captured buffer)
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


# ---- Main execution ----
save_report()
```

### Run it

```bash
python3 health_check.py
```

Then check that the file was created:

```bash
cat health_report.txt
```

---

## Part 11 — Add a Command-Line Flag

### What you will learn

- **argparse** — Letting users pass options to your script
- Running your script with flags like `--output report.txt` or `--verbose`

### Add argparse to your script

Replace the main execution section at the bottom with:

```python
import argparse


def main():
    """Parse arguments and run the health check."""
    parser = argparse.ArgumentParser(
        description="Linux Health Check Script"
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

    save_report(filename=args.output)


# This is the standard Python way to run the main function
# It means: only run this if the script is executed directly
if __name__ == "__main__":
    main()
```

### Now you can run it like this

```bash
# Default behavior
python3 health_check.py

# Save to a custom filename
python3 health_check.py -o my_report.txt

# See the help message
python3 health_check.py --help
```

### What just happened

- `argparse` creates a professional command-line interface for your script
- `-o` / `--output` lets the user choose the output filename
- `-v` / `--verbose` is a boolean flag (on or off)
- `if __name__ == "__main__":` is a Python convention — it means "run main() only when this script is executed directly, not when it is imported as a module"

---

## Part 12 — Add Logging

### What you will learn

- The `logging` module — professional way to track what your script is doing
- Different log levels (INFO, WARNING, ERROR)

### Add this near the top of your script, after your imports

```python
import logging

logging.basicConfig(
    filename="health_check.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
```

### Then sprinkle log messages into your functions

For example, in `check_disk_usage()`, add:

```python
logging.info("Checking disk usage")

# And inside the warning condition:
if usage > 80:
    logging.warning(f"{columns[5]} is {usage}% full")
```

In `check_failed_services()`:

```python
logging.info("Checking for failed services")

if result.stdout.strip() == "":
    logging.info("No failed services found")
else:
    logging.warning(f"Failed services detected: {result.stdout.strip()}")
```

### After running your script, check the log

```bash
cat health_check.log
```

This gives you a timestamped history of every run, which is exactly
what real sysadmin tools do.

---

## What You Have Learned

By completing this project, you now know:

| Concept                | Where you used it                   |
|------------------------|-------------------------------------|
| Variables              | Storing hostname, timestamps, etc.  |
| Strings and f-strings  | Building output messages            |
| Lists                  | Splitting command output into lines |
| Loops (for)            | Going through disk partitions       |
| if/else                | Disk warnings, failed services      |
| Functions              | Organizing every check              |
| File reading           | /proc/loadavg                       |
| File writing           | Saving the report                   |
| Importing modules      | os, subprocess, datetime, etc.      |
| subprocess             | Running Linux commands from Python  |
| try/except             | Handling unexpected data            |
| argparse               | Command-line flags                  |
| logging                | Professional audit trail            |

---

## What To Do Next

1. **Push this to GitHub.** Create a repo called `linux-health-check`. This is your first portfolio piece.
2. **Add a README.md** explaining what the script does and how to run it.
3. **Start Project 2: SSH/Auth Log Analyzer.** You now have the skills for it:
   file reading, string splitting, loops, and pattern matching.

---

## Quick Reference — Useful Commands on Your VM

```bash
# Run your script
python3 health_check.py

# Run with custom output file
python3 health_check.py -o report.txt

# View your saved report
cat health_report.txt

# View your log file
cat health_check.log

# Check Python version
python3 --version

# Install a Python package later when you need one
pip3 install requests
```

---

## Troubleshooting

**"python3: command not found"**
Run: `sudo apt update && sudo apt install python3 -y`

**"Permission denied" when running systemctl**
Some systemctl commands need sudo. You can run:
`sudo python3 health_check.py`
Or adjust the script to handle the permission error gracefully with try/except.

**Indentation errors**
Python is very strict about indentation. Use exactly 4 spaces per level.
In vim, you can add this to your vim config to make it easier:
`echo "set tabstop=4 shiftwidth=4 expandtab" >> ~/.vimrc`
This makes the Tab key insert 4 spaces instead of a tab character.
