import tkinter as tk
from tkinter.colorchooser import askcolor
import csv

# Initialize variables
is_drawing = False
drawing_color = "black"
line_width = 2
coordinates = []  # List to store drawing coordinates

def start_drawing(event):
    global is_drawing, prev_x, prev_y
    is_drawing = True
    prev_x, prev_y = event.x, event.y

def draw(event):
    global is_drawing, prev_x, prev_y
    if is_drawing:
        current_x, current_y = event.x, event.y
        canvas.create_line(prev_x, prev_y, current_x, current_y, fill=drawing_color, width=line_width, capstyle=tk.ROUND, smooth=True)
        # Log coordinates
        coordinates.append((prev_x, prev_y, current_x, current_y))
        prev_x, prev_y = current_x, current_y

def stop_drawing(event):
    global is_drawing
    is_drawing = False

def change_pen_color():
    global drawing_color
    color = askcolor()[1]
    if color:
        drawing_color = color

def change_line_width(value):
    global line_width
    line_width = int(value)

def save_coordinates_to_csv():
    # Save the coordinates to a CSV file
    file_name = "drawing_coordinates.csv"
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Start_X", "Start_Y", "End_X", "End_Y"])  # Header
        writer.writerows(coordinates)
    print(f"Coordinates saved to {file_name}!")

def end_game():
    # Save coordinates and close the application
    save_coordinates_to_csv()
    root.destroy()

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

color_button = tk.Button(controls_frame, text="Change Color", command=change_pen_color)
color_button.pack(side="left", padx=5, pady=5)

clear_button = tk.Button(controls_frame, text="Clear Canvas", command=lambda: canvas.delete("all"))
clear_button.pack(side="left", padx=5, pady=5)

line_width_label = tk.Label(controls_frame, text="Line Width:")
line_width_label.pack(side="left", padx=5, pady=5)

line_width_slider = tk.Scale(controls_frame, from_=1, to=10, orient="horizontal", command=lambda val: change_line_width(val))
line_width_slider.set(line_width)
line_width_slider.pack(side="left", padx=5, pady=5)

end_button = tk.Button(controls_frame, text="End Game & Save", command=end_game)
end_button.pack(side="left", padx=5, pady=5)

canvas.bind("<Button-1>", start_drawing)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_drawing)

root.mainloop()