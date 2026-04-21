##
# @file calc.py
# @brief Westernová kalkulačka s GUI v Tkinter
# @author Daniel Baloun xbaloud00

import tkinter as tk
from tkinter import font as tkfont
import mathematic as math_lib

# ============================================================
# Stav kalkulačky
# ============================================================
current_input = ""
first_value = None
operator = None
just_calculated = False

# ============================================================
# Logika
# ============================================================
def format_result(n):
    if isinstance(n, float) and n.is_integer():
        return str(int(n))
    return str(round(n, 10)).rstrip('0').rstrip('.')

def update_display(val, error=False):
    display_var.set(val)
    if error:
        display_label.config(fg="#ff6b6b")
    else:
        display_label.config(fg="#f5c518")

def handle_button(label):
    global current_input, first_value, operator, just_calculated

    try:
        if label in "0123456789":
            if just_calculated:
                current_input = ""
                just_calculated = False
            if current_input == "0":
                current_input = label
            else:
                current_input += label
            update_display(current_input)
            expr_var.set("")

        elif label == ".":
            if just_calculated:
                current_input = "0"
                just_calculated = False
            if "." not in current_input:
                current_input = (current_input or "0") + "."
                update_display(current_input)

        elif label == "⌫":
            current_input = current_input[:-1] or "0"
            update_display(current_input)

        elif label == "C":
            current_input = ""
            first_value = None
            operator = None
            just_calculated = False
            update_display("0")
            expr_var.set("")

        elif label == "n!":
            val = int(float(current_input or "0"))
            result = math_lib.factorial(val)
            expr_var.set(f"{val}! =")
            current_input = format_result(result)
            update_display(current_input)
            just_calculated = True

        elif label == "|x|":
            val = float(current_input or "0")
            result = math_lib.absolute_value(val)
            expr_var.set(f"|{val}| =")
            current_input = format_result(result)
            update_display(current_input)
            just_calculated = True

        elif label in ("+", "-", "×", "÷", "^", "√"):
            if operator and current_input and not just_calculated:
                calculate()
            first_value = float(current_input or display_var.get() or "0")
            operator = label
            current_input = ""
            just_calculated = False
            expr_var.set(f"{first_value} {label}")
            update_display(label)

        elif label == "=":
            calculate()
            just_calculated = True

    except ZeroDivisionError:
        update_display("Dělení nulou!", error=True)
        expr_var.set("")
        current_input = ""
        first_value = None
        operator = None
    except ValueError as e:
        update_display(str(e), error=True)
        expr_var.set("")
        current_input = ""
        first_value = None
        operator = None

def calculate():
    global current_input, first_value, operator
    second = float(current_input or display_var.get() or "0")
    a = first_value if first_value is not None else 0
    op = operator

    expr_var.set(f"{a} {op} {second} =")

    if op == "+":       result = math_lib.add(a, second)
    elif op == "-":     result = math_lib.subtract(a, second)
    elif op == "×":     result = math_lib.multiply(a, second)
    elif op == "÷":     result = math_lib.divide(a, second)
    elif op == "^":     result = math_lib.power(a, second)
    elif op == "√":     result = math_lib.root(a, second)
    else:               result = second

    current_input = format_result(result)
    first_value = None
    operator = None
    update_display(current_input)

# ============================================================
# Klávesnice
# ============================================================
def on_key(event):
    key_map = {
        "0":"0","1":"1","2":"2","3":"3","4":"4",
        "5":"5","6":"6","7":"7","8":"8","9":"9",
        "+":"+","-":"-","*":"×","/":"÷","^":"^",
        "=":"=","Return":"=","BackSpace":"⌫","Escape":"C",".":"."
    }
    if event.keysym in key_map:
        handle_button(key_map[event.keysym])
    elif event.char in key_map:
        handle_button(key_map[event.char])

