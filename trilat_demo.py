import numpy                                             
from numpy import sqrt, dot, cross                       
from numpy.linalg import norm
aps = [(2,2), (8,10), (7,5)]

P = (6,6)

# def trilaterate(pointA, d1, pointB, d2, pointC, d3):
#     x1, y1 = pointA
#     x2, y2 = pointB
#     x3, y3 = pointC

#     # Use equations derived from the distance formulas
#     A = np.array([[2*(x2-x1), 2*(y2-y1)], [2*(x3-x1), 2*(y3-y1)]])
#     B = np.array([[d1**2 -d2**2 -x1**2+x2**2-y1**2+y2**2], [d1**2 -d3**2 -x1**2+x3**2-y1**2+y3**2]])

#     return np.linalg.solve(A,B)

def get_signal(dist):
    return 25 - 10*3*numpy.log(dist)

def trilaterate1(P1,P2,P3,r1,r2,r3):    
    P1 = numpy.array(P1)                  
    P2 = numpy.array(P2)                  
    P3 = numpy.array(P3)                  
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
        raise Exception("The three spheres do not intersect!");
    z = sqrt(temp4)                                      
    p_12_a = P1 + x*e_x + y*e_y + z*e_z                  
    p_12_b = P1 + x*e_x + y*e_y - z*e_z                  
    return p_12_a,p_12_b 

xp, yp = P
x1,y1 = aps[0]
x2,y2 = aps[1]
x3,y3 = aps[2]

d1 = sqrt((xp-x1)**2 + (yp-y1)**2)
d2 = sqrt((xp-x2)**2 + (yp-y2)**2)
d3 = sqrt((xp-x3)**2 + (yp-y3)**2)
print(get_signal(d1))
print(get_signal(d2))
print(get_signal(d3))

# sol = trilaterate(aps[0],d1, aps[1],d2,aps[2],d2)
# print(sol)

sol2 = trilaterate1(aps[0],aps[1],aps[2],d1,d2,d3)
print(sol2)