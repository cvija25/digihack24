import pygame
import numpy
from numpy import sqrt, dot, cross
from numpy.linalg import norm

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Trilateration Simulation")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Initial points and parameters
aps = [(200, 200), (400, 100), (300, 400)]  # Scaled for display purposes
P = [300, 300]  # Movable point P (scaled for display)
move_step = 2  # How much P moves with each arrow key press

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
        raise Exception("The three spheres do not intersect!")
    z = sqrt(temp4)                                      
    p_12_a = P1 + x*e_x + y*e_y + z*e_z                  
    p_12_b = P1 + x*e_x + y*e_y - z*e_z                  
    return p_12_a, p_12_b 

# Calculate distances
def calculate_distances(P, aps):
    d1 = sqrt((P[0] - aps[0][0]) ** 2 + (P[1] - aps[0][1]) ** 2)
    d2 = sqrt((P[0] - aps[1][0]) ** 2 + (P[1] - aps[1][1]) ** 2)
    d3 = sqrt((P[0] - aps[2][0]) ** 2 + (P[1] - aps[2][1]) ** 2)
    return d1, d2, d3

# Main loop
running = True
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        P[0] -= move_step
    if keys[pygame.K_RIGHT]:
        P[0] += move_step
    if keys[pygame.K_UP]:
        P[1] -= move_step
    if keys[pygame.K_DOWN]:
        P[1] += move_step

    # Calculate distances and signals
    d1, d2, d3 = calculate_distances(P, aps)
    signal1 = get_signal(d1)
    signal2 = get_signal(d2)
    signal3 = get_signal(d3)
    
    try:
        # Solve trilateration
        sol2 = trilaterate1(aps[0], aps[1], aps[2], d1, d2, d3)
    except Exception as e:
        sol2 = [(0, 0), (0, 0)]  # Error case
    
    # Draw access points (aps)
    for ap in aps:
        pygame.draw.circle(screen, RED, ap, 5)
    
    # Draw movable point P
    pygame.draw.circle(screen, GREEN, P, 5)
    
    # Draw solution points from trilateration (if valid)
    
    pygame.draw.circle(screen, GREEN, sol2[0], 5)
    pygame.draw.circle(screen, GREEN, sol2[1], 5)

    # Display signal strengths as text (optional)
    font = pygame.font.Font(None, 36)
    signal_text = font.render(f"Signals: {signal1:.2f}, {signal2:.2f}, {signal3:.2f}", True, (0, 0, 0))
    screen.blit(signal_text, (10, 10))

    pygame.display.flip()

pygame.quit()
