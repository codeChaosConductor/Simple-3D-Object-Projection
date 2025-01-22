import json
import os

# Specify File to write to
filename = "triangle_mesh.json"

# The following list 'points' is supposed to contain arrays representing the coordinates of each vertex.
# Each array should be a 4x1 column vector, with the first three elements representing (x, y, z) coordinates,
# and the last element being 1 for homogeneous coordinates.
# You can take the given points as an example.
points = [
    [[0], [0], [0], [1]],
    [[0], [1], [0], [1]],
    [[0], [0.5], [0], [1]]
]

# The 'point_connections' array defines connections between vertices to create edges.
# Use the index of the vertices from the 'points' list.
# Note: Indexing starts from 1 for better understandability.
point_connections = [
    [1, 2],
    [2, 3],
    [3, 1]
]

# The 'face_connections' array defines the vertices used for creating faces
# Use the index of the vertices from the 'points' list.
# Note: Indexing starts from 1 for better understandability.
face_connections = [
    [1, 2, 3]
]

middle_point = [0.5, 0.5, 0.5]

if os.path.exists("objects/"+filename):
    f = open("objects/"+filename, "w")
    f.write(json.dumps([points, point_connections, face_connections, middle_point]))
    f.close()
    print("file successfully overwritten")
else:
    f = open("objects/"+filename, "x")
    f.write(json.dumps([points, point_connections, face_connections, middle_point]))
    f.close()
    print("file successfully created")
