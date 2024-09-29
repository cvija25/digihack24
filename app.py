import subprocess
import numpy as np

def get_signal_strength(bssid):
    try:
        # Run the command to dump station information for the specified BSSID
        result = subprocess.run(
            ['sudo', 'iw', 'dev', 'wlp2s0', 'station', 'dump', bssid],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            # Process the output
            for line in result.stdout.splitlines():
                if "signal:" in line:  # Look for the signal line
                    signal_strength = line.split()[1]  # Get the signal value
                    return int(signal_strength)
            return f"BSSID {bssid} not found or no signal information."
        else:
            return f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"An error occurred: {e}"

def get_distance(rssi):
    A = -40
    n = 4
    return 10**((A-rssi)/(10*n))

def trilaterate(pointA, distanceA, pointB, distanceB, pointC, distanceC):
    x1, y1 = pointA
    x2, y2 = pointB
    x3, y3 = pointC

    # Use equations derived from the distance formulas
    A = 2 * (x2 - x1)
    B = 2 * (y2 - y1)
    D = 2 * (x3 - x1)
    E = 2 * (y3 - y1)

    # The equations will lead us to a system of equations to solve for x and y
    # First equation
    C1 = distanceA**2 - distanceB**2 - x1**2 + x2**2 - y1**2 + y2**2
    # Second equation
    C2 = distanceA**2 - distanceC**2 - x1**2 + x3**2 - y1**2 + y3**2

    # Now we can rearrange to find y
    # From the first equation
    y = (C1 - A * x1) / B
    # From the second equation
    y2 = (C2 - D * x1) / E
    
    # Solve for x using the derived y values in either equation
    x1_solution = np.sqrt(distanceA**2 - (y - y1)**2) + x1
    x2_solution = np.sqrt(distanceA**2 - (y2 - y1)**2) + x1

    return (x1_solution, y)
if __name__ == "__main__":
    ap_locs = [(3/7,0.5),(5/7,0.7), (0.5,0)]
    ap_bssids = ["30:fd:65:31:7c:c1", "30:fd:65:31:63:a1", "72:18:1a:bc:8d:42"]
    while True:
        rssi1 = get_signal_strength(ap_bssids[0]) 
        d1 = get_distance(rssi1)

        rssi2 = get_signal_strength(ap_bssids[1])
        d2 = get_distance(rssi2)

        rssi3 = get_signal_strength(ap_bssids[2])
        d3 = get_distance(rssi3)

        x, y = trilaterate(ap_locs[0],d1,ap_locs[1],d2,ap_locs[2],d3)
        print(x,y)
        