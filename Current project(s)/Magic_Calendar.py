import tkinter as tk
import calendar
from datetime import datetime, date
import json
from collections import defaultdict

# === Setup ===
now = datetime.now()
current_year = now.year
current_month = now.month
todotyme = "todotyme.json"

# === Frame switching system ===
root = tk.Tk()
root.title("ToDoTyme Calendar")

calendar_frame = tk.Frame(root)
day_view_frame = tk.Frame(root)

calendar_frame.grid(row=0, column=0, sticky="nsew")
day_view_frame.grid(row=0, column=0, sticky="nsew")
day_view_frame.grid_remove()  # hide until needed

def show_frame(frame):
    calendar_frame.grid_remove()
    day_view_frame.grid_remove()
    frame.grid()

# === Log processing ===
def get_logs_by_day(log_path):
    try:
        with open(log_path, 'r') as file:
            log_data = json.load(file)
    except Exception as e:
        print(f"Error reading log: {e}")
        return defaultdict(list)

    logs_by_day = defaultdict(list)
    for entry in log_data:
        try:
            timestamp = datetime.strptime(entry["timestamp"], "%Y-%m-%d %I:%M %p")
            logs_by_day[timestamp.date()].append(entry)
        except Exception as e:
            continue
    return logs_by_day

logs_by_day = get_logs_by_day(todotyme)

def get_day_colors(log_path, year, month):
    logs_by_day = get_logs_by_day(log_path)
    colored_days = {}
    today = date.today()

    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        log_day = date(year, month, day)
        if log_day > today:
            continue

        entries = logs_by_day.get(log_day, [])
        had_launch = any("app launched" in e for e in entries)
        had_completion = any(e.get("timer status") == "complete" for e in entries)

        if had_completion:
            colored_days[day] = "green"
        elif had_launch:
            colored_days[day] = "red"

    return colored_days

# === Calendar View ===
header = tk.Label(calendar_frame, text=f"{calendar.month_name[current_month]} {current_year}", font=("Arial", 16))
header.grid(row=0, column=0, columnspan=7, pady=10)

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
for i, day in enumerate(days):
    tk.Label(calendar_frame, text=day, font=("Arial", 12, "bold")).grid(row=1, column=i)

day_colors = get_day_colors(todotyme, current_year, current_month)
cal = calendar.monthcalendar(current_year, current_month)

for week_num, week in enumerate(cal):
    for day_num, day in enumerate(week):
        if day == 0:
            label = tk.Label(calendar_frame, text="", width=4, height=2)
        else:
            color = day_colors.get(day, "SystemButtonFace")
            label = tk.Button(
                calendar_frame,
                text=str(day),
                width=4,
                height=2,
                bg=color,#<+++ controlled by get_day_colors function color = get_day_colors(todotyme, curren_year, current_month).get(day, "SystemButtonFace")
                command=lambda d=day: day_click(d)
            )
        label.grid(row=week_num+2, column=day_num)

# === Day View ===
day_view_label = tk.Label(day_view_frame, text="", font=("Arial", 14))
day_view_label.pack(pady=10)

day_view_text = tk.Text(day_view_frame, wrap=tk.WORD, width=50, height=15, state=tk.DISABLED)
day_view_text.pack(padx=10, pady=5)

def back_to_calendar():
    show_frame(calendar_frame)

back_button = tk.Button(day_view_frame, text="Back to Calendar", command=back_to_calendar)
back_button.pack(pady=10)

# === Handle clicking a day ===
def day_click(day):
    day_date = date(current_year, current_month, day)
    entries = logs_by_day.get(day_date, [])

    had_launch = any("app launched" in e for e in entries)
    had_completion = any(e.get("timer status") == "complete" for e in entries)

    tasks = []
    for e in entries:
        if "task" in e:
            tasks.append(e["task"])
        if e.get("timer status") == "complete":
            break  # Stop collecting after completed

    # Change the frame's background color
    if had_completion:
        day_view_frame.config(bg="lightgreen")
        result = "Cleaning was prompted\n"
        for task in tasks:
            result += f"- {task}\n"
        result += "Completed! Good job!"
    elif had_launch:
        day_view_frame.config(bg="lightcoral")
        result = "Cleaning was prompted\n"
        for task in tasks:
            result += f"- {task}\n"
        result += "But it was not completed."
    else:
        day_view_frame.config(bg=root.cget("bg"))
        result = "No cleaning activity on this day."

    # Update label and text box
    day_view_label.config(text=f"{calendar.month_name[current_month]} {day}, {current_year}")
    day_view_text.config(state=tk.NORMAL)
    day_view_text.delete("1.0", tk.END)
    day_view_text.insert(tk.END, result)
    day_view_text.config(state=tk.DISABLED)

    show_frame(day_view_frame)

# === Start on calendar view ===
show_frame(calendar_frame)
root.mainloop()
