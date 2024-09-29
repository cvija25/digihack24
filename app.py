import subprocess
import numpy as np
from numpy.linalg import norm
from numpy import cross, dot
import time

def check_wifi_signal(ssids):
    # Rescan for available Wi-Fi networks using the specified command
    result = subprocess.run(
        ["nmcli", "-f", "SSID,SIGNAL", "device", "wifi", "list", "--rescan", "yes"],
        capture_output=True,
        text=True
    )
    
    # Initialize list to store signal strengths
    signal_strengths = []
    
    # Parse the result and extract SSID and signal values
    for line in result.stdout.splitlines()[1:]:  # Skip the header line
        columns = line.split()
        ssid = ' '.join(columns[:-1])  # Join everything but the last column for SSID (handles multi-word SSIDs)
        signal = columns[-1]           # Last column is the signal strength

        if ssid in ssids:              # If SSID matches one in the desired list
            signal_strengths.append(int(signal))
    
    return signal_strengths

def get_distance(signal_strength):
    # Example function to convert signal strength (RSSI) to approximate distance
    # return 10 - signal_strength / 10
    return 10**(((25-signal_strength))/(10*3))*100

# def trilaterate(pointA, d1, pointB, d2, pointC, d3):
#     x1, y1 = pointA
#     x2, y2 = pointB
#     x3, y3 = pointC

#     # Use equations derived from the distance formulas
#     A = np.array([[2*(x2-x1), 2*(y2-y1)], [2*(x3-x1), 2*(y3-y1)]])
#     B = np.array([[d1**2 -d2**2 -x1**2+x2**2-y1**2+y2**2], [d1**2 -d3**2 -x1**2+x3**2-y1**2+y3**2]])

#     return np.linalg.solve(A,B)

def trilaterate(P1,r1,P2,r2,P3,r3):    
    P1 = np.array(P1)                  
    P2 = np.array(P2)                  
    P3 = np.array(P3)                  
    temp1 = P2-P1                                        
    e_x = temp1/norm(temp1)                              
    temp2 = P3-P1                                        
    i = dot(e_x,temp2)                                   
    temp3 = temp2 - i*e_x                                
    e_y = temp3/norm(temp3)                              
    e_z = cross(e_x,e_y)                                 
    d = norm(P2-P1)                                      
    j = dot(e_y,temp2)                                   
    x = (r1*r1 - r2*r2 + d*d) / (2*d)                    
    y = (r1*r1 - r3*r3 -2*i*x + i*i + j*j) / (2*j)       
    temp4 = r1*r1 - x*x - y*y                            
    if temp4<0:                                          
        raise Exception("The three spheres do not intersect!")
    z = np.sqrt(temp4)                                      
    p_12_a = P1 + x*e_x + y*e_y + z*e_z                  
    p_12_b = P1 + x*e_x + y*e_y - z*e_z                  
    return p_12_a, p_12_b 


if __name__ == "__main__":
    # Access point locations and SSIDs
    ap_locs = [(0,0), (0, 4), (4.5, 4)]
    ap_ssids = ["djole", "Bogdan's Galaxy S21 FE 5G", "Cvija iPhone"]
    
    # Check for Wi-Fi signals and get RSSI values
    signal_list = check_wifi_signal(ap_ssids)
    
    if len(signal_list) == len(ap_ssids):
        # Map signal strengths to distances
        d1 = get_distance(signal_list[0])
        d2 = get_distance(signal_list[1])
        d3 = get_distance(signal_list[2]+10)
    
        print("Signal strengths:", signal_list)
        print("Distances:", d1, d2, d3)
    
        # Trilateration to determine location
        x, y = trilaterate(ap_locs[0], d1, ap_locs[1], d2, ap_locs[2], d3)
        print("Estimated position:", x, y)
    else:
        print("Not all APs found.")
