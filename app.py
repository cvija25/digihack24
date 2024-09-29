import subprocess
import numpy as np
import time

def check_wifi_signal(bssids):
    # Rescan for available i-Fi networks using the specified command
    result = subprocess.run(
        ["nmcli", "-f", "bssid,signal", "device", "wifi", "list", "--rescan", "yes"],
        capture_output=True,
        text=True
    )
    # Split the output into lines
    # lines = result.stdout.splitlines()
    # signal_found = False
    lista = []
    for s in result.stdout.split('\n')[2:]:
        list_s = s.split(' ')
        # print(list_s[0])
        if list_s[0] in bssids:
            # print("usao")
            lista.append(int(list_s[2]))
    return lista
            

def get_distance(q):
    return 10 - q/10

def trilaterate(pointA, d1, pointB, d2, pointC, d3):
    x1, y1 = pointA
    x2, y2 = pointB
    x3, y3 = pointC

    # Use equations derived from the distance formulas
    A = np.array([[2*(x2-x1), 2*(y2-y1)], [2*(x3-x1), 2*(y3-y1)]])
    B = np.array([[d1**2 -d2**2 -x1**2+x2**2-y1**2+y2**2], [d1**2 -d3**2 -x1**2+x3**2-y1**2+y3**2]])

    return np.linalg.solve(A,B)

if __name__ == "__main__":
    ap_locs = [(7.5,6),(12.5,7), (8.75,0)]
    ap_bssids = ["30:FD:65:31:63:B0", "30:FD:65:31:7C:D1", "30:FD:65:31:63:B0"]
    #print(trilaterate(ap_locs[0],5,ap_locs[1],6,ap_locs[2],4))
    while True:
        lista = check_wifi_signal(ap_bssids) 
        rssi1 = lista[0]
        print(rssi1)
        d1 = get_distance(rssi1)

        rssi2 = lista[1]
        d2 = get_distance(rssi2)

        rssi3 = lista[2]
        d3 = get_distance(rssi3)
        # print("rssis",rssi1,rssi2,rssi3)
        # print("ds",d1,d2,d3)
        print("-----------------")
        x, y = trilaterate(ap_locs[0],d1,ap_locs[1],d2,ap_locs[2],d3)
        print(x,y)