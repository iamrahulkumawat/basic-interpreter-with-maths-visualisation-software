import tkinter as tk
from tkinter import ttk, messagebox
from interpreter import evaluate_expression

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.tip_text = text
        self.tip_window = None

    def show_tip(self):
        if self.tip_window or not self.tip_text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.tip_text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1, font=("Helvetica", 10))
        label.pack(ipadx=2)

    def hide_tip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

def draw_line():
    try:
        slope = float(slope_entry.get())
        intercept = float(intercept_entry.get())
        x1, y1 = -10, slope * -10 + intercept
        x2, y2 = 10, slope * 10 + intercept
        canvas.delete("line")
        canvas.create_line(x_to_pixel(x1), y_to_pixel(y1), x_to_pixel(x2), y_to_pixel(y2), fill="#FF6D00", width=2, tags="line", smooth=True)
    except Exception as e:
        messagebox.showerror("Error", "Invalid input for slope/intercept.")
        

def on_submit_expression():
    expression = expression_entry.get()
    try:
        result = evaluate_expression(expression)
        result_label.config(text=f"Result: {result}")
    except Exception as e:
        messagebox.showerror("Error", "Invalid math expression.")

def x_to_pixel(x):
    return canvas_width / 2 + x * scale_factor

def y_to_pixel(y):
    return canvas_height / 2 - y * scale_factor

def on_draw_hover(event):
    draw_button_style.configure('Draw.TButton', foreground="#448AFF")

def on_draw_leave(event):
    draw_button_style.configure('Draw.TButton', foreground="#FFFFFF")

def on_submit_hover(event):
    submit_button_style.configure('Submit.TButton', foreground="#448AFF")

def on_submit_leave(event):
    submit_button_style.configure('Submit.TButton', foreground="#FFFFFF")

root = tk.Tk()
root.title("Basic Calculator and Line Drawer")

root.configure(bg="#1C2331")
style = ttk.Style()
style.theme_use("clam")
style.configure(".", font=("Helvetica", 14), foreground="#FFFFFF", background="#1C2331")
style.configure("TLabel", foreground="#FFFFFF", background="#1C2331")
style.configure("TButton", font=("Helvetica", 14), foreground="#FFFFFF", background="#303F9F")

draw_button_style = ttk.Style()
draw_button_style.configure('Draw.TButton', font=("Helvetica", 14), foreground="#FFFFFF", background="#303F9F")
submit_button_style = ttk.Style()
submit_button_style.configure('Submit.TButton', font=("Helvetica", 14), foreground="#FFFFFF", background="#303F9F")


# Expression Code
expression_frame = ttk.Frame(root, padding="10", style='DarkFrame.TFrame')
expression_frame.pack(pady=10)
expression_label = ttk.Label(expression_frame, text="Enter math expression:", foreground="white", background="#303030")
expression_label.grid(row=0, column=0, padx=5, pady=5)
expression_entry = ttk.Entry(expression_frame, width=30, font=("Helvetica", 14), foreground="black")
expression_entry.grid(row=0, column=1, padx=5, pady=5)
submit_button = ttk.Button(expression_frame, text="Submit", command=on_submit_expression, cursor="hand2", style='Submit.TButton')
submit_button.grid(row=0, column=2, padx=5, pady=5)
submit_button.bind("<Enter>", on_submit_hover)
submit_button.bind("<Leave>", on_submit_leave)

result_label = ttk.Label(expression_frame, text="Result: ", font=("Helvetica", 14), foreground="white", background="#303030")
result_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

# Line drawer
line_frame = ttk.Frame(root, padding="10", style='DarkFrame.TFrame')
line_frame.pack(pady=10)
slope_label = ttk.Label(line_frame, text="Enter slope:", font=("Helvetica", 14), foreground="white", background="#303030")
slope_label.grid(row=0, column=0, padx=5, pady=5)
slope_entry = ttk.Entry(line_frame, width=10, font=("Helvetica", 14), foreground="black")
slope_entry.grid(row=0, column=1, padx=5, pady=5)
intercept_label = ttk.Label(line_frame, text="Enter intercept:", font=("Helvetica", 14), foreground="white", background="#303030")
intercept_label.grid(row=0, column=2, padx=5, pady=5)
intercept_entry = ttk.Entry(line_frame, width=10, font=("Helvetica", 14), foreground="black")
intercept_entry.grid(row=0, column=3, padx=5, pady=5)
draw_button = ttk.Button(line_frame, text="Draw Line", command=draw_line, cursor="hand2", style='Draw.TButton')
draw_button.grid(row=0, column=4, padx=5, pady=5)
draw_button.bind("<Enter>", on_draw_hover)
draw_button.bind("<Leave>", on_draw_leave)
draw_button_tip = ToolTip(draw_button, "Draw a line using the given slope and intercept.")

# Canvas
canvas_width = 400
canvas_height = 400
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="#212121")
canvas.pack()
canvas.create_line(0, canvas_height/2, canvas_width, canvas_height/2, fill="#BDBDBD", width=1)
canvas.create_line(canvas_width/2, 0, canvas_width/2, canvas_height, fill="#BDBDBD", width=1)
scale_factor = 20
for x in range(-200, 201, 20):
    canvas.create_line(x_to_pixel(x), 0, x_to_pixel(x), canvas_height, fill="#424242")
for y in range(-200, 201, 20):
    canvas.create_line(0, y_to_pixel(y), canvas_width, y_to_pixel(y), fill="#424242")

root.mainloop()
