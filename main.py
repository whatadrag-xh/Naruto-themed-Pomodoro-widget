import tkinter as tk

remaining_seconds = 10
current_state = "focusing"
is_running = False
current_cycle = 0      
total_cycles = 4   

def tick():
    global remaining_seconds, current_state, is_running, current_cycle

    if not is_running:
        return

    if remaining_seconds <= 0:
        if current_state == "resting":
            current_state = "focusing"
            remaining_seconds = 25 * 60
        else:
            current_state = "resting"
            remaining_seconds = 5 * 60
            current_cycle += 1   

            if current_cycle >= total_cycles:
                print("Pomodoro cycles completed!")
                is_running = False
                return
    else:
        remaining_seconds -= 1

    timer_label.config(text=clock_style(remaining_seconds))
    root.after(1000, tick)

root = tk.Tk()
def clock_style(remaining_seconds):
    hour = remaining_seconds // 3600
    minute = (remaining_seconds % 3600) // 60
    second = remaining_seconds % 60
    return f"{hour:02d}:{minute:02d}:{second:02d}"

def toggle_timer():
    global is_running

    if is_running:
        is_running = False
        start_pause_button.config(text="▶")

    else:
        is_running = True
        start_pause_button.config(text="||")
        tick()

start_pause_button = tk.Button(root, text="||", command=toggle_timer)
start_pause_button.pack()

def reset_timer():
    global remaining_seconds, current_state, is_running, current_cycle

    is_running = False
    current_state = "focusing"
    remaining_seconds = 25 * 60   
    current_cycle = 0

    timer_label.config(text=clock_style(remaining_seconds))
    start_pause_button.config(text="▶")

reset_button = tk.Button(root, text="↺", command=reset_timer)
reset_button.pack()

timer_label = tk.Label(root, text=clock_style(remaining_seconds), font=("Arial", 40))
timer_label.pack()
root.mainloop()