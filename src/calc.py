##
# @file calc.py
# @brief Westernová kalkulačka s GUI - OPRAVENÁ VERZE (Znaménka, Faktoriál, Zobrazení)
# @author Václav Král xkralva00
# @date 2026-04-02

import tkinter as tk
from tkinter import font as tkfont
import random
import os
import sys
import threading
import winsound
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

# --- Správa zvuku ---
_winmm = ctypes.WinDLL("winmm")
_winmm.mciSendStringW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_void_p]
_winmm.mciSendStringW.restype = ctypes.c_int32

def _mci(cmd: str) -> int:
    return _winmm.mciSendStringW(cmd, None, 0, None)

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

def load_shot_paths():
    return [os.path.join(BASE_DIR, f"shot{i}.wav") for i in range(1, 9) if os.path.exists(os.path.join(BASE_DIR, f"shot{i}.wav"))]

def play_random_shot(shot_paths):
    if shot_paths:
        path = random.choice(shot_paths)
        threading.Thread(target=lambda: winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC), daemon=True).start()

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
        self.root.configure(bg=C["bg"])

        self.expression = ""
        self.result_shown = False
        self.error_state = False
        self.pending_op = None
        self.pending_val = None

        self.shot_paths = load_shot_paths()
        self.music_on = True
        play_background_music()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()
        self._bind_keyboard()

    def _on_close(self):
        stop_background_music()
        self.root.destroy()

    def _toggle_music(self):
        self.music_on = not self.music_on
        if self.music_on:
            resume_background_music()
            self.music_btn.configure(text="♪", fg=C["gold_light"], bg=C["btn_op"])
        else:
            pause_background_music()
            self.music_btn.configure(text="♪", fg=C["wood_mid"], bg=C["btn_spec"])

    def _get_serif(self):
        available = tkfont.families()
        for f in ["Georgia", "Times New Roman"]:
            if f in available: return f
        return "serif"

    def _get_mono(self):
        available = tkfont.families()
        for f in ["Courier New", "Consolas"]:
            if f in available: return f
        return "monospace"

    def _build_ui(self):
        serif, mono = self._get_serif(), self._get_mono()
        outer = tk.Frame(self.root, bg=C["border"], padx=3, pady=3)
        outer.pack(padx=14, pady=14)
        main = tk.Frame(outer, bg=C["wood_dark"], padx=12, pady=12)
        main.pack()

        title_frame = tk.Frame(main, bg=C["wood_dark"])
        title_frame.pack(fill="x")
        tk.Label(title_frame, text="✦  DEAD MAN'S CALC  ✦", bg=C["wood_dark"], fg=C["gold_light"], font=(serif, 13, "bold"), pady=6).pack(side="left", expand=True)
        
        self.music_btn = tk.Button(title_frame, text="♪", bg=C["btn_op"], fg=C["gold_light"], relief="flat", bd=0, width=2, command=self._toggle_music)
        self.music_btn.pack(side="right", padx=(0, 2), pady=4)

        tk.Frame(main, bg=C["gold"], height=2).pack(fill="x", pady=(0, 8))

        disp_frame = tk.Frame(main, bg=C["border"], padx=2, pady=2)
        disp_frame.pack(fill="x")
        disp_inner = tk.Frame(disp_frame, bg=C["display_bg"])
        disp_inner.pack(fill="x")

        self.expr_var = tk.StringVar(value="")
        tk.Label(disp_inner, textvariable=self.expr_var, bg=C["display_bg"], fg=C["gold"], anchor="e", font=(mono, 9), padx=8, pady=2).pack(fill="x")

        self.disp_var = tk.StringVar(value="0")
        tk.Label(disp_inner, textvariable=self.disp_var, bg=C["display_bg"], fg=C["display_fg"], anchor="e", font=(mono, 26, "bold"), padx=8, pady=6, width=14).pack(fill="x")

        tk.Frame(main, bg=C["gold"], height=2).pack(fill="x", pady=(8, 6))
        btn_frame = tk.Frame(main, bg=C["wood_dark"])
        btn_frame.pack()
        self._make_buttons(btn_frame, serif)

    def _make_buttons(self, parent, serif):
        layout = [
            [("√", lambda: self._special("sqrt"), C["btn_spec"], C["btn_h"], 1), ("n√x", lambda: self._await_binary("root"), C["btn_spec"], C["btn_h"], 1), ("xⁿ", lambda: self._await_binary("power"), C["btn_spec"], C["btn_h"], 1), ("n!", lambda: self._special("factorial"), C["btn_spec"], C["btn_h"], 1), ("|x|", lambda: self._special("abs"), C["btn_spec"], C["btn_h"], 1), ("C", self._clear, C["red"], C["red_light"], 1)],
            [("7", lambda: self._digit("7"), C["btn"], C["btn_h"], 1), ("8", lambda: self._digit("8"), C["btn"], C["btn_h"], 1), ("9", lambda: self._digit("9"), C["btn"], C["btn_h"], 1), ("÷", lambda: self._op("/"), C["btn_op"], C["btn_op_h"], 1), ("⌫", self._backspace, C["wood_mid"], C["wood_light"], 2)],
            [("4", lambda: self._digit("4"), C["btn"], C["btn_h"], 1), ("5", lambda: self._digit("5"), C["btn"], C["btn_h"], 1), ("6", lambda: self._digit("6"), C["btn"], C["btn_h"], 1), ("×", lambda: self._op("*"), C["btn_op"], C["btn_op_h"], 1), ("(", lambda: self._digit("("), C["wood_mid"], C["wood_light"], 1), (")", lambda: self._digit(")"), C["wood_mid"], C["wood_light"], 1)],
            [("1", lambda: self._digit("1"), C["btn"], C["btn_h"], 1), ("2", lambda: self._digit("2"), C["btn"], C["btn_h"], 1), ("3", lambda: self._digit("3"), C["btn"], C["btn_h"], 1), ("−", lambda: self._op("-"), C["btn_op"], C["btn_op_h"], 1), ("=", self._equals, C["btn_eq"], C["btn_eq_h"], 2)],
            [("0", lambda: self._digit("0"), C["btn"], C["btn_h"], 2), (".", lambda: self._digit("."), C["btn"], C["btn_h"], 1), ("+/-", self._negate, C["btn"], C["btn_h"], 1), ("+", lambda: self._op("+"), C["btn_op"], C["btn_op_h"], 1)],
        ]
        for r, row in enumerate(layout):
            col = 0
            for text, cmd, bg, hover, span in row:
                self._btn(parent, text, cmd, bg, hover, r, col, span, serif)
                col += span

    def _btn(self, parent, text, cmd, bg, hover, row, col, span, serif):
        frame = tk.Frame(parent, bg=C["border"], padx=1, pady=1)
        frame.grid(row=row, column=col, columnspan=span, padx=3, pady=3, sticky="nsew")
        b = tk.Button(frame, text=text, bg=bg, fg=C["cream"], font=(serif, 11, "bold"), width=4 * span, height=1, relief="flat", bd=0, command=lambda: [play_random_shot(self.shot_paths), cmd()])
        b.pack(fill="both", expand=True, ipadx=4, ipady=6)

    def _bind_keyboard(self):
        self.root.bind("<Key>", self._on_key)

    def _on_key(self, event):
        char, key = event.char, event.keysym
        if char in "0123456789.+-*/()": play_random_shot(self.shot_paths)
        if char in "0123456789": self._digit(char)
        elif char == ".": self._digit(".")
        elif char == "+": self._op("+")
        elif char == "-": self._op("-")
        elif char == "*": self._op("*")
        elif char == "/": self._op("/")
        elif char in ("=", "\r"): self._equals()
        elif key == "BackSpace": self._backspace()
        elif key == "Escape": self._clear()

    def _show(self, v): self.disp_var.set(v)
    def _show_expr(self, v): self.expr_var.set(v)
    def _current_number(self):
        try: return float(self.disp_var.get())
        except: return 0.0

    # --- LOGIKA TLAČÍTEK ---

    def _digit(self, d: str):
        if self.error_state: self._clear()
        if self.result_shown and d not in "()":
            self.expression = ""
            self.result_shown = False
            self._show("0")
        
        current = self.disp_var.get()
        if current == "0" and d != ".": self._show(d)
        else: self._show(current + d)
        
        self.expression += d
        self._show_expr(self.expression)

    def _op(self, op: str):
        if self.error_state: self._clear(); return
        sym = {"+": "+", "-": "−", "*": "×", "/": "÷"}[op]
        
        # OPRAVA 1: Zákaz vkládání stejných znamének po sobě (kromě + a -)
        if self.expression and op in ("*", "/"):
            last_char = self.expression.rstrip()[-1:]
            if last_char == sym:
                return # Znaménko se nepřidá podruhé
                
        if not self.expression: self.expression = self.disp_var.get()
        self.expression += f" {sym} "
        self._show_expr(self.expression)
        self.pending_op = None
        self._show("0")
        self.result_shown = False

    def _special(self, func: str):
        if self.error_state: self._clear(); return
        if self.expression: self._equals()
        if self.error_state: return
        val = self._current_number()
        try:
            ops = {"sqrt": lambda: sqrt(val), "factorial": lambda: factorial(int(val)), "abs": lambda: absolute_value(val)}
            res = ops[func]()
            
            # OPRAVA 3: Hezké zobrazení faktoriálu, odmocniny a absolutní hodnoty
            if func == "factorial":
                expr_str = f"{int(val)}!"
            elif func == "sqrt":
                expr_str = f"√({val})"
            else: # abs
                expr_str = f"|{val}|"
                
            self._show_expr(expr_str)
            self._finish(res)
        except Exception as e: self._error(str(e))

    def _await_binary(self, func: str):
        if self.error_state: self._clear(); return
        if self.expression: self._equals()
        if self.error_state: return
        self.pending_op, self.pending_val = func, self._current_number()
        self._show_expr(f"{self.pending_val} {'^' if func=='power' else 'n√'} ?")
        self._show("0")
        self.expression, self.result_shown = "", False

    def _equals(self):
        if self.error_state: self._clear(); return
        if self.pending_op in ("root", "power"):
            a, b = self.pending_val, self._current_number()
            try:
                res = root(a, int(b)) if self.pending_op == "root" else power(a, b)
                self._show_expr(f"{a} {'√' if self.pending_op=='root' else '^'} {b} =")
                self._finish(res)
            except Exception as e: self._error(str(e))
            finally: self.pending_op = None; return

        expr = self.expression.strip()
        if not expr: return
        eval_expr = expr.replace("×", "*").replace("÷", "/").replace("−", "-")
        try:
            res = evaluate(eval_expr)
            self._show_expr(f"{expr} =")
            self._finish(res)
        except Exception as e: self._error(str(e))

    def _finish(self, res):
        formatted = self._format_result(res)
        self._show(formatted); self.expression = formatted
        self.result_shown = True; self.error_state = False

    def _format_result(self, result) -> str:
        # OPRAVA 2: Návrat hezkého formátování (×10⁸) a oprava přetečení faktoriálu
        SUPERSCRIPT = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
        
        if isinstance(result, float) and result == int(result): 
            result = int(result)
            
        if isinstance(result, int):
            s = str(result)
            if len(s.lstrip("-")) <= 14: 
                return s
            # Manuální formátování pro obrovská celá čísla, která nezvládne float
            sign = "-" if result < 0 else ""
            s_abs = s.lstrip("-")
            exp = len(s_abs) - 1
            mantissa = s_abs[0] + "." + s_abs[1:5]
            mantissa = mantissa.rstrip("0").rstrip(".")
            exp_str = str(exp).translate(SUPERSCRIPT)
            return f"{sign}{mantissa}×10{exp_str}"

        # Ostatní desetinná čísla
        result = round(result, 8)
        abs_val = abs(result)
        if abs_val == 0 or (1e-4 <= abs_val < 1e10):
            s = f"{result:.8f}".rstrip("0").rstrip(".")
            if len(s.replace("-", "").replace(".", "")) <= 14:
                return s

        try:
            formatted = f"{result:.5e}"
            mantissa, exp_part = formatted.split("e")
            mantissa = str(round(float(mantissa), 4)).rstrip("0").rstrip(".")
            exp_str = str(int(exp_part)).translate(SUPERSCRIPT)
            return f"{mantissa}×10{exp_str}"
        except Exception:
            return "Příliš velké"

    def _error(self, msg):
        self._show("CHYBA"); self._show_expr(msg[:22]); self.error_state = True

    def _clear(self):
        self.expression = ""; self.pending_op = None; self.pending_val = None
        self.result_shown = self.error_state = False
        self._show("0"); self._show_expr("")

    def _backspace(self):
        if self.error_state or self.result_shown: self._clear(); return
        curr = self.disp_var.get()
        self._show(curr[:-1] if len(curr) > 1 else "0")
        self.expression = self.expression[:-1]
        self._show_expr(self.expression)

    def _negate(self):
        try:
            val = self._current_number()
            res = val * -1
            self._show(str(int(res) if res == int(res) else res))
            self.expression = self.disp_var.get()
        except: pass

if __name__ == "__main__":
    window = tk.Tk()
    app = WesternCalculator(window)
    window.mainloop()