##
# @file calc.py
# @brief Westernová kalkulačka s GUI - VERZE S EASTER EGGY PŘED DISPLEJEM
# @author Daniel Baloun xbaloud00
# @date 2026-04-02

import tkinter as tk
from tkinter import font as tkfont
import random
import os
import sys
import threading
import ctypes

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    from mathematic import (
        add, subtract, multiply, divide,
        power, root, sqrt, factorial,
        absolute_value, evaluate
    )
except ImportError:
    print("Chyba: Nelze importovat mathematic.py.")
    sys.exit(1)

import platform

if platform.system() == "Windows":
    _winmm = ctypes.WinDLL("winmm")
    _winmm.mciSendStringW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_void_p]
    _winmm.mciSendStringW.restype = ctypes.c_int32

    def _mci(cmd: str) -> int:
        return _winmm.mciSendStringW(cmd, None, 0, None)
else:
    def _mci(cmd: str) -> int:
        return 0

def play_background_music():
    path = os.path.join(BASE_DIR, "western_boogie.mp3").replace("/", "\\")
    if os.path.exists(path):
        _mci("close bgmusic")
        _mci(f'open "{path}" type mpegvideo alias bgmusic')
        _mci("play bgmusic repeat")

def pause_background_music(): _mci("pause bgmusic")
def resume_background_music(): _mci("resume bgmusic")
def stop_background_music():
    _mci("stop bgmusic")
    _mci("close bgmusic")

def play_krovi_sound():
    path = os.path.join(BASE_DIR, "krovi.mp3").replace("/", "\\")
    if os.path.exists(path):
        _mci("close krovisound")
        _mci(f'open "{path}" type mpegvideo alias krovisound')
        _mci("play krovisound")

def load_shot_paths():
    return [os.path.join(BASE_DIR, f"shot{i}.mp3").replace("/", "\\") for i in range(1, 9) if os.path.exists(os.path.join(BASE_DIR, f"shot{i}.mp3"))]

def play_random_shot(shot_paths):
    if shot_paths:
        path = random.choice(shot_paths)
        kanal = random.randint(1, 5)
        alias = f"vystrel_{kanal}"
        _mci(f"close {alias}")
        _mci(f'open "{path}" type mpegvideo alias {alias}')
        _mci(f"play {alias}")

# --- Barvy ---
C = {
    "bg": "#1C0F05", "wood_dark": "#3B1F0A", "wood_mid": "#5C2E0A", "wood_light": "#7A3B10",
    "gold": "#C8921A", "gold_light": "#E8B84B", "cream": "#F2DEB0", "red": "#8B2020",
    "red_light": "#B03030", "display_bg": "#0D0602", "display_fg": "#E8B84B",
    "btn": "#4A2208", "btn_h": "#6B3410", "btn_op": "#6B2E05", "btn_op_h": "#8B4010",
    "btn_spec": "#3D1A00", "btn_eq": "#8B2020", "btn_eq_h": "#B03030", "border": "#C8921A",
}

