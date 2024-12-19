import tkinter as tk
from tkinter.colorchooser import askcolor
import csv
import threading
import numpy as np
from crazyflie_py import Crazyswarm
import random

# Initialize variables
is_drawing = False
drawing_color = "black"
line_width = 2
coordinates = []  # List to store drawing coordinates

####################### drawing #######################


def start_drawing(event):
    global is_drawing, prev_x, prev_y
    is_drawing = True
    prev_x, prev_y = event.x, event.y


def draw(event):
    global is_drawing, prev_x, prev_y
    if is_drawing:
        current_x, current_y = event.x, event.y
        canvas.create_line(
            prev_x,
            prev_y,
            current_x,
            current_y,
            fill=drawing_color,
            width=line_width,
            capstyle=tk.ROUND,
            smooth=True,
        )
        # Log coordinates
        coordinates.append((prev_x, prev_y, current_x, current_y))
        prev_x, prev_y = current_x, current_y


def stop_drawing(event):
    global is_drawing
    is_drawing = False


def save_coordinates_to_csv():
    # Save the coordinates to a CSV file
    file_name = "drawing_coordinates.csv"
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Start_X", "Start_Y", "End_X", "End_Y"])  # Header
        writer.writerows(coordinates)

    print(f"Coordinates saved to {file_name}!")


####################### drawing #######################

####################### crazyflie #######################


# crazyflie motion with coordinates
def initialize_crazyflie():
    global crazyfly
    global timeHelper
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    crazyfly = allcfs.crazyflies[0]  # using one crazyflie
    crazyfly.takeoff(targetHeight=0.5, duration=1.0)
    timeHelper.sleep(1.0)


# Function to move Crazyflie along the path in the CSV
# def move_crazyflie_along_path():
#     # Read the coordinates from the CSV file
#     file_name = "drawing_coordinates.csv"
#     with open(file_name, mode="r") as file:
#         reader = csv.reader(file)
#         next(reader)  # Skip header
#         numRows = 0

#         for row in reader:
#             duration = 1
#             start_x, start_y, end_x, end_y = map(float, row)

#             if numRows == 0:
#                 duration = 5

#             # Convert canvas coordinates to flight coordinates

#             # changing origin to bottom left
#             flight_start_x = (start_x / 500) * 4  # Example scaling
#             flight_start_y = ((800 - start_y) / 400) * 4  # Example scaling

#             flight_end_x = (end_x / 500) * 4  # Example scaling
#             flight_end_y = ((800 - end_y) / 400) * 4  # Example scaling

#             # Move Crazyflie from start to end of each line segment
#             crazyfly.goTo(
#                 np.array([0.5, flight_start_y, flight_start_x]), 0.0, duration
#             )
#             timeHelper.sleep(duration)  # You can adjust the delay as needed
#             crazyfly.goTo(np.array([0.5, flight_start_y, flight_start_x]), 0.0, 1.0)

#             # Optionally, add a sleep to make the drone move in stages (adjust for your timing needs)
#             timeHelper.sleep(1.0)  # You can adjust the delay as needed

#             numRows += 1

#     # Land Crazyflie after completing the movement
#     crazyfly.land(0.04, 2.0)


