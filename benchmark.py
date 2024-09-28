import subprocess
import time

def rescan_and_get_access_points():
    try:
        # Force a fresh Wi-Fi scan
        subprocess.run(['nmcli', 'dev', 'wifi', 'rescan'], check=True)
        
        # Get the list of available Wi-Fi networks
        result = subprocess.run(['nmcli', '-t', '-f', 'SSID,SIGNAL', 'dev', 'wifi'], 
                                stdout=subprocess.PIPE, text=True)
        
        # Parse the output
        networks = result.stdout.strip().split('\n')
        
        # Print available networks
        for network in networks:
            print(network)
            #print(f"SSID: {ssid}, BSSID: {bssid}, Signal Strength: {signal}%")
    
    except subprocess.CalledProcessError as e:
        print(f"Error during Wi-Fi rescan: {e}")

# Main loop to continuously scan
refresh_interval = 5  # Set the interval in seconds

try:
    while True:
        print("\nRescanning for Wi-Fi networks...\n")
        rescan_and_get_access_points()
        
        # Wait for the specified interval before rescanning
        time.sleep(refresh_interval)

except KeyboardInterrupt:
    print("Scanning interrupted by user.")
