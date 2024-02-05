import numpy as np
import math
import pygame
import json

# Basic perspective projection of an object.
# Control the position of the cube with W,S (up,down), A,D (left, right) and Y,X (forward, backward).

# Initialization of camera and window variables
# These variables can be changed without any hesitations
fov = 70
far = 10
near = 0.1
speed = 0.01

# Set the filename of the object
filename = "cube.json"

# Specify what should be drawn
draw_vertices = True
draw_edges = True
draw_faces = True

# Window settings 
window_size = [800, 600]
aspect_ratio = window_size[0] / window_size[1]


# Open and convert the object file
f = open("objects/"+filename, "r")
mesh = json.loads(f.read())
f.close()

points = []

for point in mesh[0]:
    points.append(np.array(point, dtype=np.double))

edge_connections = mesh[1]
face_connections = mesh[2]

# Function for creating a projection matrix

def make_projection_matrix(aspect_ratio, fov, far, near):
    focal_length = 1 / math.tan(math.radians(0.5*fov))
    projection_matrix = np.array([
        [-focal_length / aspect_ratio, 0, 0, 0],
        [0, focal_length, 0, 0],
        [0, 0, (far + near) / (far - near), (2 * far * near) / (near - far)],
        [0, 0, -1, 0]
    ])
    return projection_matrix


pygame.init()
screen = pygame.display.set_mode((window_size[0], window_size[1]))
clock = pygame.time.Clock()

projection_matrix = make_projection_matrix(aspect_ratio, fov, far, near)

# create an offset between camera and object
for i in range(len(points)):
    points[i][2] += 5

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    keys = pygame.key.get_pressed()
    for i in range(len(points)):
        if keys[pygame.K_s]:
            points[i][1][0] -= speed
        if keys[pygame.K_w]:
            points[i][1][0] += speed
        if keys[pygame.K_a]:
            points[i][0][0] -= speed
        if keys[pygame.K_d]:
            points[i][0][0] += speed
        if keys[pygame.K_y]:
            points[i][2][0] -= speed
        if keys[pygame.K_x]:
            points[i][2][0] += speed

    screen.fill((255, 255, 255))

    calculated_points = []

    # calculate the coordinates for each vertice
    for point in points:
        calc = np.matmul(projection_matrix, point).flatten()
        if calc[3] != 0:
            calc /= calc[3]

    # check if point has to get clipped
        if -1 <= calc[2] <= 1:
            calculated_points.append([calc[0], calc[1], 1])
        else:
            calculated_points.append([calc[0], calc[1], 0])

    # When defined in 'draw_faces' draw faces
    if draw_faces == True:
        for face in face_connections:
            face_points = []
            is_clipping = False
            for point in face:
                if calculated_points[point-1][2] == 0:
                    is_clipping = True
                face_points.append((calculated_points[point-1][0] * aspect_ratio * window_size[0] + 0.5 *
                                   window_size[0], calculated_points[point-1][1] * window_size[0] + 0.5 * window_size[1]))
            if not is_clipping:
                pygame.draw.polygon(screen, (0, 200, 200), face_points)

    # When defined in 'draw_vertices' draw vertices
    if draw_vertices == True:
        for point in calculated_points:
            pos = (int(point[0] * aspect_ratio * window_size[0] + 0.5 * window_size[0]),
                   int(point[1] * window_size[0] + 0.5 * window_size[1]))
            if point[2] == 1:
                pygame.draw.circle(screen, (255, 0, 0), pos, 5)

    # When defined in 'draw_edges' draw edges
    if draw_edges == True:
        for x in edge_connections:
            pos1 = (calculated_points[x[0]-1][0] * aspect_ratio * window_size[0] + 0.5 *
                    window_size[0], calculated_points[x[0]-1][1] * window_size[0] + 0.5 * window_size[1])
            pos2 = (calculated_points[x[1]-1][0] * aspect_ratio * window_size[0] + 0.5 *
                    window_size[0], calculated_points[x[1]-1][1] * window_size[0] + 0.5 * window_size[1])
            if calculated_points[x[0]-1][2] == 1 and calculated_points[x[1]-1][2] == 1:
                pygame.draw.line(screen, (0, 0, 0), pos1, pos2)

    pygame.display.flip()  # Rerender the screen
    clock.tick(30)  # Framerate of 30 fps

pygame.quit()