# ============================================================
# GUI
# ============================================================
root = tk.Tk()
root.title("🤠 Western Kalkulačka")
root.resizable(False, False)
root.configure(bg="#3d1f00")

# Barvy
WOOD       = "#3d1f00"
WOOD_LIGHT = "#6b3a1f"
GOLD       = "#c8960c"
GOLD_BRIGHT= "#f5c518"
PARCHMENT  = "#f2e8c9"
LEATHER    = "#8b4513"
BTN_NUM    = "#c8930c"
BTN_OP     = "#7a5030"
BTN_EQ     = "#2d5a1b"
BTN_CLEAR  = "#7a2020"
BTN_SPEC   = "#4a5a7a"

# Outer frame — dřevo
outer = tk.Frame(root, bg=WOOD_LIGHT, bd=6, relief="ridge")
outer.pack(padx=14, pady=14)

# Gold border
gold_frame = tk.Frame(outer, bg=GOLD, bd=3)
gold_frame.pack(padx=2, pady=2)

# Parchment inner
inner = tk.Frame(gold_frame, bg=PARCHMENT, padx=18, pady=16)
inner.pack()

# Title
tk.Label(inner, text="★   W A N T E D   ★", bg=PARCHMENT, fg=WOOD_LIGHT,
         font=("Georgia", 9, "italic")).pack()

tk.Label(inner, text="CALC·U·LATOR", bg=PARCHMENT, fg=WOOD,
         font=("Georgia", 26, "bold")).pack(pady=(0,2))

tk.Label(inner, text="Dead or Alive  ·  Est. 1876", bg=PARCHMENT, fg=LEATHER,
         font=("Georgia", 8, "italic")).pack(pady=(0,10))

# Display frame
disp_outer = tk.Frame(inner, bg=GOLD, bd=2)
disp_outer.pack(fill="x", pady=(0,12))

disp_inner = tk.Frame(disp_outer, bg="#0d0800", padx=10, pady=8)
disp_inner.pack(fill="x", padx=2, pady=2)

expr_var = tk.StringVar(value="")
tk.Label(disp_inner, textvariable=expr_var, bg="#0d0800", fg="#7a5500",
         font=("Courier", 10), anchor="e").pack(fill="x")

display_var = tk.StringVar(value="0")
display_label = tk.Label(disp_inner, textvariable=display_var,
                          bg="#0d0800", fg=GOLD_BRIGHT,
                          font=("Courier", 28, "bold"), anchor="e")
display_label.pack(fill="x")

# Divider
tk.Label(inner, text="─── ✦ ───", bg=PARCHMENT, fg=GOLD,
         font=("Georgia", 11)).pack(pady=(0,10))

# Buttons
btn_frame = tk.Frame(inner, bg=PARCHMENT)
btn_frame.pack()

