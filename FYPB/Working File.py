import tkinter as tk
from tkinter import messagebox
import math

scale_factor = 10  # 1 meter = 10 pixels

class ShapeDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("Draw Shape with Meters & Area")
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()

        self.points = []
        self.shape_complete = False
        self.mouse_line = None
        self.area_text = None

        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<Button-3>", self.remove_last_point)
        self.canvas.bind("<Motion>", self.update_mouse_line)

        btn_frame = tk.Frame(root)
        btn_frame.pack()
        tk.Button(btn_frame, text="Complete Shape", command=self.complete_shape).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear", command=self.clear_canvas).pack(side=tk.LEFT, padx=5)

    def add_point(self, event):
        if self.shape_complete:
            return

        x, y = event.x, event.y

        # Auto-close if near first point
        if len(self.points) > 2:
            dx = x - self.points[0][0]
            dy = y - self.points[0][1]
            if math.hypot(dx, dy) <= 10:
                self.complete_shape()
                return

        self.points.append((x, y))
        self.redraw()

    def remove_last_point(self, event):
        if not self.shape_complete and self.points:
            self.points.pop()
            self.redraw()

    def update_mouse_line(self, event):
        if not self.shape_complete and self.points:
            self.redraw()
            x1, y1 = self.points[-1]
            x2, y2 = event.x, event.y
            self.canvas.create_line(x1, y1, x2, y2, fill="gray", dash=(4, 2))

            dist = math.hypot(x2 - x1, y2 - y1) / scale_factor
            self.canvas.create_text(x2 + 10, y2 - 10, text=f"{dist:.2f} m", fill="black")

    def redraw(self):
        self.canvas.delete("all")
        if not self.points:
            return

        for i, (x, y) in enumerate(self.points):
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill='red')
            if i > 0:
                x0, y0 = self.points[i-1]
                self.canvas.create_line(x0, y0, x, y, fill='blue', width=2)
                self.draw_segment_length(x0, y0, x, y)

        if self.shape_complete:
            self.canvas.create_polygon(self.points, fill="#add8e6", outline='blue', width=2)
            self.draw_segment_length(*self.points[-1], *self.points[0])
            self.display_area()

    def draw_segment_length(self, x1, y1, x2, y2):
        dist = math.hypot(x2 - x1, y2 - y1) / scale_factor
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        self.canvas.create_text(mid_x + 5, mid_y - 5, text=f"{dist:.2f} m", fill="black", font=("Arial", 10))

    def calculate_area(self):
        area = 0
        pts = self.points
        for i in range(len(pts)):
            j = (i + 1) % len(pts)
            area += pts[i][0] * pts[j][1]
            area -= pts[j][0] * pts[i][1]
        return abs(area) / 2

    def display_area(self):
        area_px = self.calculate_area()
        area_m2 = area_px / (scale_factor ** 2)
        self.area_text = self.canvas.create_text(10, 590, anchor="w",
                                                 text=f"Area: {area_m2:.2f} m²", fill="blue", font=("Arial", 14))

    def complete_shape(self):
        if len(self.points) < 3:
            messagebox.showinfo("Info", "At least 3 points required to complete shape.")
            return
        self.shape_complete = True
        self.redraw()

    def clear_canvas(self):
        self.points = []
        self.shape_complete = False
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShapeDrawer(root)
    root.mainloop()