class WesternCalculator:
    def __init__(self, root_window: tk.Tk):
        self.root = root_window
        self.root.title("☆  DEAD MAN'S CALC  ☆")
        self.root.resizable(False, False)

        # Ikonka
        try:
            icon_path = os.path.join(BASE_DIR, "icon.png")
            icon_img = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(False, icon_img)
        except: pass
        
        self.expression = ""
        self.result_shown = False
        self.error_state = False
        self.pending_op = None
        self.pending_val = None

        self.shot_paths = load_shot_paths()
        self.music_on = True
        play_background_music()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._nacti_obrazky()
        self._build_ui()
        self._bind_keyboard()

        self.root.after(15000, self.letajici_krovi)

    def _on_close(self):
        stop_background_music()
        self.root.destroy()

    def _nacti_obrazky(self):
        self.krovi_frames = []
        try:
            from PIL import Image, ImageTk
            krovi_img = Image.open(os.path.join(BASE_DIR, "krovi.png")).convert("RGBA")
            for angle in range(0, 360, 15):
                rotated = krovi_img.rotate(-angle, expand=True)
                self.krovi_frames.append(ImageTk.PhotoImage(rotated))
        except: pass

        try:
            self.img_error = tk.PhotoImage(file=os.path.join(BASE_DIR, "error.png"))
            self.img_67 = tk.PhotoImage(file=os.path.join(BASE_DIR, "67.png"))
        except:
            self.img_error = self.img_67 = None

    def _build_ui(self):
        serif, mono = self._get_serif(), self._get_mono()
        self.root.geometry("420x650")
        self.canvas = tk.Canvas(self.root, width=420, height=650, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        try:
            self.bg_photo = tk.PhotoImage(file=os.path.join(BASE_DIR, "background.png"))
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except:
            self.canvas.configure(bg=C["wood_dark"])

        self.music_btn = tk.Button(self.root, text="♪", bg=C["btn_op"], fg=C["gold_light"], relief="flat", bd=0, width=2, command=self._toggle_music)
        self.canvas.create_window(390, 20, window=self.music_btn, anchor="ne")

        # --- NOVÝ DISPLEJ (nakreslený přímo na plátně kvůli vrstvám Z-index) ---
        disp_w, disp_h = 380, 85
        cx, cy = 210, 240
        dx1, dy1 = cx - disp_w/2, cy - disp_h/2
        dx2, dy2 = cx + disp_w/2, cy + disp_h/2

        # Vykreslení rámečku a pozadí displeje
        self.canvas.create_rectangle(dx1, dy1, dx2, dy2, fill=C["border"], outline="")
        self.canvas.create_rectangle(dx1+2, dy1+2, dx2-2, dy2-2, fill=C["display_bg"], outline="")

        # Proměnné a Textové položky displeje
        self.expr_var = tk.StringVar(value="")
        self.expr_text_id = self.canvas.create_text(dx2 - 10, dy1 + 20, text="", fill=C["gold"], anchor="e", font=(mono, 9))

        self.disp_var = tk.StringVar(value="0")
        self.disp_text_id = self.canvas.create_text(dx2 - 10, dy2 - 25, text="0", fill=C["display_fg"], anchor="e", font=(mono, 26, "bold"))

        self._make_buttons(serif)

    def _make_buttons(self, serif):
        layout = [
            [("√", lambda: self._special("sqrt"), C["btn_spec"], C["btn_h"], 1), ("n√x", lambda: self._await_binary("root"), C["btn_spec"], C["btn_h"], 1), ("xⁿ", lambda: self._await_binary("power"), C["btn_spec"], C["btn_h"], 1), ("n!", lambda: self._special("factorial"), C["btn_spec"], C["btn_h"], 1), ("|x|", lambda: self._special("abs"), C["btn_spec"], C["btn_h"], 1), ("C", self._clear, C["red"], C["red_light"], 1)],
            [("7", lambda: self._digit("7"), C["btn"], C["btn_h"], 1), ("8", lambda: self._digit("8"), C["btn"], C["btn_h"], 1), ("9", lambda: self._digit("9"), C["btn"], C["btn_h"], 1), ("÷", lambda: self._op("/"), C["btn_op"], C["btn_op_h"], 1), ("⌫", self._backspace, C["wood_mid"], C["wood_light"], 2)],
            [("4", lambda: self._digit("4"), C["btn"], C["btn_h"], 1), ("5", lambda: self._digit("5"), C["btn"], C["btn_h"], 1), ("6", lambda: self._digit("6"), C["btn"], C["btn_h"], 1), ("×", lambda: self._op("*"), C["btn_op"], C["btn_op_h"], 1), ("(", lambda: self._digit("("), C["wood_mid"], C["wood_light"], 1), (")", lambda: self._digit(")"), C["wood_mid"], C["wood_light"], 1)],
            [("1", lambda: self._digit("1"), C["btn"], C["btn_h"], 1), ("2", lambda: self._digit("2"), C["btn"], C["btn_h"], 1), ("3", lambda: self._digit("3"), C["btn"], C["btn_h"], 1), ("−", lambda: self._op("-"), C["btn_op"], C["btn_op_h"], 1), ("=", self._equals, C["btn_eq"], C["btn_eq_h"], 2)],
            [("0", lambda: self._digit("0"), C["btn"], C["btn_h"], 2), (".", lambda: self._digit("."), C["btn"], C["btn_h"], 1), ("+/-", self._negate, C["btn"], C["btn_h"], 1), ("+", lambda: self._op("+"), C["btn_op"], C["btn_op_h"], 1)],
        ]
        start_x, start_y = 18, 310
        btn_w, btn_h, pad = 60, 50, 4
        for r, row in enumerate(layout):
            curr_x = start_x
            for text, cmd, bg, hover, span in row:
                self._btn(text, cmd, bg, hover, curr_x, start_y + r*(btn_h+pad), span, serif, btn_w, btn_h, pad)
                curr_x += (btn_w * span) + (pad * span)

    def _btn(self, text, cmd, bg, hover, x, y, span, serif, btn_w, btn_h, pad):
        w = (btn_w * span) + (pad * (span - 1))
        self.canvas.create_rectangle(x, y, x+w, y+btn_h, fill=C["border"], outline="")
        btn_id = self.canvas.create_rectangle(x+1, y+1, x+w-1, y+btn_h-1, fill=bg, outline="")
        self.canvas.create_text(x+w/2, y+btn_h/2, text=text, fill=C["cream"], font=(serif, 11, "bold"))
        ov_id = self.canvas.create_rectangle(x, y, x+w, y+btn_h, fill="", outline="")
        self.canvas.tag_bind(ov_id, "<Button-1>", lambda e: [play_random_shot(self.shot_paths), cmd()])
        self.canvas.tag_bind(ov_id, "<Enter>", lambda e: self.canvas.itemconfig(btn_id, fill=hover))
        self.canvas.tag_bind(ov_id, "<Leave>", lambda e: self.canvas.itemconfig(btn_id, fill=bg))

    # --- SPECIÁLNÍ EFEKTY ---
    def _vyskakovaci_efekt(self, zvuk_file, obrazek_obj, alias):
        path = os.path.join(BASE_DIR, zvuk_file).replace("/", "\\")
        if os.path.exists(path) and obrazek_obj:
            _mci(f"close {alias}")
            _mci(f'open "{path}" type mpegvideo alias {alias}')
            _mci(f"play {alias}")
            
            # Y=240 je přesně střed displeje. Nyní díky úpravě vykreslení spolehlivě překryje výsledky.
            img_id = self.canvas.create_image(210, 240, image=obrazek_obj, anchor="center")
            self.canvas.tag_raise(img_id)
            self.root.after(2000, lambda: self.canvas.delete(img_id))

    def letajici_krovi(self):
        self.root.after(15000, self.letajici_krovi)
        if not self.krovi_frames: return
        threading.Thread(target=play_krovi_sound, daemon=True).start()
        y, x = random.randint(350, 580), -100
        kid = self.canvas.create_image(x, y, anchor="center")
        self._animovat_krovi(kid, x, y, 0)

    def _animovat_krovi(self, kid, x, y, fidx):
        if x > 500: self.canvas.delete(kid); return
        self.canvas.itemconfig(kid, image=self.krovi_frames[fidx % len(self.krovi_frames)])
        self.canvas.coords(kid, x, y)
        self.canvas.tag_raise(kid)
        self.root.after(30, lambda: self._animovat_krovi(kid, x+5, y, fidx+1))

    # --- FUNKCE PRO ÚPRAVU DISPLEJE ---
    def _show(self, v): 
        self.disp_var.set(v)
        self.canvas.itemconfig(self.disp_text_id, text=v)
        
    def _show_expr(self, v): 
        self.expr_var.set(v)
        self.canvas.itemconfig(self.expr_text_id, text=v)

    # --- LOGIKA ---
    def _finish(self, res):
        formatted = self._format_result(res)
        self._show(formatted); self.expression = formatted
        self.result_shown, self.error_state = True, False
        try:
            if float(res) == 67:
                self._vyskakovaci_efekt("67.mp3", self.img_67, "egg67")
        except: pass

    def _error(self, msg):
        self._show("CHYBA"); self._show_expr(msg[:22]); self.error_state = True
        self._vyskakovaci_efekt("error.mp3", self.img_error, "eggerror")

    def _digit(self, d):
        if self.error_state: self._clear()
        if self.result_shown and d not in "()": self.expression = ""; self.result_shown = False; self._show("0")
        curr = self.disp_var.get()
        self._show(d if curr == "0" and d != "." else curr + d)
        self.expression += d; self._show_expr(self.expression)

    def _op(self, op):
        if self.error_state: self._clear(); return
        sym = {"+": "+", "-": "−", "*": "×", "/": "÷"}[op]
        if self.expression and op in ("*", "/") and self.expression.rstrip()[-1:] == sym: return
        if not self.expression: self.expression = self.disp_var.get()
        self.expression += f" {sym} "; self._show_expr(self.expression)
        self.pending_op = None; self._show("0"); self.result_shown = False

    def _special(self, func):
        if self.error_state: self._clear(); return
        if self.expression: self._equals()
        if self.error_state: return
        val = self._current_number()
        try:
            ops = {"sqrt": lambda: sqrt(val), "factorial": lambda: factorial(int(val)), "abs": lambda: absolute_value(val)}
            res = ops[func]()
            expr_str = f"{int(val)}!" if func == "factorial" else f"√({val})" if func == "sqrt" else f"|{val}|"
            self._show_expr(expr_str); self._finish(res)
        except Exception as e: self._error(str(e))

    def _await_binary(self, func):
        if self.error_state: self._clear(); return
        if self.expression: self._equals()
        if self.error_state: return
        self.pending_op, self.pending_val = func, self._current_number()
        self._show_expr(f"{self.pending_val} {'^' if func=='power' else 'n√'} ?")
        self._show("0"); self.expression, self.result_shown = "", False

    def _equals(self):
        if self.error_state: self._clear(); return
        if self.pending_op in ("root", "power"):
            a, b = self.pending_val, self._current_number()
            try:
                res = root(a, int(b)) if self.pending_op == "root" else power(a, b)
                self._show_expr(f"{a} {'√' if self.pending_op=='root' else '^'} {b} ="); self._finish(res)
            except Exception as e: self._error(str(e))
            finally: self.pending_op = None; return
        expr = self.expression.strip()
        if not expr: return
        eval_expr = expr.replace("×", "*").replace("÷", "/").replace("−", "-")
        try: res = evaluate(eval_expr); self._show_expr(f"{expr} ="); self._finish(res)
        except Exception as e: self._error(str(e))

    # --- POMOCNÉ ---
    def _toggle_music(self):
        self.music_on = not self.music_on
        if self.music_on: resume_background_music(); self.music_btn.configure(text="♪", fg=C["gold_light"], bg=C["btn_op"])
        else: pause_background_music(); self.music_btn.configure(text="♪", fg=C["wood_mid"], bg=C["btn_spec"])
    def _get_serif(self): return "Georgia" if "Georgia" in tkfont.families() else "serif"
    def _get_mono(self): return "Courier New" if "Courier New" in tkfont.families() else "monospace"
    def _current_number(self): 
        try: return float(self.disp_var.get())
        except: return 0.0
    def _clear(self): self.expression = ""; self.pending_op = self.pending_val = None; self.result_shown = self.error_state = False; self._show("0"); self._show_expr("")
    def _backspace(self):
        if self.error_state or self.result_shown: self._clear(); return
        curr = self.disp_var.get()
        self._show(curr[:-1] if len(curr) > 1 else "0"); self.expression = self.expression[:-1]; self._show_expr(self.expression)
    def _negate(self):
        try: v = self._current_number(); res = v * -1; self._show(str(int(res) if res == int(res) else res)); self.expression = self.disp_var.get()
        except: pass
    def _bind_keyboard(self): self.root.bind("<Key>", self._on_key)
    def _on_key(self, event):
        c, k = event.char, event.keysym
        if c in "0123456789.+-*/()": play_random_shot(self.shot_paths)
        if c in "0123456789": self._digit(c)
        elif c == ".": self._digit(".")
        elif c == "+": self._op("+")
        elif c == "-": self._op("-")
        elif c == "*": self._op("*")
        elif c == "/": self._op("/")
        elif c in ("=", "\r"): self._equals()
        elif k == "BackSpace": self._backspace()
        elif k == "Escape": self._clear()

    def _format_result(self, result) -> str:
        SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
        if isinstance(result, float) and result == int(result): result = int(result)
        if isinstance(result, int):
            s = str(result)
            if len(s.lstrip("-")) <= 14: return s
            sign, s_abs = ("-", s.lstrip("-")) if result < 0 else ("", s)
            mant = (s_abs[0] + "." + s_abs[1:5]).rstrip("0").rstrip(".")
            return f"{sign}{mant}×10{str(len(s_abs)-1).translate(SUP)}"
        result = round(result, 8)
        abs_v = abs(result)
        if abs_v == 0 or (1e-4 <= abs_v < 1e10):
            s = f"{result:.8f}".rstrip("0").rstrip(".")
            if len(s.replace("-","").replace(".","")) <= 14: return s
        try:
            m, e = f"{result:.5e}".split("e")
            return f"{str(round(float(m), 4)).rstrip('0').rstrip('.')}×10{str(int(e)).translate(SUP)}"
        except: return "Příliš velké"

if __name__ == "__main__":
    window = tk.Tk()
    app = WesternCalculator(window)
    window.mainloop()