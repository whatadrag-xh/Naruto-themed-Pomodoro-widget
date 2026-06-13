import customtkinter as ctk

remaining_seconds = 25 * 60
current_state = "focusing"
is_running = False
current_cycle = 0
total_cycles = 4
focus_duration = 25 * 60
rest_duration = 5 * 60

root = ctk.CTk()
root.title("Pomodoro Timer")
root.geometry("300x350")

focus_entry = ctk.CTkEntry(root)
focus_entry.pack(pady=5)
focus_entry.insert(0, "25")

rest_entry = ctk.CTkEntry(root)
rest_entry.pack(pady=5)
rest_entry.insert(0, "5")

cycles_entry = ctk.CTkEntry(root)
cycles_entry.pack(pady=5)
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
        
        reset_timer()
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
    
    timer_label.configure(text=clock_style(remaining_seconds))
    root.after(1000, tick)

def toggle_timer():
    global is_running
    
    if is_running:
        is_running = False
        start_pause_button.configure(text="▶")
    else:
        is_running = True
        start_pause_button.configure(text="||")
        tick()

def reset_timer():
    global remaining_seconds, current_state, is_running, current_cycle, focus_duration
    
    is_running = False
    current_state = "focusing"
    remaining_seconds = focus_duration
    current_cycle = 0
    
    timer_label.configure(text=clock_style(remaining_seconds))
    start_pause_button.configure(text="▶")

button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=10)

set_button = ctk.CTkButton(button_frame, text="Set", command=set_settings, width=80)
set_button.grid(row=0, column=0, padx=5)

start_pause_button = ctk.CTkButton(button_frame, text="▶", command=toggle_timer, width=80)
start_pause_button.grid(row=0, column=1, padx=5)

reset_button = ctk.CTkButton(button_frame, text="↺", command=reset_timer, width=80)
reset_button.grid(row=0, column=2, padx=5)

timer_label = ctk.CTkLabel(root, text=clock_style(remaining_seconds), font=("Arial", 40))
timer_label.pack(pady=20)

root.mainloop()