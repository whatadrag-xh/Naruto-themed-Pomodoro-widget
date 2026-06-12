import tkinter as tk

remaining_seconds = 25 * 60
current_state = "focusing"
is_running = False
current_cycle = 0
total_cycles = 4
focus_duration = 25 * 60
rest_duration = 5 * 60

root = tk.Tk()
root.title("Pomodoro Timer")
root.geometry("300x300")

focus_entry = tk.Entry(root)
focus_entry.pack()
focus_entry.insert(0, "25")

rest_entry = tk.Entry(root)
rest_entry.pack()
rest_entry.insert(0, "5")

cycles_entry = tk.Entry(root)
cycles_entry.pack()
cycles_entry.insert(0, "4")

def clock_style(remaining_seconds):
    hour = remaining_seconds // 3600
    minute = (remaining_seconds % 3600) // 60
    second = remaining_seconds % 60
    return f"{hour:02d}:{minute:02d}:{second:02d}"

def set_settings():
    global remaining_seconds, total_cycles, focus_duration, rest_duration, current_state, current_cycle, is_running
    
    try:
        focus_minutes = int(focus_entry.get())
        rest_minutes = int(rest_entry.get())
        total_cycles = int(cycles_entry.get())
        
        focus_duration = focus_minutes * 60
        rest_duration = rest_minutes * 60
        
        remaining_seconds = focus_duration
        current_state = "focusing"
        current_cycle = 0
        is_running = False
        
        timer_label.config(text=clock_style(remaining_seconds))
        start_pause_button.config(text="▶")
    except ValueError:
        print("Please enter a valid number.")

def tick():
    global remaining_seconds, current_state, is_running, current_cycle, focus_duration, rest_duration
    
    if not is_running:
        return
    
    if remaining_seconds <= 0:
        if current_state == "resting":
            current_state = "focusing"
            remaining_seconds = focus_duration
        else:
            current_state = "resting"
            remaining_seconds = rest_duration
            current_cycle += 1
            
            if current_cycle >= total_cycles:
                print("Pomodoro cycles completed!")
                is_running = False
                return
    else:
        remaining_seconds -= 1
    
    timer_label.config(text=clock_style(remaining_seconds))
    root.after(1000, tick)

def toggle_timer():
    global is_running
    
    if is_running:
        is_running = False
        start_pause_button.config(text="▶")
    else:
        is_running = True
        start_pause_button.config(text="||")
        tick()

def reset_timer():
    global remaining_seconds, current_state, is_running, current_cycle, focus_duration
    
    is_running = False
    current_state = "focusing"
    remaining_seconds = focus_duration
    current_cycle = 0
    
    timer_label.config(text=clock_style(remaining_seconds))
    start_pause_button.config(text="▶")

set_button = tk.Button(root, text="Set", command=set_settings)
set_button.pack()

start_pause_button = tk.Button(root, text="▶", command=toggle_timer)
start_pause_button.pack()

reset_button = tk.Button(root, text="↺", command=reset_timer)
reset_button.pack()

timer_label = tk.Label(root, text=clock_style(remaining_seconds), font=("Arial", 40))
timer_label.pack()

root.mainloop()