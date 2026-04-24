##
# @file calc.py
# @brief Westernová kalkulačka v2.0 — GUI v Tkinter
# @author Daniel Baloun xbaloud00

import tkinter as tk
import math
import mathematic as math_lib
import colorsys, os, ctypes, wave, struct, random, tempfile

try:
    import winsound
    WINSOUND_AVAILABLE = True
except ImportError:
    WINSOUND_AVAILABLE = False

# ══════════════════════════════════════════════════════════════
#  KONFIGURACE
# ══════════════════════════════════════════════════════════════
MUSIC_FILENAME = "western_boogie.mp3"
MUSIC_VOLUME   = 300
GUNSHOT_FILES  = ["shot1.wav", "shot2.wav", "shot3.wav"]

_BASE = os.path.dirname(os.path.abspath(__file__))
def _path(f): return os.path.join(_BASE, f)

# ══════════════════════════════════════════════════════════════
#  BARVY
# ══════════════════════════════════════════════════════════════
WOOD        = "#3d1f00"
WOOD_LIGHT  = "#6b3a1f"
GOLD        = "#c8960c"
GOLD_BRIGHT = "#f5c518"
PARCHMENT   = "#f2e8c9"
LEATHER     = "#8b4513"
BTN_NUM     = "#c8930c"
BTN_OP      = "#7a5030"
BTN_EQ      = "#2d5a1b"
BTN_CLEAR   = "#7a2020"
BTN_SPEC    = "#4a5a7a"
BTN_MEM     = "#5a3a6a"
BTN_SCI     = "#3a4a6a"
BTN_CONST   = "#1a4a3a"
BTN_NEW     = "#3a2a5a"
BTN_DISABLED= "#5a5050"   # šedá — tlačítka bez logiky

# ══════════════════════════════════════════════════════════════
#  ZVUKY VÝSTŘELŮ
# ══════════════════════════════════════════════════════════════
_shot_paths = []
_gen_temps  = []
_last_shot  = -1

def _generate_shot_wav(variation):
    sample_rate = 44100
    n = int(sample_rate * 0.4)
    params = [
        dict(crack=0.90, cd=20, freq=60,  ba=0.50, bd=8),
        dict(crack=0.65, cd=10, freq=45,  ba=0.80, bd=6),
        dict(crack=0.75, cd=25, freq=90,  ba=0.35, bd=12),
    ]
    p = params[variation % 3]
    rng = random.Random(variation * 7919)
    samples = []
    for i in range(n):
        t = i / sample_rate
        c = (rng.random()*2-1) * math.exp(-t*p["cd"]) * p["crack"]
        b = math.sin(2*math.pi*p["freq"]*t) * math.exp(-t*p["bd"]) * p["ba"]
        m = (rng.random()*2-1) * math.exp(-t*40) * 0.3
        samples.append(int(max(-1.0, min(1.0, c+b+m)) * 32767))
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    with wave.open(tmp.name, 'w') as wf:
        wf.setnchannels(1); wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(struct.pack(f'<{n}h', *samples))
    return tmp.name

def _init_shots():
    global _shot_paths, _gen_temps
    for i, fn in enumerate(GUNSHOT_FILES):
        p = _path(fn)
        if os.path.exists(p):
            _shot_paths.append(p)
        else:
            g = _generate_shot_wav(i)
            _shot_paths.append(g)
            _gen_temps.append(g)

