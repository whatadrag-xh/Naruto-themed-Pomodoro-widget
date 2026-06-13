import tkinter as tk
import os
import random
import winsound
from PIL import Image, ImageTk

remaining_seconds = 25 * 60
current_state = "focusing"
is_running = False
current_cycle = 0
total_cycles = 4
focus_duration = 25 * 60
rest_duration = 5 * 60

FOCUS_ACCENT = "#E05C5C"
REST_ACCENT = "#4FC3A1"
SHADOW = "#000000"
WIN_W, WIN_H = 300, 380

root = tk.Tk()
root.title("Pomodoro Timer")
root.geometry(f"{WIN_W}x{WIN_H}")
root.resizable(False, False)
root.config(bg="black")

canvas = tk.Canvas(root, width=WIN_W, height=WIN_H,
                   highlightthickness=0, bg="black")
canvas.pack(fill="both", expand=True)

files = os.listdir("naruto-theme-pomodoro-wallpaper")
chosen_file = random.choice(files)
pil_img = Image.open(
    f"naruto-theme-pomodoro-wallpaper/{chosen_file}"
).resize((WIN_W, WIN_H))
bg_photo = ImageTk.PhotoImage(pil_img)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

def clock_style(secs):
    h, rem = divmod(secs, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def beep(times=2):
    try:
        for _ in range(times):
            winsound.Beep(1000, 200)
    except Exception:
        pass

def accent():
    return FOCUS_ACCENT if current_state == "focusing" else REST_ACCENT

FONT_SMALL = ("Arial", 11)

focus_var = tk.StringVar(value="25")
rest_var = tk.StringVar(value="5")
cycles_var = tk.StringVar(value="4")

def make_entry_row(y, label_text, textvariable):
    canvas.create_rectangle(14, y-14, 286, y+14,
                            fill="", outline="#aaaaaa", width=1)
    
    canvas.create_text(25, y+1, text=label_text, anchor="w",
                       fill=SHADOW, font=FONT_SMALL)
    
    canvas.create_text(24, y, text=label_text, anchor="w",
                       fill="#FF6B00", font=FONT_SMALL)
    
    ent = tk.Entry(root, textvariable=textvariable,
                   bg="black", fg="#F3EFEC",
                   insertbackground="white", relief="flat",
                   font=FONT_SMALL, width=4, justify="center",
                   highlightthickness=0)
    canvas.create_window(278, y, window=ent, anchor="e")
    return ent

focus_entry  = make_entry_row(30, "Focus (min)", focus_var)
rest_entry   = make_entry_row(58, "Rest (min)", rest_var)
cycles_entry = make_entry_row(86, "Cycles", cycles_var)

def make_canvas_button(x, y, w, h, label, command, label_color="#FF6B00"):
    rect_id = canvas.create_rectangle(
        x, y, x+w, y+h, fill="", outline="#aaaaaa", width=1
    )
    
    canvas.create_text(x + w//2 + 1, y + h//2 + 1, text=label,
                       fill=SHADOW, font=("Arial", 13, "bold"))
    
    text_id = canvas.create_text(
        x + w//2, y + h//2, text=label,
        fill=label_color, font=("Arial", 13, "bold")
    )

    def on_click(_): 
        command()
    def on_enter(_): 
        canvas.itemconfig(rect_id, outline="white", width=2)
    def on_leave(_): 
        canvas.itemconfig(rect_id, outline="#aaaaaa", width=1)

    for item in (rect_id, text_id):
        canvas.tag_bind(item, "<Button-1>", on_click)
        canvas.tag_bind(item, "<Enter>", on_enter)
        canvas.tag_bind(item, "<Leave>", on_leave)

    return rect_id, text_id

canvas.create_text(WIN_W//2+1, 153, text="● FOCUS",
                   fill=SHADOW, font=("Arial", 12, "bold"), tags="state_shadow")
state_text = canvas.create_text(WIN_W//2, 152, text="● FOCUS",
                                fill=FOCUS_ACCENT, font=("Arial", 12, "bold"))

canvas.create_text(WIN_W//2+2, 212, text=clock_style(remaining_seconds),
                   fill=SHADOW, font=("Arial", 46, "bold"), tags="timer_shadow")
timer_text = canvas.create_text(WIN_W//2, 210, text=clock_style(remaining_seconds),
                                fill=FOCUS_ACCENT, font=("Arial", 46, "bold"))

cycle_dot_ids: list[int] = []

def cycle_bar_update():
    for i, dot_id in enumerate(cycle_dot_ids):
        if i < current_cycle:
            color = FOCUS_ACCENT
        elif i == current_cycle and current_state == "resting":
            color = REST_ACCENT
        else:
            color = "#555555"
        canvas.itemconfig(dot_id, fill=color, outline=color)

def rebuild_dots():
    for d in cycle_dot_ids:
        canvas.delete(d)
    cycle_dot_ids.clear()
    spacing = 22
    start_x = WIN_W//2 - (total_cycles - 1) * spacing // 2
    for i in range(total_cycles):
        x = start_x + i * spacing
        dot = canvas.create_oval(x-7, 270, x+7, 284,
                                 fill="#555555", outline="#555555")
        cycle_dot_ids.append(dot)
    cycle_bar_update()

def update_accent():
    color = accent()
    label = "● FOCUS" if current_state == "focusing" else "● REST"
    canvas.itemconfig(state_text, text=label, fill=color)
    for item in canvas.find_withtag("state_shadow"):
        canvas.itemconfig(item, text=label)
    canvas.itemconfig(timer_text, fill=color)
    cycle_bar_update()

def sync_timer_display():
    t = clock_style(remaining_seconds)
    canvas.itemconfig(timer_text, text=t)
    for item in canvas.find_withtag("timer_shadow"):
        canvas.itemconfig(item, text=t)

def set_settings():
    global focus_duration, rest_duration, total_cycles
    try:
        focus_min = int(focus_var.get())
        rest_min = int(rest_var.get())
        n_cycles = int(cycles_var.get())
        if not (1 <= focus_min <= 120 and 1 <= rest_min <= 60 and 1 <= n_cycles <= 10):
            raise ValueError
    except ValueError:
        canvas.itemconfig(set_btn_rect, fill="#550000", outline="#ff4444")
        root.after(400, lambda: canvas.itemconfig(set_btn_rect,
                                                  fill="", outline="#aaaaaa"))
        return
    focus_duration = focus_min * 60
    rest_duration = rest_min  * 60
    total_cycles = n_cycles
    rebuild_dots()
    reset_timer()

def tick():
    global remaining_seconds, current_state, is_running, current_cycle
    if not is_running:
        return
    if remaining_seconds <= 0:
        beep()
        if current_state == "focusing":
            current_cycle += 1
            if current_cycle >= total_cycles:
                is_running = False
                canvas.itemconfig(timer_text, text="Done! 🎉", fill=REST_ACCENT)
                canvas.itemconfig(state_text, text="● ALL DONE", fill=REST_ACCENT)
                canvas.itemconfig(play_btn_text, text="▶")
                return
            current_state = "resting"
            remaining_seconds = rest_duration
        else:
            current_state = "focusing"
            remaining_seconds = focus_duration
        update_accent()
    else:
        remaining_seconds -= 1
    sync_timer_display()
    root.after(1000, tick)

def toggle_timer():
    global is_running
    if is_running:
        is_running = False
        canvas.itemconfig(play_btn_text, text="▶")
    else:
        is_running = True
        canvas.itemconfig(play_btn_text, text="⏸")
        tick()

def reset_timer():
    global remaining_seconds, current_state, is_running, current_cycle
    is_running = False
    current_state = "focusing"
    remaining_seconds = focus_duration
    current_cycle = 0
    canvas.itemconfig(play_btn_text, text="▶")
    sync_timer_display()
    update_accent()

BTN_Y = 110
set_btn_rect, _ = make_canvas_button(14, BTN_Y, 80, 28, "Set", set_settings)
play_rect, play_btn_text = make_canvas_button(110, BTN_Y, 80, 28, "▶", toggle_timer)
_ , _= make_canvas_button(206, BTN_Y, 80, 28, "↺", reset_timer)

rebuild_dots()

root.mainloop()