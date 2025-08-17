
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageGrab
import io 
import math
import fitz  # PyMuPDF

CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 800

class ShapeDrawer:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x950")
        self.root.title("Draw Shape with Zoom, Pan, Scale, Area")
        try:
            self.root.state('zoomed')
        except Exception:
            pass

        # ====== LIGHT TYPES, COLORS, AND SCORES ======
        self.light_colors = {
            "Diesel": "red",
            "Hydrogen": "orange",
            "Solar": "green",
            "Biodiesel": "yellow"
        }
        # (source_score, efficiency_score)
        self.light_scores = {
            "Hydrogen": (1.0, 1.0),
            "Solar": (0.306, 0.238),
            "Diesel": (0.108, 0.388),
            "Biodiesel": (0.578, 0.406),
        }

        # Default weekly costs per tower (AUD) — editable in UI
        self.weekly_running_costs = {
            "Diesel": 112,
            "Hydrogen": 0,
            "Solar": 0,
            "Biodiesel": 193,
        }
        self.weekly_hire_costs = {
            "Diesel": 560,
            "Hydrogen": 430,
            "Solar": 330,
            "Biodiesel": 560,
        }

        self.light_type = tk.StringVar(value="Diesel")

        # ====== TOP CONTROLS (CENTERED) ======
        top_controls = tk.Frame(root)
        top_controls.pack(side=tk.TOP, fill=tk.X)

        # a centered container that holds the two rows
        centered_block = tk.Frame(top_controls)
        centered_block.pack(pady=(6, 4))  # pack centers by default, so this whole block is centered

        # --- Buttons row ---
        btn_frame = tk.Frame(centered_block)
        btn_frame.pack(side=tk.TOP, pady=(0, 4))
        tk.Button(btn_frame, text="Place Points", command=self.activate_place_points).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Complete Shape", command=self.complete_shape).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear", command=self.clear_canvas).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Load PDF", command=self.load_pdf_background).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Set Scale", command=self.activate_set_scale).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text=" Export Plan to PDF", command=self.export_pdf).pack(side=tk.LEFT, padx=5)

        # --- Light type dropdown row ---
        light_frame = tk.Frame(centered_block)
        light_frame.pack(side=tk.TOP)
        menu_button = tk.Menubutton(light_frame, textvariable=self.light_type, relief=tk.RAISED, width=16)
        menu = tk.Menu(menu_button, tearoff=0)
        for label, color in self.light_colors.items():
            def setter(value=label):
                self.light_type.set(value)
            menu.add_command(label=label, command=setter)
            try:
                menu.entryconfig(label, background=color)
            except Exception:
                pass
        menu_button.config(menu=menu)
        menu_button.pack(side=tk.LEFT, padx=5)
        tk.Button(light_frame, text="Add Lights", command=self.activate_light_mode).pack(side=tk.LEFT, padx=5)

        # ====== MAIN LAYOUT ======
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.side_panel = tk.Frame(self.canvas_frame, bd=1, relief=tk.GROOVE, padx=10, pady=10)
        self.side_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=8, pady=8)

        self.canvas = tk.Canvas(self.canvas_frame, bg='white', width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.v_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.h_scroll = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        # ====== STATE ======
        self.bg_image_original = None
        self.bg_image_scaled = None
        self.bg_photo = None
        self.zoom_level = 1.0
        self.scale_factor = 10  # pixels per meter (will be set by user)

        self.offset_x = 0
        self.offset_y = 0
        self.pan_start = None

        self.points = []
        self.shape_complete = False
        self.setting_scale = False
        self.scale_points = []

        self.placing_light = False
        self.lights = []  # list of dicts: {x,y,type,color}

        # ====== BINDINGS ======
        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<Button-3>", self.remove_last_point)
        self.canvas.bind("<Motion>", self.update_mouse_line)
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<ButtonPress-2>", self.start_pan)
        self.canvas.bind("<B2-Motion>", self.do_pan)

        # ====== RIGHT-SIDE PANEL CONTENT ======
        self.build_right_panel()

        # overlays
        self.fill_overlay = None
        self.light_overlay = None
        # ---- Undo/Redo ----
        self.undo_stack = []
        self.redo_stack = []

        for seq in ("<Control-z>", "<Control-Z>"):
            self.root.bind_all(seq, self.undo)
        for seq in ("<Control-y>", "<Control-Y>", "<Shift-Control-Z>", "<Shift-Control-z>"):
            self.root.bind_all(seq, self.redo)

        # take an initial snapshot
        self._push_undo(clear_redo=False)


    # ---------- Right-side UI ----------
    def build_right_panel(self):
        # Table (header changed to "Criteria Score")
        table = tk.Frame(self.side_panel)
        table.pack(anchor="n", fill="x")

        header = tk.Label(table, text="Criteria Score", font=("Arial", 11, "bold"))
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0,6))

        criteria = ["Environmental", "Economical", "Safety/Constructability"]
        self.criteria_vars = {}
        for i, name in enumerate(criteria, start=1):
            tk.Label(table, text=name, anchor="w").grid(row=i, column=0, sticky="w", padx=(0,6), pady=3)
            var = tk.StringVar(value="—")
            self.criteria_vars[name] = var
            tk.Label(table, textvariable=var, relief=tk.SUNKEN, width=20, anchor="e").grid(row=i, column=1, sticky="e", pady=3)

        # Inputs
        inputs = tk.Frame(self.side_panel)
        inputs.pack(anchor="n", fill="x", pady=(12,0))

        # Budget
        tk.Label(inputs, text="Budget (AUD)").grid(row=0, column=0, sticky="w", pady=3)
        self.budget_var = tk.StringVar()
        e_budget = tk.Entry(inputs, textvariable=self.budget_var)
        e_budget.grid(row=0, column=1, sticky="ew", pady=3)

        # Duration (months)
        tk.Label(inputs, text="Duration (months)").grid(row=1, column=0, sticky="w", pady=3)
        self.duration_var = tk.StringVar()
        e_duration = tk.Entry(inputs, textvariable=self.duration_var)
        e_duration.grid(row=1, column=1, sticky="ew", pady=3)

        # Hired Equipment (Y/N)
        tk.Label(inputs, text="Hired Equipment (Y/N)").grid(row=2, column=0, sticky="w", pady=3)
        self.hired_var = tk.StringVar(value="N")
        radios = tk.Frame(inputs)
        radios.grid(row=2, column=1, sticky="w", pady=3)
        tk.Radiobutton(radios, text="Y", variable=self.hired_var, value="Y", command=self.recompute_financials).pack(side=tk.LEFT, padx=(0,8))
        tk.Radiobutton(radios, text="N", variable=self.hired_var, value="N", command=self.recompute_financials).pack(side=tk.LEFT)

        # Total Spent (computed, not an input) — placed directly below Hired Equipment
        tk.Label(inputs, text="Total Spent (AUD)").grid(row=3, column=0, sticky="w", pady=(6,3))
        self.total_spent_var = tk.StringVar(value="—")
        tk.Label(inputs, textvariable=self.total_spent_var, relief=tk.SUNKEN, width=20, anchor="e").grid(row=3, column=1, sticky="ew", pady=(6,3))

        inputs.grid_columnconfigure(1, weight=1)

        # ---- Costs per week per tower ----
        costs = tk.LabelFrame(self.side_panel, text="Weekly Costs per Tower (AUD)")
        costs.pack(anchor="n", fill="x", pady=(12,0))

        self.cost_vars = {}  # (type) -> (running_var, hire_var)
        row = 0
        tk.Label(costs, text="Type").grid(row=row, column=0, sticky="w")
        tk.Label(costs, text="Running / wk").grid(row=row, column=1, sticky="e")
        tk.Label(costs, text="Hire / wk").grid(row=row, column=2, sticky="e")
        row += 1
        for t in ["Diesel", "Hydrogen", "Solar", "Biodiesel"]:
            tk.Label(costs, text=t).grid(row=row, column=0, sticky="w", pady=2)
            rv = tk.StringVar(value=str(self.weekly_running_costs[t]))
            hv = tk.StringVar(value=str(self.weekly_hire_costs[t]))
            er = tk.Entry(costs, textvariable=rv, width=10)
            eh = tk.Entry(costs, textvariable=hv, width=10)
            er.grid(row=row, column=1, sticky="e", padx=4)
            eh.grid(row=row, column=2, sticky="e", padx=4)
            # trace recompute on change
            rv.trace_add("write", lambda *args: self.recompute_financials())
            hv.trace_add("write", lambda *args: self.recompute_financials())
            self.cost_vars[t] = (rv, hv)
            row += 1

        # Trace budget/duration
        self.budget_var.trace_add("write", lambda *args: self.recompute_financials())
        self.duration_var.trace_add("write", lambda *args: self.recompute_financials())
        
        #Export to PDF
    def export_pdf(self)
        self

        #Undo - redo
    def _snapshot(self):
        return {
            "points": [tuple(p) for p in self.points],
            "shape_complete": self.shape_complete,
            "lights": [dict(L) for L in self.lights],
            "scale_factor": self.scale_factor,
            "zoom_level": self.zoom_level,
            "offset_x": self.offset_x,
            "offset_y": self.offset_y,
        }

    def _restore(self, s):
        self.points = [tuple(p) for p in s.get("points", [])]
        self.shape_complete = bool(s.get("shape_complete", False))
        self.lights = [dict(L) for L in s.get("lights", [])]
        self.scale_factor = float(s.get("scale_factor", self.scale_factor))
        self.zoom_level = float(s.get("zoom_level", self.zoom_level))
        self.offset_x = float(s.get("offset_x", self.offset_x))
        self.offset_y = float(s.get("offset_y", self.offset_y))
        self.update_environmental_score()
        self.recompute_financials()
        self.rescale_background()
        self.redraw()

    def _push_undo(self, clear_redo=True):
        if len(self.undo_stack) > 300:
            self.undo_stack.pop(0)
        self.undo_stack.append(self._snapshot())
        if clear_redo:
            self.redo_stack.clear()

    def undo(self, event=None):
        if not self.undo_stack:
            return
        # move current to redo, restore last undo
        self.redo_stack.append(self._snapshot())
        state = self.undo_stack.pop()
        self._restore(state)

    def redo(self, event=None):
        if not self.redo_stack:
            return
        # move current to undo, restore last redo
        self.undo_stack.append(self._snapshot())
        state = self.redo_stack.pop()
        self._restore(state)
        






    # ---------- Canvas tools ----------
    def activate_place_points(self):
        self.canvas.config(cursor="arrow")
        self.placing_light = False
        self.canvas.bind("<Button-1>", self.add_point)

    def activate_light_mode(self):
        self.placing_light = True
        try:
            self.canvas.config(cursor="circle")
        except Exception:
            self.canvas.config(cursor="crosshair")
        self.canvas.bind("<Button-1>", self.place_light)

    def place_light(self, event):
        if not self.placing_light:
            return
        self._push_undo()
        x = (event.x - self.offset_x) / self.zoom_level
        y = (event.y - self.offset_y) / self.zoom_level
        ltype = self.light_type.get()
        color = self.light_colors.get(ltype, "gray")
        self.lights.append({"x": x, "y": y, "type": ltype, "color": color})
        self.update_environmental_score()
        self.recompute_financials()
        self.redraw()

    def update_environmental_score(self):
        """Environmental total = avg(source scores) + avg(efficiency scores) over all placed lights."""
        if not self.lights:
            self.criteria_vars["Environmental"].set("—")
            return
        src_vals, eff_vals = [], []
        for L in self.lights:
            scores = self.light_scores.get(L["type"])
            if scores:
                s, e = scores
                src_vals.append(s); eff_vals.append(e)
        if not src_vals or not eff_vals:
            self.criteria_vars["Environmental"].set("—")
            return
        total = (sum(src_vals)/len(src_vals)) + (sum(eff_vals)/len(eff_vals))
        self.criteria_vars["Environmental"].set(f"{total:.3f}")

    # ---- Financials ----
    def parse_float(self, s):
        try:
            return float(str(s).strip())
        except Exception:
            return 0.0

    def compute_total_spent(self):
        # count lights by type
        counts = {"Diesel":0, "Hydrogen":0, "Solar":0, "Biodiesel":0}
        for L in self.lights:
            t = L["type"]
            if t in counts:
                counts[t] += 1

        months = self.parse_float(self.duration_var.get())
        weeks = months * 4.0  # assume 4 weeks per month

        hired = (self.hired_var.get().upper() == "Y")

        # Sum weekly costs across all towers
        weekly_total = 0.0
        for t, n in counts.items():
            rv = self.parse_float(self.cost_vars[t][0].get())  # running
            hv = self.parse_float(self.cost_vars[t][1].get())  # hire
            per_tower_week = rv + (hv if hired else 0.0)
            weekly_total += n * per_tower_week

        return weeks * weekly_total

    def recompute_financials(self):
        spent = self.compute_total_spent()
        # Update total spent label
        if spent > 0:
            self.total_spent_var.set(f"{spent:,.2f}")
        else:
            self.total_spent_var.set("—")

        # Economical score
        budget = self.parse_float(self.budget_var.get())
        econ = None
        if spent > 0 and budget > 0:
            if spent > budget: # overspent
                ##econ = 1 - (budget / spent) #check with team
                econ = (budget/spent)**0.5
            else: # underspent or exactly on budget
                econ = 1 + (spent / budget)
                if econ > 2:
                    econ = 2.0
        elif budget > 0 and spent == 0:
            # nothing placed yet; treat as neutral
            econ = 1.0

        if econ is None:
            self.criteria_vars["Economical"].set("—")
        else:
            self.criteria_vars["Economical"].set(f"{econ:.3f}")

    def draw_lights(self):
        overlay = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        influence_radius_m = 20  # meters
        radius_px_nominal = influence_radius_m * self.scale_factor

        for L in self.lights:
            sx = L["x"] * self.zoom_level + self.offset_x
            sy = L["y"] * self.zoom_level + self.offset_y
            r = 5
            self.canvas.create_oval(sx - r, sy - r, sx + r, sy + r, fill=L["color"], outline="black")
            radius_px = radius_px_nominal * self.zoom_level
            draw.ellipse([sx - radius_px, sy - radius_px, sx + radius_px, sy + radius_px],
                         fill=(255, 255, 0, 80))

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
        self._push_undo()
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
            self._push_undo() 
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
        self._push_undo()
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
            self._push_undo()
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
        # draw lights & translucent radii
        self.draw_lights()

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
        self.canvas.create_rectangle(5, 5, 180, 30, fill='white', outline='gray')
        self.canvas.create_text(10, 10, anchor="nw", text=f"Area: {area_m2:.2f} m²", fill="blue", font=("Arial", 14))

    def complete_shape(self):
        if len(self.points) < 3:
            messagebox.showinfo("Info", "At least 3 points required to complete shape.")
            return
        self._push_undo()
        self.shape_complete = True
        self.redraw()

    def clear_canvas(self):
        self._push_undo()
        self.points = []
        self.shape_complete = False
        self.lights = []
        self.canvas.delete("all")
        self.update_environmental_score()
        self.recompute_financials()
        self.redraw()

if __name__ == "__main__":
    root = tk.Tk()
    app = ShapeDrawer(root)
    root.mainloop()
