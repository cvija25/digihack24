import subprocess
import time

def check_wifi_signal(bssid):
    while True:
        # Rescan for available Wi-Fi networks
 
        # Get the list of available Wi-Fi networks using the specified command
        result = subprocess.run(
            ["nmcli", "-f", "bssid,signal", "device", "wifi", "list", "--rescan", "yes"],
            capture_output=True,
            text=True
        )

        # Split the output into lines
        # lines = result.stdout.splitlines()
        # signal_found = False
        for s in result.stdout.split('\n')[2:]:
            list_s = s.split(' ')
            if list_s[0] == bssid:
                print(list_s[2])

        # for line in lines:
        #     if line:  # Check if the line is not empty
        #         parts = line.split(':')  # Split by tab character
        #         ssid = parts[0]  # The SSID is the first element
        #         signal_strength = parts[1]  # The signal strength is the third element

        #         # Check if the SSID matches the target SSID
        #         if ssid == target_ssid:
        #             print(signal_strength)
        #             signal_found = True
        #             break  # Exit loop once the target SSID is found

        # if not signal_found:
        #     print("SSID not found.")

        # Wait for 1 second before rescanning

if __name__ == "__main__":
    check_wifi_signal("30:FD:65:31:7C:C1")
