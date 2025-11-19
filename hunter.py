#!/usr/bin/env python3
import paramiko
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# --- CONFIGURATION ---
TARGET_IP = "192.168.100.128"  # Your Ubuntu VM IP
USERNAME = "student"
PASSWORD = "student123"

# Known binaries that can allow privilege escalation if SUID is set
# Based on GTFOBins project
GTFOBINS_LIST = [
    "cp", "find", "nano", "vim", "awk", "less", "nmap", "bash", "python", "man","my_cp"
]

class EscalationHunter:
    def __init__(self, ip, user, password):
        """Initialize the scanner with target credentials."""
        self.ip = ip
        self.user = user
        self.password = password
        self.client = None

    def connect(self):
        """Establishes SSH connection to the target."""
        print(f"{Fore.CYAN}[*] Connecting to {self.ip} via SSH...")
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.ip, username=self.user, password=self.password)
            print(f"{Fore.GREEN}[+] Connection successful!\n")
            return True
        except Exception as e:
            print(f"{Fore.RED}[-] Connection failed: {e}")
            return False

    def disconnect(self):
        """Closes the SSH connection."""
        if self.client:
            self.client.close()
            print(f"{Fore.CYAN}[*] Connection closed.")

    def scan_suid(self):
        """
        Logic:
        1. Search for all files with SUID bit set.
        2. Compare filenames against the GTFOBins list.
        3. Alert if a match is found.
        """
        print(f"{Fore.YELLOW}[INFO] Starting SUID Vulnerability Scan...")
        
        # Command explanation:
        # find /       -> Search from root directory
        # -perm -u=s   -> Look for files with SUID bit set
        # -type f      -> Look for files only (not directories)
        # 2>/dev/null  -> Discard error messages (permission denied errors)
        command = "find / -perm -u=s -type f 2>/dev/null"
        
        try:
            # Execute the command on the remote server
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode().strip()
            
            if not output:
                print(f"{Fore.WHITE}[-] No SUID files found (unexpected).")
                return

            suid_files = output.splitlines()
            vulnerabilities_found = 0

            for file_path in suid_files:
                # Extract binary name (e.g., '/usr/bin/find' -> 'find')
                binary_name = file_path.split("/")[-1]

                # CHECK: Is this binary in our danger list?
                if binary_name in GTFOBINS_LIST:
                    print(f"{Fore.RED}[!!!] CRITICAL VULNERABILITY FOUND: {file_path}")
                    print(f"{Fore.RED}      Reason: '{binary_name}' is a known GTFOBin and has SUID set.")
                    vulnerabilities_found += 1
                else:
                    # Optional: Print safe SUID files in grey/white
                    # print(f"{Fore.WHITE}[~] Found standard SUID file: {file_path}")
                    pass

            if vulnerabilities_found == 0:
                print(f"{Fore.GREEN}[V] No obvious GTFOBins vulnerabilities found in SUID scan.")
            else:
                print(f"\n{Fore.RED}[!] Total critical files found: {vulnerabilities_found}")

        except Exception as e:
            print(f"{Fore.RED}[-] Error during SUID scan: {e}")

    def run(self):
        """Main execution flow."""
        if self.connect():
            self.scan_suid()
            self.disconnect()

if __name__ == "__main__":
    print(f"{Fore.MAGENTA}--- 🕵️  ESCALATION HUNTER v1.0 🕵️  ---")
    
    # Create an instance of the hunter and run it
    hunter = EscalationHunter(TARGET_IP, USERNAME, PASSWORD)
    hunter.run()
