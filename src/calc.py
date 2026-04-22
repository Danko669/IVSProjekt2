##
# @file calc.py
# @brief Westernová kalkulačka s GUI v Tkinter
# @author Daniel Baloun xbaloud00

import tkinter as tk
from tkinter import font as tkfont
import mathematic as math_lib
import math
import os
import ctypes
import wave
import struct
import random
import tempfile

try:
    import winsound
    WINSOUND_AVAILABLE = True
except ImportError:
    WINSOUND_AVAILABLE = False

# ============================================================
#  KONFIGURACE — uprav názvy souborů dle potřeby
# ============================================================
MUSIC_FILENAME   = "western_boogie.mp3"   # hudba na pozadí
MUSIC_VOLUME     = 300                     # hlasitost hudby 0–1000

# Dej 3 WAV soubory se zvuky výstřelů do stejné složky.
# Pokud soubor neexistuje, použije se automaticky generovaný zvuk.
GUNSHOT_FILES = [
    "shot1.wav",
    "shot2.wav",
    "shot3.wav",
    "shot4.wav",
    "shot5.wav",
    "shot6.wav",
    "shot7.wav",
    "shot8.wav",
]

# ============================================================
#  Cesty — složka kde leží calc.py
# ============================================================
_BASE = os.path.dirname(os.path.abspath(__file__))

def _path(filename):
    return os.path.join(_BASE, filename)

# ============================================================
#  Zvuky výstřelů
# ============================================================
_shot_paths   = []   # načtené soubory (vlastní nebo generované)
_gen_temps    = []   # dočasné vygenerované soubory ke smazání
_last_shot    = -1   # index naposledy přehraného zvuku


