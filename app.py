import subprocess
import numpy as np
from numpy.linalg import norm
from numpy import cross, dot
from config import ap_locs, ap_ssids

def check_wifi_signal(ssids):
    result = subprocess.run(
        ["nmcli", "-f", "SSID,SIGNAL", "device", "wifi", "list", "--rescan", "yes"],
        capture_output=True,
        text=True
    )
    
    signal_strengths = []
    
    for line in result.stdout.splitlines()[1:]:
        columns = line.split()
        ssid = ' '.join(columns[:-1])
        signal = columns[-1]

        if ssid in ssids:
            signal_strengths.append(int(signal))
    
    return signal_strengths

def get_distance(signal_strength):
    return 10**(((25-signal_strength))/(10*3))*100

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
    
    signal_list = check_wifi_signal(ap_ssids)
    
    if len(signal_list) == len(ap_ssids):
        d1 = get_distance(signal_list[0])
        d2 = get_distance(signal_list[1])
        d3 = get_distance(signal_list[2]+10)
    
        print("Signal strengths:", signal_list)
        print("Distances:", d1, d2, d3)
    
        x, y = trilaterate(ap_locs[0], d1, ap_locs[1], d2, ap_locs[2], d3)
        print("Estimated position:", x, y)
    else:
        print("Not all APs found.")