def move_crazyflie_along_path1():
    # Read the coordinates from the CSV file
    canvas_width = 800
    canvas_height = 600
    max_y = 3  # Example lab width in meters
    max_z = 2  # Lab height in meters

    file_name = "drawing_coordinates.csv"
    with open(file_name, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        all_rows = list(reader)
        total_points = len(all_rows)

        increment = max(1, total_points // 8)
        print(f"Total points:{total_points}, Increment: {increment}")

        for numRows in range(0, total_points, increment):
            row = all_rows[numRows]
            duration = 0.5
            start_x, start_y, end_x, end_y = map(float, row)

            if numRows == 0:
                duration = 2

            # Convert canvas coordinates to flight coordinates

            # # changing origin to bottom left
            # flight_start_y = (start_x / 500) * 2  # Example scaling (map to Y axis)
            # flight_start_z = (
            #     (800 - start_y) / 400
            # ) * 1  # Example scaling (map to Z axis)

            # flight_end_y = (end_x / 500) * 2  # Example scaling (map to Y axis)
            # flight_end_z = ((800 - end_y) / 400) * 1  # Example scaling (map to Z axis)

            ################### editing this for now############
            flight_start_y = (start_x / canvas_width) * max_y
            flight_start_z = ((start_y) / canvas_height) * max_z
            flight_end_y = (end_x / canvas_width) * max_y
            flight_end_z = ((end_y) / canvas_height) * max_z
            ################### editing this for now############

            # flight_start_y = (start_x / 600) * 3
            # flight_start_z = (start_y / 450) * 2
            # flight_end_y = (end_x / 600) * 3
            # flight_end_z = (end_y / 450) * 2

            # Move Crazyflie from start to end of each line segment
            crazyfly.goTo(
                np.array([0.5, flight_start_y, flight_start_z]),
                0.0,
                duration,  # Z and Y movement
            )
            timeHelper.sleep(2)  # You can adjust the delay as needed

    # Land Crazyflie after completing the movement
    crazyfly.land(0.04, 3.0)


def move_crazyflie_along_path():
    # Read the coordinates from the CSV file
    canvas_width = 800
    canvas_height = 600
    max_y = 3  # Example lab width in meters
    max_z = 2  # Lab height in meters

    file_name = "drawing_coordinates.csv"
    with open(file_name, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        all_rows = list(reader)
        total_points = len(all_rows)
        # all_points = list(reader)
        # sampled_points = all_points[::40]

        increment = max(1, total_points // 4)
        print(f"Total points:{total_points}, Increment: {increment}")

        # numRows = 0

        for numRows in range(0, total_points, increment):
            row = all_rows[numRows]
            duration = 0.5
            start_x, start_y, end_x, end_y = map(float, row)

            if numRows == 0:
                duration = 2

            ################### editing this for now############
            flight_start_y = (start_x / canvas_width) * max_y
            flight_start_z = ((canvas_height - start_y) / canvas_height) * max_z
            flight_end_y = (end_x / canvas_width) * max_y
            flight_end_z = ((canvas_height - end_y) / canvas_height) * max_z
            ################### editing this for now############

            # flight_start_y = (start_x / 600) * 3
            # flight_start_z = (start_y / 450) * 2
            # flight_end_y = (end_x / 600) * 3
            # flight_end_z = (end_y / 450) * 2

            # Move Crazyflie from start to end of each line segment

            #   crazyfly.goTo(
            #      np.array([0, flight_start_y, flight_start_z]),
            #     0.0,
            #    duration,  # Z and Y movement
            # )

            crazyfly.cmdPosition(np.array([0.5, flight_start_y, flight_start_z]), 0.0)

            timeHelper.sleep(0.05)  # You can adjust the delay as needed
            # crazyfly.goTo(np.array([0, flight_end_y, flight_end_z]), 0.0, duration)
            crazyfly.cmdPosition(np.array([0.5, flight_end_y, flight_end_z]), 0.0)

            timeHelper.sleep(0.05)

            # Optionally, add a sleep to make the drone move in stages (adjust for your timing needs)
        #   timeHelper.sleep(2.0)  # You can adjust the delay as needed

        # numRows += 120

    # Land Crazyflie after completing the movement
    crazyfly.land(0.04, 3.0)


####################### crazyflie #######################


def end_game():
    # Save coordinates and close the application
    save_coordinates_to_csv()
    root.destroy()


def load_words_from_csv():
    """Loads words from a CSV file."""
    words = []
    try:
        with open("words.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # Ensure there's a word in the row
                    words.append(row[0])
    except FileNotFoundError:
        print("CSV file not found. Please ensure 'words.csv' is in the directory.")
    return words


def display_random_word():
    """Displays a random word from the CSV in the text box."""
    words = load_words_from_csv()
    if words:
        random_word = random.choice(words)
        word_text_box.config(state=tk.NORMAL)  # Enable editing
        word_text_box.delete(1.0, tk.END)  # Clear existing text
        word_text_box.insert(tk.END, random_word)  # Insert the random word
        word_text_box.config(state=tk.DISABLED)  # Disable editing after inserting


# Initialize the GUI
root = tk.Tk()
root.title("Whiteboard App")
root.geometry("800x600")

# Canvas for drawing
canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

# Frame for controls
controls_frame = tk.Frame(root)
controls_frame.pack(side="top", fill="x")

clear_button = tk.Button(
    controls_frame, text="Clear Canvas", command=lambda: canvas.delete("all")
)
clear_button.pack(side="left", padx=5, pady=5)

end_button = tk.Button(controls_frame, text="End Game & Save", command=end_game)
end_button.pack(side="left", padx=5, pady=5)

random_word_button = tk.Button(
    controls_frame, text="Show Random Word", command=display_random_word
)
random_word_button.pack(side="left", padx=5, pady=5)
word_text_box = tk.Text(root, height=2, width=40, font=("Helvetica", 16))
word_text_box.pack(side="top", padx=10, pady=10)
word_text_box.config(state=tk.DISABLED)

canvas.bind("<Button-1>", start_drawing)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_drawing)


def launch(nodes):
    executor = rclpy.executors.MultiThreadedExecutor()

    for node in nodes:
        executor.add_node(node)

    thread = threading.Thread(target=executor.spin, daemon=True)
    thread.start()
    try:
        while rclpy.ok():
            pass
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()
    thread.join()


# def initialize_crazyflie():
#     # node_config_file = get_package_share_directory('crazyflie'), 'config', 'crazyflies.yaml'

#     # Initialize swarm
#     global crazyfly
#     swarm = Crazyswarm()
#     timeHelper = swarm.timeHelper
#     allcfs = swarm.allcfs
#     crazyfly = allcfs.crazyflies[0]  # only using the first crazyflie
#     crazyfly.takeoff(targetHeight=0.5, duration=1.0)  # Take off with a target height
#     timeHelper.sleep(1.0)
#     with open("cfs_ordering.yaml") as f:
#         ordering = yaml.safe_load(f) #TODO!!!
#         order = ordering['cfs']

#     crazyflies = [swarm.allcfs.crazyfliesById[int(k)] for k in order]
#     counter = 0
#     nodes = []
#     cfs = []

#     #   -----------Insert Nodes Here-----------
#     import groupAllCFs_node
#     cfs = []
#     cfs.append(crazyflies[0])
#     nodes.append(groupAllCFs_node.worker_node(cfs, len(nodes), 1))

#     # Launch all nodes
#     return launch(nodes)

root.mainloop()


initialize_crazyflie()


move_crazyflie_along_path1()