def _generate_shot_wav(variation: int) -> str:
    """Vygeneruje jeden ze 3 různých výstřelů (záložní, pokud chybí WAV)."""
    sample_rate = 44100
    duration    = 0.4
    n           = int(sample_rate * duration)

    # Každá variace má jiné parametry
    params = [
        dict(crack=0.90, crack_decay=20, boom_freq=60,  boom_amp=0.50, boom_decay=8),   # ostrý
        dict(crack=0.65, crack_decay=10, boom_freq=45,  boom_amp=0.80, boom_decay=6),   # hluboký
        dict(crack=0.75, crack_decay=25, boom_freq=90,  boom_amp=0.35, boom_decay=12),  # praskavý
    ]
    p = params[variation % 3]

    rng = random.Random(variation * 7919)   # fixní seed pro každou variaci
    samples = []
    for i in range(n):
        t   = i / sample_rate
        env = math.exp(-t * p["crack_decay"])
        crack = (rng.random() * 2 - 1) * env * p["crack"]
        boom  = math.sin(2 * math.pi * p["boom_freq"] * t) * math.exp(-t * p["boom_decay"]) * p["boom_amp"]
        mid   = (rng.random() * 2 - 1) * math.exp(-t * 40) * 0.3
        s     = max(-1.0, min(1.0, crack + boom + mid))
        samples.append(int(s * 32767))

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    with wave.open(tmp.name, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(struct.pack(f'<{n}h', *samples))
    return tmp.name


def _init_shots():
    global _shot_paths, _gen_temps
    for i, filename in enumerate(GUNSHOT_FILES):
        p = _path(filename)
        if os.path.exists(p):
            _shot_paths.append(p)
            print(f"🔫 Načten vlastní výstřel: {filename}")
        else:
            gen = _generate_shot_wav(i)
            _shot_paths.append(gen)
            _gen_temps.append(gen)
            print(f"🔫 Soubor '{filename}' nenalezen — použit generovaný zvuk #{i+1}")


def play_gunshot():
    """Přehraje náhodný výstřel (jiný než ten předchozí)."""
    global _last_shot
    if not WINSOUND_AVAILABLE or not _shot_paths:
        return
    count = len(_shot_paths)
    if count == 1:
        idx = 0
    else:
        choices = [i for i in range(count) if i != _last_shot]
        idx = random.choice(choices)
    _last_shot = idx
    try:
        winsound.PlaySound(
            _shot_paths[idx],
            winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT
        )
    except Exception:
        pass


# ============================================================
#  Hudba — Windows MCI
# ============================================================
_music_path   = _path(MUSIC_FILENAME)
music_playing = False
_winmm        = ctypes.windll.winmm if hasattr(ctypes, "windll") else None


def _mci(cmd: str):
    if _winmm:
        _winmm.mciSendStringW(cmd, None, 0, None)


def _init_music():
    global music_playing
    if not _winmm:
        return
    if not os.path.exists(_music_path):
        print(f"⚠ Hudební soubor nenalezen: {_music_path}")
        return
    try:
        _mci(f'open "{_music_path}" type mpegvideo alias bgmusic')
        _mci(f"setaudio bgmusic volume to {MUSIC_VOLUME}")
        _mci("play bgmusic repeat")
        music_playing = True
    except Exception as e:
        print(f"Hudbu se nepodařilo spustit: {e}")


def _cleanup():
    _mci("stop bgmusic")
    _mci("close bgmusic")
    for p in _gen_temps:
        try:
            os.unlink(p)
        except Exception:
            pass


def toggle_music(event=None):
    global music_playing
    if not _winmm:
        return
    if music_playing:
        _mci("pause bgmusic")
        music_playing = False
        music_note_label.config(fg="#6b5a3e")
        note_status.config(text="OFF")
    else:
        _mci("resume bgmusic")
        music_playing = True
        music_note_label.config(fg=GOLD_BRIGHT)
        note_status.config(text="")


# ============================================================
#  Stav kalkulačky
# ============================================================
current_input   = ""
first_value     = None
operator        = None
just_calculated = False


def format_result(n):
    if isinstance(n, float) and n.is_integer():
        return str(int(n))
    return str(round(n, 10)).rstrip('0').rstrip('.')


def update_display(val, error=False):
    display_var.set(val)
    display_label.config(fg="#ff6b6b" if error else "#f5c518")


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
    a, op  = (first_value if first_value is not None else 0), operator
    expr_var.set(f"{a} {op} {second} =")

    if op == "+":       result = math_lib.add(a, second)
    elif op == "-":     result = math_lib.subtract(a, second)
    elif op == "×":     result = math_lib.multiply(a, second)
    elif op == "÷":     result = math_lib.divide(a, second)
    elif op == "^":     result = math_lib.power(a, second)
    elif op == "√":     result = math_lib.root(a, second)
    else:               result = second

    current_input = format_result(result)
    first_value   = None
    operator      = None
    update_display(current_input)


# ============================================================
#  Klávesnice
# ============================================================
def on_key(event):
    key_map = {
        "0":"0","1":"1","2":"2","3":"3","4":"4",
        "5":"5","6":"6","7":"7","8":"8","9":"9",
        "+":"+","-":"-","*":"×","/":"÷","^":"^",
        "=":"=","Return":"=","BackSpace":"⌫","Escape":"C",".":"."
    }
    if event.keysym in key_map:  handle_button(key_map[event.keysym])
    elif event.char in key_map:  handle_button(key_map[event.char])


# ============================================================
#  GUI
# ============================================================
root = tk.Tk()
root.title("🤠 Western Kalkulačka")
root.resizable(False, False)
root.configure(bg="#3d1f00")

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

outer = tk.Frame(root, bg=WOOD_LIGHT, bd=6, relief="ridge")
outer.pack(padx=14, pady=14)

gold_frame = tk.Frame(outer, bg=GOLD, bd=3)
gold_frame.pack(padx=2, pady=2)

inner = tk.Frame(gold_frame, bg=PARCHMENT, padx=18, pady=16)
inner.pack()

# ── Notička ───────────────────────────────────────────────
music_topbar = tk.Frame(inner, bg=PARCHMENT)
music_topbar.pack(fill="x")

tk.Label(music_topbar, bg=PARCHMENT, width=3).pack(side="left")

note_frame = tk.Frame(music_topbar, bg=PARCHMENT, cursor="hand2")
note_frame.pack(side="right")

music_note_label = tk.Label(note_frame, text="♪", bg=PARCHMENT, fg=GOLD_BRIGHT,
                             font=("Georgia", 20, "bold"), cursor="hand2")
music_note_label.pack(side="left")

note_status = tk.Label(note_frame, text="", bg=PARCHMENT, fg="#6b5a3e",
                        font=("Georgia", 8), cursor="hand2")
note_status.pack(side="left", pady=(8, 0))

for widget in (note_frame, music_note_label, note_status):
    widget.bind("<Button-1>", toggle_music)

music_note_label.bind("<Enter>", lambda e: music_note_label.config(font=("Georgia", 23, "bold")))
music_note_label.bind("<Leave>", lambda e: music_note_label.config(font=("Georgia", 20, "bold")))

# ── Titulky ───────────────────────────────────────────────
tk.Label(inner, text="★   W A N T E D   ★", bg=PARCHMENT, fg=WOOD_LIGHT,
         font=("Georgia", 9, "italic")).pack()
tk.Label(inner, text="CALC·U·LATOR", bg=PARCHMENT, fg=WOOD,
         font=("Georgia", 26, "bold")).pack(pady=(0, 2))
tk.Label(inner, text="Dead or Alive  ·  Est. 1876", bg=PARCHMENT, fg=LEATHER,
         font=("Georgia", 8, "italic")).pack(pady=(0, 10))

# ── Display ───────────────────────────────────────────────
disp_outer = tk.Frame(inner, bg=GOLD, bd=2)
disp_outer.pack(fill="x", pady=(0, 12))

disp_inner = tk.Frame(disp_outer, bg="#0d0800", padx=10, pady=8)
disp_inner.pack(fill="x", padx=2, pady=2)

expr_var = tk.StringVar(value="")
tk.Label(disp_inner, textvariable=expr_var, bg="#0d0800", fg="#7a5500",
         font=("Courier", 10), anchor="e").pack(fill="x")

display_var = tk.StringVar(value="0")
display_label = tk.Label(disp_inner, textvariable=display_var, bg="#0d0800",
                          fg=GOLD_BRIGHT, font=("Courier", 28, "bold"), anchor="e")
display_label.pack(fill="x")

tk.Label(inner, text="─── ✦ ───", bg=PARCHMENT, fg=GOLD,
         font=("Georgia", 11)).pack(pady=(0, 10))

# ── Tlačítka ──────────────────────────────────────────────
btn_frame = tk.Frame(inner, bg=PARCHMENT)
btn_frame.pack()


def make_btn(parent, label, color, row, col, colspan=1):
    import colorsys
    w = 68 * colspan + (colspan - 1) * 6
    h = 62
    c = tk.Canvas(parent, width=w, height=h,
                  bg=PARCHMENT, highlightthickness=0, bd=0)
    c.grid(row=row, column=col, columnspan=colspan,
           padx=3, pady=3, sticky="nsew")

    cx, cy, r = w // 2, h // 2, min(w, h) // 2 - 3
    pts, ir = [], r * 0.42
    for i in range(10):
        ang = math.radians(i * 36 - 90)
        rad = r if i % 2 == 0 else ir
        pts += [cx + rad * math.cos(ang), cy + rad * math.sin(ang)]

    rh = int(color[1:3], 16) / 255
    gh = int(color[3:5], 16) / 255
    bh = int(color[5:7], 16) / 255
    h2, s2, v2 = colorsys.rgb_to_hsv(rh, gh, bh)
    r2, g2, b2 = colorsys.hsv_to_rgb(h2, s2 * 0.6, min(1.0, v2 * 1.4))
    light = "#{:02x}{:02x}{:02x}".format(int(r2*255), int(g2*255), int(b2*255))
    tf    = PARCHMENT if color != BTN_NUM else WOOD
    tf_font = ("Georgia", 16 if len(label) <= 2 else 12, "bold")

    def draw(fill=color):
        c.delete("all")
        c.create_polygon([p+2 for p in pts], fill="#1a0a00", outline="")
        c.create_polygon(pts, fill=fill, outline=WOOD, width=1.5)
        c.create_text(cx, cy, text=label, font=tf_font, fill=tf)

    draw()
    c.bind("<Enter>",    lambda e: draw(light))
    c.bind("<Leave>",    lambda e: draw(color))
    c.bind("<Button-1>", lambda e: handle_button(label))


buttons = [
    ("C",   BTN_CLEAR, 0, 0), ("|x|", BTN_SPEC, 0, 1),
    ("n!",  BTN_SPEC,  0, 2), ("÷",   BTN_OP,   0, 3),
    ("7",   BTN_NUM,   1, 0), ("8",   BTN_NUM,  1, 1),
    ("9",   BTN_NUM,   1, 2), ("×",   BTN_OP,   1, 3),
    ("4",   BTN_NUM,   2, 0), ("5",   BTN_NUM,  2, 1),
    ("6",   BTN_NUM,   2, 2), ("-",   BTN_OP,   2, 3),
    ("1",   BTN_NUM,   3, 0), ("2",   BTN_NUM,  3, 1),
    ("3",   BTN_NUM,   3, 2), ("+",   BTN_OP,   3, 3),
    ("^",   BTN_SPEC,  4, 0), ("√",   BTN_SPEC, 4, 1),
    (".",   BTN_SPEC,  4, 2), ("⌫",   BTN_SPEC, 4, 3),
]
for lbl, clr, row, col in buttons:
    make_btn(btn_frame, lbl, clr, row, col)

make_btn(btn_frame, "0", BTN_NUM, 5, 0, colspan=2)
make_btn(btn_frame, "=", BTN_EQ,  5, 2, colspan=2)

tk.Label(inner, text="~ Fastest Calculations in the West ~",
         bg=PARCHMENT, fg=LEATHER,
         font=("Georgia", 8, "italic")).pack(pady=(12, 0))

root.bind("<Key>", on_key)

root.after(100, _init_shots)
root.after(300, _init_music)
root.protocol("WM_DELETE_WINDOW", lambda: (_cleanup(), root.destroy()))

root.mainloop()