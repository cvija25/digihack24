from access_points import get_scanner
import numpy as np
import time



def signal_quality_to_dbm(signal_quality):
    """
    Convert signal quality percentage (0-100) to dBm.
    
    :param signal_quality: Signal quality as a percentage (0-100)
    :return: Signal strength in dBm
    """
    # Define the mapping for signal quality to dBm
    min_dbm = -90  # Corresponds to 0%
    max_dbm = -30  # Corresponds to 100%

    # Linear interpolation
    dbm = max_dbm + (min_dbm - max_dbm) * (1 - signal_quality / 100.0)
    return dbm

def get_distance(quality):
    A = -40
    n = 4
    rssi = signal_quality_to_dbm(quality)
    return 10**((A-rssi)/(10*n))

def mylocation(access_points, ap_locations):
    signal_qualities = [ap.quality for ap in access_points]
    distances = [get_distance(quality) for quality in signal_qualities]

    p1 = ap_locations[0]
    p2 = ap_locations[1]
    p3 = ap_locations[2]
    # Corresponding distances to the unknown point
    d1 = distances[0]
    d2 = distances[1]
    d3 = distances[2]

    # Solve system of equations derived from:
    # (x - x1)^2 + (y - y1)^2 = d1^2
    # (x - x2)^2 + (y - y2)^2 = d2^2
    # (x - x3)^2 + (y - y3)^2 = d3^2

    # Subtract equations (p2 from p1 and p3 from p1)
    A1 = 2 * (p2[0] - p1[0])
    B1 = 2 * (p2[1] - p1[1])
    C1 = d1**2 - d2**2 - p1[0]**2 + p2[0]**2 - p1[1]**2 + p2[1]**2

    A2 = 2 * (p3[0] - p1[0])
    B2 = 2 * (p3[1] - p1[1])
    C2 = d1**2 - d3**2 - p1[0]**2 + p3[0]**2 - p1[1]**2 + p3[1]**2

    # Solve the linear system of equations
    A = np.array([[A1, B1], [A2, B2]])
    C = np.array([C1, C2])

    # Solve for x, y (your location)
    x, y = np.linalg.solve(A, C)

    return x,y

def get_ap_locations():
    return [[0,1],[1,1],[1,0]]



if __name__ == "__main__":
    wifi = get_scanner()
    while True:
        access_points = wifi.get_access_points()        
        # possible = ["Bogdan's Galaxy S21 FE 5G", "djole", "Cvija iPhone"]
        print([(a.ssid,a.quality) for a in access_points if a.ssid == "IT_Hub"])
        access_points = [a for a in access_points]
        ap_locations = get_ap_locations()
        x, y = mylocation(access_points,ap_locations)
        print(x,y)
        time.sleep(2)
        