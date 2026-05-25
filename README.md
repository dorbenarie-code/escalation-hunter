# 🕵️ Escalation Hunter

**Version:** 4.0 (Production Ready)  
**Language:** Python 3  
**Focus:** Linux Privilege Escalation & Post-Exploitation  

## 📖 Project Overview

**Escalation Hunter** is an automated cybersecurity tool designed to detect Privilege Escalation vectors in Linux environments. Unlike standard exploit suggesters that rely solely on kernel version matching, this tool actively hunts for logic-based misconfigurations and dangerous permissions.

The tool operates remotely from an attacker machine, such as Kali Linux, connects via SSH to the target, and performs a comprehensive audit based on industry-standard methodologies such as GTFOBins.

## ⚡ Key Features

- **Remote Auditing:** Uses `paramiko` to manage secure SSH connections without requiring agent installation on the target.
- **SUID Scanner:** Scans the filesystem for SUID binaries and cross-references them with a known database of dangerous binaries, such as GTFOBins.
- **Sudo Rights Analysis:** Detects dangerous `sudo` permissions, including password injection handling, and identifies binaries that can spawn root shells.
- **Cron Job Hunter:** Analyzes `/etc/crontab` to identify root-owned tasks that are writable by unprivileged users.
- **Reporting:** Generates dual output — a colored console display for real-time analysis and a clean text report for documentation.
- **CLI Architecture:** Built with `argparse` for a flexible command-line interface experience.

## 🏗️ Lab Environment

The project was developed and tested in an isolated virtual environment:

- **Attacker:** Kali Linux running the scanner.
- **Target:** Ubuntu Server 22.04 with a hardened configuration and intentional vulnerabilities planted for testing.

### Planted Vulnerabilities (POC)

To validate the tool's logic, the following vectors were implemented in the lab:

- [x] **SUID Binary:** A custom copy of `cp`, named `my_cp`, with the SUID bit set.
- [x] **Sudo Misconfiguration:** The user `student` is allowed to run `find` as root.
- [x] **Insecure Cron Job:** A root-owned script, `backup.sh`, is world-writable.

## 🚀 Installation & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/dorbenarie-code/escalation-hunter.git
cd escalation-hunter
```

### 2. Install Dependencies

```bash
pip install paramiko colorama
```

### 3. Run the Scanner

You can run the tool by providing the target IP and credentials via CLI arguments:

```bash
# Basic Run
./hunter.py -t 192.168.100.128 -u student -p student123

# Run and Save Report
./hunter.py -t 192.168.100.128 -u student -p student123 -o report.txt
```

## Arguments

| Argument | Description |
| :--- | :--- |
| `-t`, `--target` | Target IP address |
| `-u`, `--user` | SSH username |
| `-p`, `--password` | SSH password |
| `-o`, `--output` | Optional: save the report to a file |

## 📸 Example Output

Below is an actual execution log from the test environment using version 4.0:

```text
   🕵️   ESCALATION HUNTER v4.0
   ---------------------------
   Automated Privilege Escalation Scanner


[*] Connecting to 192.168.100.128 as student...
[+] Connection established successfully.

[*] --- Starting SUID Audit ---
[!!!] CRITICAL SUID: /home/student/my_cp (Matches GTFOBins)
----------------------------------------

[*] --- Starting Sudo Rights Audit ---
[!!!] CRITICAL Sudo: /usr/bin/find (Matches GTFOBins)
----------------------------------------

[*] --- Starting Cron Jobs Audit ---
[!!!] CRITICAL CRON: /usr/local/bin/backup.sh
[*] Reason: Running as root & Writable by user
[*] Evidence: -rwxrwxrwx 1 root root 28 Nov 18 14:47 /usr/local/bin/backup.sh

[*] SSH session closed.
```

## ⚖️ Disclaimer

This tool is intended for **educational purposes and authorized security testing only**. Using this tool on systems without permission is illegal.
