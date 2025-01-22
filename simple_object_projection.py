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

rotation_x = 0
rotation_y = 0
rotation_z = 0

# Set the filename of the object
filename = "square_based_pyramid.json"

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
middle_point = mesh[3]

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


def rot_y(pt):
        v = pt[0] - middle_point[0]
        u = pt[1] - middle_point[1]
        
        hyp = np.sqrt(u**2 + v**2)

        angle = np.degrees(np.arctan2(u, v))

        new_angle = angle - rotation_y

        new_x = np.cos(np.radians(new_angle)) * hyp + middle_point[0]
        new_y = np.sin(np.radians(new_angle)) * hyp + middle_point[1]

        return [new_x, new_y, pt[2], pt[3]]

def rot_x(pt):
        v = pt[1] - middle_point[1]
        u = pt[2] - middle_point[2]
        
        hyp = np.sqrt(u**2 + v**2)

        angle = np.degrees(np.arctan2(u, v))

        new_angle = angle - rotation_x

        new_x = np.cos(np.radians(new_angle)) * hyp + middle_point[1]
        new_y = np.sin(np.radians(new_angle)) * hyp + middle_point[2]

        return [pt[0], new_x, new_y, pt[3]]

def rot_z(pt):
        v = pt[0] - middle_point[0]
        u = pt[2] - middle_point[2]
        
        hyp = np.sqrt(u**2 + v**2)

        angle = np.degrees(np.arctan2(u, v))

        new_angle = angle - rotation_z

        new_x = np.cos(np.radians(new_angle)) * hyp + middle_point[0]
        new_y = np.sin(np.radians(new_angle)) * hyp + middle_point[2]

        return [new_x, pt[1], new_y, pt[3]]

def rotate_object(pot):
        
        new_pt = rot_z(rot_x(rot_y(pot)))

        return np.array(new_pt, dtype=np.double)


pygame.init()
screen = pygame.display.set_mode((window_size[0], window_size[1]))
resized_screen = pygame.transform.scale(screen, (window_size[0], window_size[1]))
clock = pygame.time.Clock()

projection_matrix = make_projection_matrix(aspect_ratio, fov, far, near)

# create an offset between camera and object
middle_point[2] += 5
for i in range(len(points)):
    points[i][2] += 5

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
         rotation_z = 0
         rotation_x = 0
         rotation_y = 0
    if keys[pygame.K_LEFT]:
        rotation_z += 1
    if keys[pygame.K_RIGHT]:
        rotation_z -= 1
    if keys[pygame.K_UP]:
        rotation_x += 1
    if keys[pygame.K_DOWN]:
        rotation_x -= 1
    if keys[pygame.K_n]:
        rotation_y += 1
    if keys[pygame.K_m]:
        rotation_y -= 1

    if keys[pygame.K_s]:
            middle_point[1] -= speed
    if keys[pygame.K_w]:
            middle_point[1] += speed
    if keys[pygame.K_a]:
            middle_point[0] -= speed
    if keys[pygame.K_d]:
            middle_point[0] += speed
    if keys[pygame.K_y]:
            middle_point[2] -= speed
    if keys[pygame.K_x]:
            middle_point[2] += speed

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
    for pt in points:
        
        new_point = rotate_object(pt)

        calc = np.matmul(projection_matrix, new_point).flatten()
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

    #screen.blit(resized_screen, (0, 0))
    pygame.display.flip()  # Rerender the screen
    clock.tick(30)  # Framerate of 30 fps

pygame.quit()
