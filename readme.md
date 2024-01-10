# Simple 3D Object Projection

## Description
This project demonstrates a simple 3D perspective projection of an object using Python and the Pygame library. The user can control the position of the object along different axes, change the Object itself and control different values.

## Instructions
1. Use W and S keys to move the object up and down along the y-axis.
2. Use A and D keys to move the object left and right along the x-axis.
3. Use Y and X keys to move the object forward and backward along the z-axis.

## Dependencies
- Python standard library
- Pygame library
- Numpy library

## Setup
1. Install Python: https://www.python.org/downloads/
2. Install Pygame: `pip install pygame`
3. Install Numpy: `pip install numpy`

## Usage
1. Clone the repository: `git clone https://github.com/codeChaosConductor/Simple-3D-Object-Projection/`
2. Navigate to the project directory: `cd <project-directory>`
3. Run the script: `python object_projection.py`

## Configuration
You can customize the following parameters in the script:
- `fov`: Field of view for the perspective projection.
- `far`: Far clipping plane distance.
- `near`: Near clipping plane distance.
- `speed`: Movement speed of the object.
- `draw_vertices`: Set to `True` to draw vertices.
- `draw_edges`: Set to `True` to draw edges.

## Object Configuration
- `points`: List of 3D coordinates representing object vertices.
- `point_connections`: List of connections between vertices.

## Credits
- Developed by Fynn Mannack
- If you use this code in your project, please provide attribution by linking to this [repository](https://github.com/codeChaosConductor/Simple-3D-Object-Projection/) in your project documentation or source code.

This code was written as a part of my research paper (Facharbeit) about 3D-animations.

Feel free to modify the code, experiment with different objects, and integrate it into your own projects! If you find any issues or have suggestions, please create an issue or pull request.