def play_gunshot():
    global _last_shot
    if not WINSOUND_AVAILABLE or not _shot_paths: return
    pool = [i for i in range(len(_shot_paths)) if i != _last_shot] if len(_shot_paths) > 1 else [0]
    idx = random.choice(pool)
    _last_shot = idx
    try:
        winsound.PlaySound(_shot_paths[idx],
            winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
    except Exception: pass

# ══════════════════════════════════════════════════════════════
#  HUDBA (Windows MCI)
# ══════════════════════════════════════════════════════════════
_music_path   = _path(MUSIC_FILENAME)
music_playing = False
_winmm        = ctypes.windll.winmm if hasattr(ctypes, "windll") else None

def _mci(cmd):
    if _winmm: _winmm.mciSendStringW(cmd, None, 0, None)

def _init_music():
    global music_playing
    if not _winmm or not os.path.exists(_music_path): return
    try:
        _mci(f'open "{_music_path}" type mpegvideo alias bgmusic')
        _mci(f"setaudio bgmusic volume to {MUSIC_VOLUME}")
        _mci("play bgmusic repeat")
        music_playing = True
    except Exception as e: print(f"Hudba: {e}")

def _cleanup():
    _mci("stop bgmusic"); _mci("close bgmusic")
    for p in _gen_temps:
        try: os.unlink(p)
        except: pass

def toggle_music(event=None):
    global music_playing
    if not _winmm: return
    if music_playing:
        _mci("pause bgmusic"); music_playing = False
        music_note_label.config(fg="#6b5a3e"); note_status.config(text="OFF")
    else:
        _mci("resume bgmusic"); music_playing = True
        music_note_label.config(fg=GOLD_BRIGHT); note_status.config(text="")

# ══════════════════════════════════════════════════════════════
#  STAV KALKULAČKY
# ══════════════════════════════════════════════════════════════
current_input   = ""
first_value     = None
operator        = None
just_calculated = False

# ══════════════════════════════════════════════════════════════
#  LOGIKA (beze změny oproti v1)
# ══════════════════════════════════════════════════════════════
def format_result(n):
    if isinstance(n, float) and n.is_integer():
        return str(int(n))
    return str(round(n, 10)).rstrip('0').rstrip('.')

def update_display(val, error=False):
    display_var.set(val)
    display_label.config(fg="#ff6b6b" if error else GOLD_BRIGHT)

def handle_button(label):
    global current_input, first_value, operator, just_calculated
    play_gunshot()
    try:
        if label in "0123456789":
            if just_calculated:
                current_input = ""
                just_calculated = False
            current_input = label if current_input == "0" else current_input + label
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
        expr_var.set(""); current_input = ""; first_value = None; operator = None
    except ValueError as e:
        update_display(str(e), error=True)
        expr_var.set(""); current_input = ""; first_value = None; operator = None

def calculate():
    global current_input, first_value, operator
    second = float(current_input or display_var.get() or "0")
    a, op  = (first_value if first_value is not None else 0), operator
    expr_var.set(f"{a} {op} {second} =")
    if op == "+":   result = math_lib.add(a, second)
    elif op == "-": result = math_lib.subtract(a, second)
    elif op == "×": result = math_lib.multiply(a, second)
    elif op == "÷": result = math_lib.divide(a, second)
    elif op == "^": result = math_lib.power(a, second)
    elif op == "√": result = math_lib.root(a, second)
    else:           result = second
    current_input = format_result(result)
    first_value = None; operator = None
    update_display(current_input)

# ══════════════════════════════════════════════════════════════
#  KLÁVESNICE
# ══════════════════════════════════════════════════════════════
def on_key(event):
    key_map = {
        "0":"0","1":"1","2":"2","3":"3","4":"4",
        "5":"5","6":"6","7":"7","8":"8","9":"9",
        "+":"+","-":"-","*":"×","/":"÷","^":"^",
        "=":"=","Return":"=","BackSpace":"⌫","Escape":"C",".":"."
    }
    k = event.keysym if event.keysym in key_map else event.char
    if k in key_map: handle_button(key_map[k])

# ══════════════════════════════════════════════════════════════
#  GUI — ROOT
# ══════════════════════════════════════════════════════════════
root = tk.Tk()
root.title("🤠 Western Kalkulačka v2.0")
root.resizable(False, False)
root.configure(bg=WOOD)

# Rámce
outer = tk.Frame(root, bg=WOOD_LIGHT, bd=4, relief="ridge")
outer.pack(padx=6, pady=6)
gold_frame = tk.Frame(outer, bg=GOLD, bd=2)
gold_frame.pack(padx=2, pady=2)
inner = tk.Frame(gold_frame, bg=PARCHMENT, padx=8, pady=6)
inner.pack()

# ── Notička ───────────────────────────────────────────────
topbar = tk.Frame(inner, bg=PARCHMENT)
topbar.pack(fill="x")
tk.Label(topbar, bg=PARCHMENT, width=3).pack(side="left")
note_frame = tk.Frame(topbar, bg=PARCHMENT, cursor="hand2")
note_frame.pack(side="right")
music_note_label = tk.Label(note_frame, text="♪", bg=PARCHMENT, fg=GOLD_BRIGHT,
                             font=("Georgia", 20, "bold"), cursor="hand2")
music_note_label.pack(side="left")
note_status = tk.Label(note_frame, text="", bg=PARCHMENT, fg="#6b5a3e",
                        font=("Georgia", 8), cursor="hand2")
note_status.pack(side="left", pady=(8, 0))
for w in (note_frame, music_note_label, note_status):
    w.bind("<Button-1>", toggle_music)
music_note_label.bind("<Enter>", lambda e: music_note_label.config(font=("Georgia", 23, "bold")))
music_note_label.bind("<Leave>", lambda e: music_note_label.config(font=("Georgia", 20, "bold")))

# ── Titulky ───────────────────────────────────────────────
tk.Label(inner, text="★  W A N T E D  ★", bg=PARCHMENT, fg=WOOD_LIGHT,
         font=("Georgia", 8, "italic")).pack()
tk.Label(inner, text="CALC·U·LATOR", bg=PARCHMENT, fg=WOOD,
         font=("Georgia", 20, "bold")).pack(pady=(0, 1))
tk.Label(inner, text="Dead or Alive · Est. 1876 · v2.0", bg=PARCHMENT, fg=LEATHER,
         font=("Georgia", 7, "italic")).pack(pady=(0, 4))

# ── Záložky módů ──────────────────────────────────────────
MODE_LABELS   = ["BASIC", "SCIENTIFIC", "GRAPH", "CONVERT"]
current_mode  = tk.StringVar(value="SCIENTIFIC")
mode_tab_btns = {}

tabs_frame = tk.Frame(inner, bg=WOOD_LIGHT, bd=1, relief="solid")
tabs_frame.pack(fill="x", pady=(0, 6))

def set_mode(mode):
    current_mode.set(mode)
    for m, btn in mode_tab_btns.items():
        if m == mode:
            btn.config(bg=WOOD, fg=GOLD_BRIGHT, relief="sunken")
        else:
            btn.config(bg=WOOD_LIGHT, fg=PARCHMENT, relief="flat")
    # Sci rows: видно только в SCIENTIFIC
    if mode == "SCIENTIFIC":
        sci_frame.pack(before=divider_label, fill="x", pady=(0, 4))
    else:
        sci_frame.pack_forget()

for m in MODE_LABELS:
    b = tk.Label(tabs_frame, text=m, bg=WOOD_LIGHT, fg=PARCHMENT,
                 font=("Georgia", 7, "bold"), padx=8, pady=3, cursor="hand2")
    b.pack(side="left", expand=True, fill="x")
    b.bind("<Button-1>", lambda e, mm=m: set_mode(mm))
    mode_tab_btns[m] = b

# ── Dvojsloupcový layout ───────────────────────────────────
columns = tk.Frame(inner, bg=PARCHMENT)
columns.pack()

left  = tk.Frame(columns, bg=PARCHMENT)
left.pack(side="left", padx=(0, 6))

right = tk.Frame(columns, bg=PARCHMENT)
right.pack(side="left", fill="y")

# ══════════════════════════════════════════════════════════════
#  LEVÝ SLOUPEC
# ══════════════════════════════════════════════════════════════

# ── Display ───────────────────────────────────────────────
disp_outer = tk.Frame(left, bg=GOLD, bd=2)
disp_outer.pack(fill="x", pady=(0, 8))
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

# Indikátory DEG/RAD a paměti (zatím jen vizuál)
badge_row = tk.Frame(disp_inner, bg="#0d0800")
badge_row.pack(fill="x", pady=(4, 0))

def _badge(parent, text, active=False):
    fg = GOLD_BRIGHT if active else "#7a5500"
    bd = tk.Label(parent, text=text, bg="#0d0800", fg=fg,
                  font=("Courier", 9), relief="flat",
                  padx=5, pady=1, bd=1)
    bd.pack(side="left", padx=(0, 3))
    return bd

deg_badge = _badge(badge_row, "DEG", active=True)
rad_badge = _badge(badge_row, "RAD", active=False)
mem_badge = _badge(badge_row, "M: —", active=False)

# ══════════════════════════════════════════════════════════════
#  TOVÁRNA NA HVĚZDIČKOVÉ TLAČÍTKO
# ══════════════════════════════════════════════════════════════
def make_btn(parent, label, color, row, col,
             colspan=1, w=66, h=60, on_click=None, disabled=False):
    """
    Vytvoří westernové hvězdičkové tlačítko.
    disabled=True → tmavší barva, žádný klik handler.
    """
    cw = w * colspan + (colspan - 1) * 5
    c = tk.Canvas(parent, width=cw, height=h,
                  bg=PARCHMENT, highlightthickness=0, bd=0)
    c.grid(row=row, column=col, columnspan=colspan,
           padx=2, pady=2, sticky="nsew")

    fill = BTN_DISABLED if disabled else color
    cx, cy = cw // 2, h // 2
    r  = min(cw, h) // 2 - 3
    ir = r * 0.42
    pts = []
    for i in range(10):
        ang = math.radians(i * 36 - 90)
        rad = r if i % 2 == 0 else ir
        pts += [cx + rad * math.cos(ang), cy + rad * math.sin(ang)]

    rh = int(fill[1:3], 16) / 255
    gh = int(fill[3:5], 16) / 255
    bh = int(fill[5:7], 16) / 255
    import colorsys as _cs
    h2, s2, v2 = _cs.rgb_to_hsv(rh, gh, bh)
    r2, g2, b2 = _cs.hsv_to_rgb(h2, s2 * 0.6, min(1.0, v2 * 1.4))
    light = "#{:02x}{:02x}{:02x}".format(int(r2*255), int(g2*255), int(b2*255))

    fs   = 9 if len(label) > 3 else (13 if len(label) > 2 else 15)
    tf   = PARCHMENT if color != BTN_NUM else WOOD
    if disabled: tf = "#6a5a5a"
    font = ("Georgia", fs, "bold")

    def draw(f=fill):
        c.delete("all")
        c.create_polygon([p+2 for p in pts], fill="#1a0a00", outline="")
        c.create_polygon(pts, fill=f, outline=WOOD, width=1.5)
        c.create_text(cx, cy, text=label, font=font, fill=tf)

    draw()

    if not disabled:
        c.bind("<Enter>",    lambda e: draw(light))
        c.bind("<Leave>",    lambda e: draw(fill))
        if on_click:
            c.bind("<Button-1>", lambda e: on_click(label))
        else:
            c.bind("<Button-1>", lambda e: handle_button(label))

# ══════════════════════════════════════════════════════════════
#  VĚDECKÉ TLAČÍTKA (skryté v BASIC módu)
# ══════════════════════════════════════════════════════════════
sci_frame = tk.Frame(left, bg=PARCHMENT)
# (zabalí se až při set_mode — startuje jako SCIENTIFIC)

sci_buttons = [
    # řádek 0
    ("sin",   BTN_SCI,  0, 0), ("cos",   BTN_SCI, 0, 1),
    ("tan",   BTN_SCI,  0, 2), ("log",   BTN_SCI, 0, 3),
    # řádek 1
    ("sin⁻¹", BTN_SCI,  1, 0), ("cos⁻¹", BTN_SCI, 1, 1),
    ("tan⁻¹", BTN_SCI,  1, 2), ("ln",    BTN_SCI, 1, 3),
    # řádek 2
    ("10ˣ",  BTN_SCI,  2, 0), ("eˣ",    BTN_SCI, 2, 1),
    ("x²",   BTN_NEW,  2, 2), ("³√",    BTN_NEW, 2, 3),
]
for lbl, clr, row, col in sci_buttons:
    make_btn(sci_frame, lbl, clr, row, col, w=66, h=50, disabled=True)

# Popisek pod sci tlačítky
tk.Label(sci_frame, text="— zatím bez logiky —", bg=PARCHMENT, fg="#b0956a",
         font=("Georgia", 7, "italic")).grid(row=3, column=0, columnspan=4, pady=(2, 0))

# ── Divider ───────────────────────────────────────────────
divider_label = tk.Label(left, text="─── ✦ ───", bg=PARCHMENT, fg=GOLD,
                          font=("Georgia", 11))
divider_label.pack(pady=(6, 4))

# ── Paměťová řada (vizuál, bez logiky) ───────────────────
mem_frame = tk.Frame(left, bg=PARCHMENT)
mem_frame.pack(pady=(0, 4))
for ci, lbl in enumerate(["MC", "MR", "M+", "M−"]):
    make_btn(mem_frame, lbl, BTN_MEM, 0, ci, w=66, h=50, disabled=True)
tk.Label(left, text="— zatím bez logiky —", bg=PARCHMENT, fg="#b0956a",
         font=("Georgia", 7, "italic")).pack()

# ── Hlavní mřížka tlačítek (plná logika) ─────────────────
tk.Label(left, text="─── ✦ ───", bg=PARCHMENT, fg=GOLD,
         font=("Georgia", 11)).pack(pady=(4, 4))

btn_frame = tk.Frame(left, bg=PARCHMENT)
btn_frame.pack()

main_buttons = [
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
for lbl, clr, row, col in main_buttons:
    make_btn(btn_frame, lbl, clr, row, col)

make_btn(btn_frame, "0", BTN_NUM, 5, 0, colspan=2)
make_btn(btn_frame, "=", BTN_EQ,  5, 2, colspan=2)

# Tagline
tk.Label(left, text="~ Fastest Calculations in the West ~",
         bg=PARCHMENT, fg=LEATHER,
         font=("Georgia", 8, "italic")).pack(pady=(10, 0))

# ══════════════════════════════════════════════════════════════
#  PRAVÝ SLOUPEC — páska s historií
# ══════════════════════════════════════════════════════════════
tk.Label(right, text="— TAPE —", bg=PARCHMENT, fg=WOOD,
         font=("Georgia", 10, "bold")).pack(pady=(0, 4))

tape_outer = tk.Frame(right, bg=GOLD, bd=2)
tape_outer.pack(fill="both", expand=True)
tape_inner = tk.Frame(tape_outer, bg="#e8dca0", padx=4, pady=4)
tape_inner.pack(fill="both", expand=True, padx=2, pady=2)

tape_text = tk.Text(
    tape_inner,
    width=16, height=24,
    bg="#e8dca0", fg=WOOD,
    font=("Courier", 9),
    relief="flat", bd=0,
    state="disabled",
    wrap="none",
    cursor="arrow",
)
tape_scroll = tk.Scrollbar(tape_inner, orient="vertical",
                            command=tape_text.yview)
tape_text.configure(yscrollcommand=tape_scroll.set)
tape_scroll.pack(side="right", fill="y")
tape_text.pack(side="left", fill="both", expand=True)

# Odesílat výsledky do pásky při výpočtu
_orig_calculate = calculate

def calculate():
    global current_input, first_value, operator
    second = float(current_input or display_var.get() or "0")
    a, op  = (first_value if first_value is not None else 0), operator
    expr_s = f"{a} {op} {second} ="
    expr_var.set(expr_s)
    if op == "+":   result = math_lib.add(a, second)
    elif op == "-": result = math_lib.subtract(a, second)
    elif op == "×": result = math_lib.multiply(a, second)
    elif op == "÷": result = math_lib.divide(a, second)
    elif op == "^": result = math_lib.power(a, second)
    elif op == "√": result = math_lib.root(a, second)
    else:           result = second
    current_input = format_result(result)
    first_value = None; operator = None
    update_display(current_input)
    # Přidej do pásky
    tape_text.config(state="normal")
    tape_text.insert("end", f"{a} {op} {second}\n")
    tape_text.insert("end", f" → {current_input}\n")
    tape_text.insert("end", f"{'─'*15}\n")
    tape_text.see("end")
    tape_text.config(state="disabled")

# Také unární operace (n!, |x|) do pásky — přepíšeme handle_button
_orig_handle = handle_button
def handle_button(label):
    global current_input, first_value, operator, just_calculated
    play_gunshot()
    try:
        if label in "0123456789":
            if just_calculated: current_input = ""; just_calculated = False
            current_input = label if current_input == "0" else current_input + label
            update_display(current_input); expr_var.set("")
        elif label == ".":
            if just_calculated: current_input = "0"; just_calculated = False
            if "." not in current_input:
                current_input = (current_input or "0") + "."; update_display(current_input)
        elif label == "⌫":
            current_input = current_input[:-1] or "0"; update_display(current_input)
        elif label == "C":
            current_input = ""; first_value = None; operator = None
            just_calculated = False; update_display("0"); expr_var.set("")
        elif label == "n!":
            val = int(float(current_input or "0"))
            result = math_lib.factorial(val)
            expr_s = f"{val}! ="
            expr_var.set(expr_s)
            current_input = format_result(result); update_display(current_input)
            just_calculated = True
            tape_text.config(state="normal")
            tape_text.insert("end", f"{val}!\n → {current_input}\n{'─'*15}\n")
            tape_text.see("end"); tape_text.config(state="disabled")
        elif label == "|x|":
            val = float(current_input or "0")
            result = math_lib.absolute_value(val)
            expr_s = f"|{val}| ="
            expr_var.set(expr_s)
            current_input = format_result(result); update_display(current_input)
            just_calculated = True
            tape_text.config(state="normal")
            tape_text.insert("end", f"|{val}|\n → {current_input}\n{'─'*15}\n")
            tape_text.see("end"); tape_text.config(state="disabled")
        elif label in ("+", "-", "×", "÷", "^", "√"):
            if operator and current_input and not just_calculated: calculate()
            first_value = float(current_input or display_var.get() or "0")
            operator = label; current_input = ""; just_calculated = False
            expr_var.set(f"{first_value} {label}"); update_display(label)
        elif label == "=":
            calculate(); just_calculated = True
    except ZeroDivisionError:
        update_display("Dělení nulou!", error=True)
        expr_var.set(""); current_input = ""; first_value = None; operator = None
    except ValueError as e:
        update_display(str(e)[:20], error=True)
        expr_var.set(""); current_input = ""; first_value = None; operator = None

# Tlačítko pro vymazání pásky
def clear_tape():
    tape_text.config(state="normal")
    tape_text.delete("1.0", "end")
    tape_text.config(state="disabled")

tk.Label(right, text="", bg=PARCHMENT).pack()   # spacer
clear_btn_c = tk.Canvas(right, width=110, height=30,
                          bg=PARCHMENT, highlightthickness=0)
clear_btn_c.pack()
clear_btn_c.create_rectangle(2, 2, 108, 28, fill=BTN_CLEAR, outline=WOOD, width=1.5)
clear_btn_c.create_text(55, 15, text="CLEAR TAPE",
                         font=("Georgia", 9, "bold"), fill=PARCHMENT)
clear_btn_c.bind("<Button-1>", lambda e: clear_tape())
clear_btn_c.bind("<Enter>",    lambda e: clear_btn_c.itemconfig(1, fill="#9a3030"))
clear_btn_c.bind("<Leave>",    lambda e: clear_btn_c.itemconfig(1, fill=BTN_CLEAR))

# ══════════════════════════════════════════════════════════════
#  SPUŠTĚNÍ
# ══════════════════════════════════════════════════════════════

# Nastav výchozí mód
set_mode("SCIENTIFIC")

root.bind("<Key>", on_key)
root.after(100, _init_shots)
root.after(300, _init_music)
root.protocol("WM_DELETE_WINDOW", lambda: (_cleanup(), root.destroy()))
root.mainloop()