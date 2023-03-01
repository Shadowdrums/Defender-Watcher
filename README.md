# Defender-Watcher
Monitors Windows Defender for changes
This program is a Python script that monitors the status of Windows Defender on a Windows machine. It uses PowerShell commands to get information about the status of Windows Defender, such as whether it is running, when the last scan was performed, and whether any threats were detected.

The program first defines a function called get_defender_status that uses the subprocess module to run PowerShell commands and capture the output. It then parses the output to extract the relevant information about Windows Defender, and returns this information in the form of a dictionary.

The program then uses the get_defender_status function to take a snapshot of the current Windows Defender status when the script is started. It writes this snapshot to a file called "Defender-snapshot.txt" and prints it to the console.

The program then enters an infinite loop, where it repeatedly calls get_defender_status to check the current status of Windows Defender. If the status has changed since the previous check, the program prints a message to the console and writes the message to a file called "Defender.txt". The program also updates the prev_status variable with the current status so that it can compare it with the next status check.

The program uses time.sleep to pause between checks, with the length of the pause specified by the check_interval variable.

The program is designed to run continuously until it is interrupted by a keyboard interrupt (i.e. the user presses Ctrl-C).
