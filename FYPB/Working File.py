import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import math
import fitz  # PyMuPDF

scale_factor = 10  # 1 meter = 10 pixels

class ShapeDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("Draw Shape with Meters & Area")
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()

        self.points = []
        self.shape_complete = False
        self.bg_image = None
        self.bg_photo = None
        self.fill_overlay = None

        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<Button-3>", self.remove_last_point)
        self.canvas.bind("<Motion>", self.update_mouse_line)

        btn_frame = tk.Frame(root)
        btn_frame.pack()
        tk.Button(btn_frame, text="Complete Shape", command=self.complete_shape).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear", command=self.clear_canvas).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Load PDF", command=self.load_pdf_background).pack(side=tk.LEFT, padx=5)

    def load_pdf_background(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return
        try:
            doc = fitz.open(file_path)
            page = doc.load_page(0)
            pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img = img.resize((800, 600), Image.Resampling.LANCZOS)  # Pillow 10+
            self.bg_image = img
            self.bg_photo = ImageTk.PhotoImage(img)
            self.redraw()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load PDF: {e}")

    def add_point(self, event):
        if self.shape_complete:
            return

        x, y = event.x, event.y

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

        # Draw background image if available
        if self.bg_photo:
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        if not self.points:
            return

        for i, (x, y) in enumerate(self.points):
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill='red')
            if i > 0:
                x0, y0 = self.points[i-1]
                self.canvas.create_line(x0, y0, x, y, fill='blue', width=2)
                self.draw_segment_length(x0, y0, x, y)

        if self.shape_complete:
            # Draw translucent shape
            self.draw_translucent_polygon()
            self.draw_segment_length(*self.points[-1], *self.points[0])
            self.display_area()

    def draw_translucent_polygon(self):
        # Create transparent overlay using PIL
        overlay = Image.new("RGBA", (800, 600), (0, 0, 0, 0))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(overlay)
        draw.polygon(self.points, fill=(0, 123, 255, 50))  # ~20% opacity

        self.fill_overlay = ImageTk.PhotoImage(overlay)
        self.canvas.create_image(0, 0, image=self.fill_overlay, anchor="nw")

        # Draw outline over it
        self.canvas.create_polygon(self.points, fill="", outline='blue', width=2)

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
        self.canvas.create_text(10, 590, anchor="w",
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
        self.redraw()

if __name__ == "__main__":
    root = tk.Tk()
    app = ShapeDrawer(root)
    root.mainloop()