def make_btn(parent, label, color, row, col, colspan=1):
    """Vytvoří westernové tlačítko se hvězdičkou v pozadí"""

    # Canvas pro hvězdičku
    w = 68 * colspan + (colspan - 1) * 6
    h = 62
    c = tk.Canvas(parent, width=w, height=h,
                  bg=PARCHMENT, highlightthickness=0, bd=0)
    c.grid(row=row, column=col, columnspan=colspan,
           padx=3, pady=3, sticky="nsew")

    # Nakresli hvězdičku
    cx, cy, r = w // 2, h // 2, min(w, h) // 2 - 3
    import math
    points = []
    inner_r = r * 0.42
    for i in range(10):
        angle = math.radians(i * 36 - 90)
        radius = r if i % 2 == 0 else inner_r
        points.append(cx + radius * math.cos(angle))
        points.append(cy + radius * math.sin(angle))

    # Stín
    shadow = [p + 2 for p in points]
    c.create_polygon(shadow, fill="#1a0a00", outline="", smooth=False)
    # Hvězdička
    c.create_polygon(points, fill=color, outline=WOOD, width=1.5, smooth=False)
    # Světlý okraj
    import colorsys
    r_hex = int(color[1:3], 16) / 255
    g_hex = int(color[3:5], 16) / 255
    b_hex = int(color[5:7], 16) / 255
    h2, s2, v2 = colorsys.rgb_to_hsv(r_hex, g_hex, b_hex)
    v2 = min(1.0, v2 * 1.4)
    r2, g2, b2 = colorsys.hsv_to_rgb(h2, s2 * 0.6, v2)
    light_color = "#{:02x}{:02x}{:02x}".format(int(r2*255), int(g2*255), int(b2*255))

    # Text
    c.create_text(cx, cy, text=label,
                  font=("Georgia", 16 if len(label) <= 2 else 12, "bold"),
                  fill=PARCHMENT if color != BTN_NUM else WOOD)

    # Hover a click efekty
    def on_enter(e):
        c.delete("all")
        shadow2 = [p + 2 for p in points]
        c.create_polygon(shadow2, fill="#1a0a00", outline="", smooth=False)
        bright = []
        for i in range(10):
            angle = math.radians(i * 36 - 90)
            rad = (r + 2) if i % 2 == 0 else (inner_r + 1)
            bright.append(cx + rad * math.cos(angle))
            bright.append(cy + rad * math.sin(angle))
        c.create_polygon(bright, fill=light_color, outline=WOOD, width=1.5)
        c.create_text(cx, cy, text=label,
                      font=("Georgia", 16 if len(label) <= 2 else 12, "bold"),
                      fill=PARCHMENT if color != BTN_NUM else WOOD)

    def on_leave(e):
        c.delete("all")
        shadow3 = [p + 2 for p in points]
        c.create_polygon(shadow3, fill="#1a0a00", outline="", smooth=False)
        c.create_polygon(points, fill=color, outline=WOOD, width=1.5)
        c.create_text(cx, cy, text=label,
                      font=("Georgia", 16 if len(label) <= 2 else 12, "bold"),
                      fill=PARCHMENT if color != BTN_NUM else WOOD)

    def on_click(e):
        handle_button(label)

    c.bind("<Enter>", on_enter)
    c.bind("<Leave>", on_leave)
    c.bind("<Button-1>", on_click)

# Layout tlačítek: (label, barva, řádek, sloupec, colspan)
buttons = [
    ("C",   BTN_CLEAR, 0, 0), ("|x|", BTN_SPEC,  0, 1),
    ("n!",  BTN_SPEC,  0, 2), ("÷",   BTN_OP,    0, 3),
    ("7",   BTN_NUM,   1, 0), ("8",   BTN_NUM,   1, 1),
    ("9",   BTN_NUM,   1, 2), ("×",   BTN_OP,    1, 3),
    ("4",   BTN_NUM,   2, 0), ("5",   BTN_NUM,   2, 1),
    ("6",   BTN_NUM,   2, 2), ("-",   BTN_OP,    2, 3),
    ("1",   BTN_NUM,   3, 0), ("2",   BTN_NUM,   3, 1),
    ("3",   BTN_NUM,   3, 2), ("+",   BTN_OP,    3, 3),
    ("^",   BTN_SPEC,  4, 0), ("√",   BTN_SPEC,  4, 1),
    (".",   BTN_SPEC,  4, 2), ("⌫",   BTN_SPEC,  4, 3),
]

for label, color, row, col in buttons:
    make_btn(btn_frame, label, color, row, col)

# 0 a = přes 2 sloupce
make_btn(btn_frame, "0", BTN_NUM, 5, 0, colspan=2)
make_btn(btn_frame, "=", BTN_EQ,  5, 2, colspan=2)

# Tagline
tk.Label(inner, text="~ Fastest Calculations in the West ~",
         bg=PARCHMENT, fg=LEATHER,
         font=("Georgia", 8, "italic")).pack(pady=(12, 0))

# Klávesnice
root.bind("<Key>", on_key)

root.mainloop()