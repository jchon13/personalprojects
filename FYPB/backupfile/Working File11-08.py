
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import math
import fitz  # PyMuPDF

CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 800

class ShapeDrawer:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x900")
        self.root.title("Draw Shape with Zoom, Pan, Scale, Area")
        self.root.state('zoomed')

        self.light_colors = {
            "Diesel": "red",
            "Hydrogen": "orange",
            "Solar": "green",
            "Biodiesel": "yellow"
        }

        self.light_type = tk.StringVar(value="Diesel")

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg='white')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.v_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scroll = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scroll.pack(fill=tk.X)

        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        self.bg_image_original = None
        self.bg_image_scaled = None
        self.bg_photo = None
        self.zoom_level = 1.0
        self.scale_factor = 10

        self.offset_x = 0
        self.offset_y = 0
        self.pan_start = None

        self.points = []
        self.shape_complete = False
        self.setting_scale = False
        self.scale_points = []

        self.placing_light = False
        self.light_circles = []

        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<Button-3>", self.remove_last_point)
        self.canvas.bind("<Motion>", self.update_mouse_line)
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<ButtonPress-2>", self.start_pan)
        self.canvas.bind("<B2-Motion>", self.do_pan)

        btn_frame = tk.Frame(root)
        btn_frame.pack()
        tk.Button(btn_frame, text="Place Points", command=self.activate_place_points).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Complete Shape", command=self.complete_shape).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear", command=self.clear_canvas).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Load PDF", command=self.load_pdf_background).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Set Scale", command=self.activate_set_scale).pack(side=tk.LEFT, padx=5)

        # Custom dropdown with colored lines
        light_frame = tk.Frame(root)
        light_frame.pack(pady=10)

        menu_button = tk.Menubutton(light_frame, textvariable=self.light_type, relief=tk.RAISED)
        menu = tk.Menu(menu_button, tearoff=0)
        for label, color in self.light_colors.items():
            def setter(value=label):
                self.light_type.set(value)
            menu.add_command(label=label, command=setter)
            menu.entryconfig(label, background=color)
        menu_button.config(menu=menu)
        menu_button.pack(side=tk.LEFT, padx=5)

        tk.Button(light_frame, text="Add Lights", command=self.activate_light_mode).pack(side=tk.LEFT, padx=5)

    
    def activate_place_points(self):
        self.canvas.config(cursor="arrow")
        self.placing_light = False
        self.canvas.bind("<Button-1>", self.add_point)
    def activate_light_mode(self):
            self.placing_light = True
            self.canvas.config(cursor="circle")
            self.canvas.bind("<Button-1>", self.place_light)

    def place_light(self, event):
        if not self.placing_light:
            return
        x = (event.x - self.offset_x) / self.zoom_level
        y = (event.y - self.offset_y) / self.zoom_level
        color = self.light_colors.get(self.light_type.get(), "gray")
        self.light_circles.append((x, y, color))
        self.redraw()

    def draw_lights(self):
        self.display_light_area()

    # Create a single transparent overlay for all radii
        overlay = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        for x, y, color in self.light_circles:
            sx = x * self.zoom_level + self.offset_x
            sy = y * self.zoom_level + self.offset_y
            r = 5
            influence_radius = 20  # in meters
            radius_px = influence_radius * self.scale_factor * self.zoom_level

            # Draw translucent yellow circle on the overlay
            draw.ellipse([sx - radius_px, sy - radius_px, sx + radius_px, sy + radius_px],
                        fill=(255, 255, 0, 80))

            # Draw the light point itself
            self.canvas.create_oval(sx - r, sy - r, sx + r, sy + r, fill=color, outline="black")

        # Convert the overlay to a PhotoImage and show it
        self.light_overlay = ImageTk.PhotoImage(overlay)
        self.canvas.create_image(0, 0, image=self.light_overlay, anchor="nw")
        self.light_overlay = ImageTk.PhotoImage(overlay)
        self.canvas.create_image(0, 0, image=self.light_overlay, anchor="nw")

    def load_pdf_background(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return
        try:
            doc = fitz.open(file_path)
            page = doc.load_page(0)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img = img.resize((CANVAS_WIDTH, CANVAS_HEIGHT), Image.Resampling.LANCZOS)
            self.bg_image_original = img
            self.rescale_background()
            self.redraw()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load PDF: {e}")

    def zoom(self, event):
        old_zoom = self.zoom_level
        factor = 1.1 if event.delta > 0 else 0.9
        self.zoom_level = max(0.2, min(5.0, self.zoom_level * factor))
        mouse_x, mouse_y = event.x, event.y
        world_x = (mouse_x - self.offset_x) / old_zoom
        world_y = (mouse_y - self.offset_y) / old_zoom
        self.offset_x = mouse_x - world_x * self.zoom_level
        self.offset_y = mouse_y - world_y * self.zoom_level
        self.rescale_background()
        self.redraw()

    def start_pan(self, event):
        self.pan_start = (event.x, event.y)

    def do_pan(self, event):
        if self.pan_start:
            dx = event.x - self.pan_start[0]
            dy = event.y - self.pan_start[1]
            self.offset_x += dx
            self.offset_y += dy
            self.pan_start = (event.x, event.y)
            self.redraw()

    def rescale_background(self):
        if self.bg_image_original:
            w, h = self.bg_image_original.size
            scaled = self.bg_image_original.resize((int(w * self.zoom_level), int(h * self.zoom_level)), Image.Resampling.LANCZOS)
            self.bg_image_scaled = scaled
            self.bg_photo = ImageTk.PhotoImage(self.bg_image_scaled)

    def activate_set_scale(self):
        self.setting_scale = True
        self.scale_points = []
        messagebox.showinfo("Set Scale", "Click two points to define a known distance.")

    def finish_setting_scale(self):
        x1, y1 = self.scale_points[0]
        x2, y2 = self.scale_points[1]
        pixel_dist = math.hypot(x2 - x1, y2 - y1)
        user_input = simpledialog.askfloat("Set Scale", "Enter real-world length in meters:")
        if user_input and user_input > 0:
            self.scale_factor = pixel_dist / user_input
            messagebox.showinfo("Scale Set", f"New scale: {self.scale_factor:.2f} px/m")
        else:
            messagebox.showerror("Invalid Input", "Must enter a positive number.")
        self.setting_scale = False
        self.scale_points = []
        self.redraw()

    def add_point(self, event):
        if self.placing_light:
            return
        x, y = (event.x - self.offset_x) / self.zoom_level, (event.y - self.offset_y) / self.zoom_level
        if self.setting_scale:
            self.scale_points.append((x, y))
            if len(self.scale_points) == 2:
                self.finish_setting_scale()
            return
        if self.shape_complete:
            return
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
            x1 = x1 * self.zoom_level + self.offset_x
            y1 = y1 * self.zoom_level + self.offset_y
            x2, y2 = event.x, event.y
            self.canvas.create_line(x1, y1, x2, y2, fill="gray", dash=(4, 2))
            dist = math.hypot((x2 - x1), (y2 - y1)) / self.scale_factor
            self.canvas.create_text(x2 + 10, y2 - 10, text=f"{dist:.2f} m", fill="black")

    def redraw(self):
        self.canvas.delete("all")
        if self.bg_photo:
            self.canvas.create_image(self.offset_x, self.offset_y, image=self.bg_photo, anchor="nw")
        if self.points:
            scaled_points = [(x * self.zoom_level + self.offset_x, y * self.zoom_level + self.offset_y) for x, y in self.points]
            for i, (x, y) in enumerate(scaled_points):
                self.canvas.create_oval(x-3, y-3, x+3, y+3, fill='red')
                if i > 0:
                    x0, y0 = scaled_points[i-1]
                    self.canvas.create_line(x0, y0, x, y, fill='blue', width=2)
                    self.draw_segment_length(x0, y0, x, y)
            if self.shape_complete:
                self.draw_translucent_polygon(scaled_points)
                self.draw_segment_length(*scaled_points[-1], *scaled_points[0])
                self.display_area()
        self.draw_lights()
        self.calculate_lit_area_within_shape()

    def draw_translucent_polygon(self, scaled_points):
        overlay = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        draw.polygon(scaled_points, fill=(0, 123, 255, 50))
        self.fill_overlay = ImageTk.PhotoImage(overlay)
        self.canvas.create_image(0, 0, image=self.fill_overlay, anchor="nw")
        self.canvas.create_polygon(scaled_points, fill="", outline='blue', width=2)

    def draw_segment_length(self, x1, y1, x2, y2):
        wx1 = (x1 - self.offset_x) / self.zoom_level
        wy1 = (y1 - self.offset_y) / self.zoom_level
        wx2 = (x2 - self.offset_x) / self.zoom_level
        wy2 = (y2 - self.offset_y) / self.zoom_level
        dist = math.hypot(wx2 - wx1, wy2 - wy1) / self.scale_factor
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
        area_m2 = area_px / (self.scale_factor ** 2)
        text = f"Area: {area_m2:.2f} m²"
        self.canvas.create_rectangle(5, 5, 180, 30, fill='white', outline='gray')
        self.canvas.create_text(10, 10, anchor="nw", text=text, fill="blue", font=("Arial", 14))

    def display_light_area(self):
        import numpy as np
        light_mask = Image.new("L", (CANVAS_WIDTH, CANVAS_HEIGHT), 0)
        draw = ImageDraw.Draw(light_mask)
        influence_radius = 20  # meters
        radius_px = int(influence_radius * self.scale_factor)

        for x, y, _ in self.light_circles:
            sx = int(x * self.zoom_level + self.offset_x)
            sy = int(y * self.zoom_level + self.offset_y)
            draw.ellipse([sx - radius_px, sy - radius_px, sx + radius_px, sy + radius_px], fill=1)

        mask_array = np.array(light_mask)
        unique_area_px = np.count_nonzero(mask_array)
        unique_area_m2 = unique_area_px / (self.scale_factor ** 2)

        text = f"Light Area: {unique_area_m2:.2f} m²"
        self.canvas.create_rectangle(200, 5, 420, 30, fill='white', outline='gray')
        self.canvas.create_text(210, 10, anchor="nw", text=text, fill="darkgreen", font=("Arial", 14))


    def calculate_lit_area_within_shape(self):
        import numpy as np
        if not self.shape_complete or not self.points:
            return

        # Create mask for lights
        light_mask = Image.new("L", (CANVAS_WIDTH, CANVAS_HEIGHT), 0)
        draw_light = ImageDraw.Draw(light_mask)
        influence_radius = 20  # meters
        radius_px = int(influence_radius * self.scale_factor)

        for x, y, _ in self.light_circles:
            sx = int(x * self.zoom_level + self.offset_x)
            sy = int(y * self.zoom_level + self.offset_y)
            draw_light.ellipse([sx - radius_px, sy - radius_px, sx + radius_px, sy + radius_px], fill=1)

        # Create mask for shape
        shape_mask = Image.new("L", (CANVAS_WIDTH, CANVAS_HEIGHT), 0)
        draw_shape = ImageDraw.Draw(shape_mask)
        scaled_points = [(x * self.zoom_level + self.offset_x, y * self.zoom_level + self.offset_y) for x, y in self.points]
        draw_shape.polygon(scaled_points, fill=1)

        # Combine masks
        light_array = np.array(light_mask)
        shape_array = np.array(shape_mask)
        intersection = np.logical_and(light_array, shape_array)
        intersection_area_px = np.count_nonzero(intersection)
        intersection_area_m2 = intersection_area_px / (self.scale_factor ** 2)

        text = f"Lit Area Inside Shape: {intersection_area_m2:.2f} m²"
        self.canvas.create_rectangle(430, 5, 730, 30, fill='white', outline='gray')
        self.canvas.create_text(440, 10, anchor="nw", text=text, fill="darkorange", font=("Arial", 14))

    def complete_shape(self):
        if len(self.points) < 3:
            messagebox.showinfo("Info", "At least 3 points required to complete shape.")
            return
        self.shape_complete = True
        self.redraw()

    def clear_canvas(self):
        self.points = []
        self.shape_complete = False
        self.light_circles = []
        self.canvas.delete("all")
        self.redraw()

if __name__ == "__main__":
    root = tk.Tk()
    app = ShapeDrawer(root)
    root.mainloop()
