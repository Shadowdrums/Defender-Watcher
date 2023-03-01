import time
import subprocess
import os

def get_defender_status():
    # Define the PowerShell command to get Windows Defender status
    powershell_command = 'Get-MpComputerStatus'

    # Run the PowerShell command and capture the output
    result = subprocess.run(['powershell', '-Command', powershell_command], capture_output=True)

    # Check the return code of the PowerShell command to see if it was successful
    if result.returncode != 0:
        print(f"Error running PowerShell command: {result.stderr.decode('utf-8').strip()}")
        return None
    else:
        # Parse the output of the PowerShell command to get the Windows Defender status
        output = result.stdout.decode('utf-8').strip()
        status = {}
        lines = output.split('\n')
        for line in lines:
            parts = line.split(':')
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                status[key] = value

        # Get additional information from the PowerShell command
        status['Real-time protection'] = subprocess.run(['powershell', '-Command', 'Get-MpPreference RealTimeScanDirection'], capture_output=True).stdout.decode('utf-8').strip()
        last_scan_info = subprocess.run(['powershell', '-Command', 'Get-MpComputerStatus | Select-Object -ExpandProperty lastquickscan'], capture_output=True).stdout.decode('utf-8').strip().split(',')
        if len(last_scan_info) == 3:
            status['Last scan date'] = last_scan_info[0].strip()
            status['Items scanned'] = last_scan_info[1].strip()
            status['Items detected'] = last_scan_info[2].strip()
            status['Items quarantined'] = subprocess.run(['powershell', '-Command', 'Get-MpThreatDetection | Select-Object -ExpandProperty QuarantineItems'], capture_output=True).stdout.decode('utf-8').strip()

        return status


if __name__ == "__main__":
    # Define the number of seconds between status checks
    check_interval = 5

    # Take a snapshot of the current defender status on startup and write it to Defender-snapshot.txt
    snapshot = get_defender_status()
    if snapshot is not None:
        with open("Defender-snapshot.txt", "w") as f:
            for key, value in snapshot.items():
                f.write(f"{key}: {value}\n")
                print(f"{key}: {value}")


        # Print out the initial snapshot to the console
        print(f"Initial Windows Defender status:\n{snapshot}\n")

    # Initialize the previous status to None
    prev_status = snapshot

    try:
        with open(os.path.join(os.getcwd(), "Defender.txt"), "a") as f:
            while True:
                # Get the current status of Windows Defender
                status = get_defender_status()

                # If the status has changed, print out a message
                if status is not None and status != prev_status:
                    label = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]"
                    print(label, "Windows Defender status changed:")
                    f.write(label + " Windows Defender status changed:\n")
                    for key, value in status.items():
                        if prev_status is None or status.get(key) != prev_status.get(key):
                            message = f"{key}: {value}"
                            print(label, message)
                            f.write(label + " " + message + "\n")
                    prev_status = status

                # Wait for the check interval before checking again
                time.sleep(check_interval)

    except KeyboardInterrupt:
        pass
