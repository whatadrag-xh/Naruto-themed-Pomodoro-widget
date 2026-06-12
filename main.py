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

    print(remaining_seconds)
    root.after(1000, tick)

root = tk.Tk()
tick()
root.mainloop()