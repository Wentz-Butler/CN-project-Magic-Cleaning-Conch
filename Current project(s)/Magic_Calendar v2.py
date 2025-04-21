import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime, date, timedelta
import json
from collections import defaultdict
import os

# === Setup ===
now = datetime.now()
current_year = now.year
current_month = now.month
todotyme = "todotyme.json"
scheduled_tasks = []

# === Frame switching system ===
root = tk.Tk()
root.title("ToDoTyme Calendar")

calendar_frame = tk.Frame(root)
day_view_frame = tk.Frame(root)
schedule_frame = tk.Frame(root)

calendar_frame.grid(row=0, column=0, sticky="nsew")
day_view_frame.grid(row=0, column=0, sticky="nsew")
schedule_frame.grid(row=0, column=0, sticky="nsew")
schedule_frame.grid_remove()

def show_frame(frame):
    for f in [calendar_frame, day_view_frame, schedule_frame]:
        f.grid_remove()
    frame.grid()

# === Log processing ===
def load_logs(log_path):
    if not os.path.exists(log_path):
        return []
    try:
        with open(log_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading log: {e}")
        return []

def write_log(entry):
    logs = load_logs(todotyme)
    logs.append(entry)
    with open(todotyme, 'w') as file:
        json.dump(logs, file, indent=4)

def get_logs_by_day(log_path):
    logs = load_logs(log_path)
    logs_by_day = defaultdict(list)
    for entry in logs:
        try:
            timestamp = datetime.strptime(entry["timestamp"], "%Y-%m-%d %I:%M %p")
            logs_by_day[timestamp.date()].append(entry)
        except Exception:
            continue
    return logs_by_day

def get_day_colors(log_path, year, month):
    logs_by_day = get_logs_by_day(log_path)
    colored_days = {}
    today = date.today()

    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        log_day = date(year, month, day)
        if log_day > today:
            future_entries = logs_by_day.get(log_day, [])
            for entry in future_entries:
                if entry.get("choice") == "cleaning":
                    colored_days[day] = "yellow"
                elif entry.get("choice") != "cleaning":
                    colored_days[day] = "light blue"
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

def reload_calendar():
    for widget in calendar_frame.grid_slaves():
        if int(widget.grid_info()["row"]) > 1:
            widget.destroy()

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
                    bg=color,
                    command=lambda d=day: day_click(d)
                )
            label.grid(row=week_num+2, column=day_num)

reload_calendar()

# === Day View ===
day_view_label = tk.Label(day_view_frame, text="", font=("Arial", 14))
day_view_label.pack(pady=10)

day_view_text = tk.Text(day_view_frame, wrap=tk.WORD, width=50, height=15, state=tk.DISABLED)
day_view_text.pack(padx=10, pady=5)

schedule_button = tk.Button(day_view_frame, text="Schedule", command=lambda: show_frame(schedule_frame))
schedule_button.pack(pady=5)

back_button = tk.Button(day_view_frame, text="Back to Calendar", command=lambda: show_frame(calendar_frame))
back_button.pack(pady=10)

# === Scheduling UI ===
sched_label = tk.Label(schedule_frame, text="Schedule a Task", font=("Arial", 14))
sched_label.pack(pady=10)

what_var = tk.StringVar(value="Cleaning")
what_menu = ttk.Combobox(schedule_frame, textvariable=what_var, values=["Cleaning", "Something else"], state="readonly")
what_menu.pack(pady=5)

custom_task_var = tk.StringVar()
custom_task_entry = tk.Entry(schedule_frame, textvariable=custom_task_var)

def toggle_custom_entry(event):
    if what_var.get() == "Something else":
        custom_task_entry.pack(pady=5)
    else:
        custom_task_entry.pack_forget()

what_menu.bind("<<ComboboxSelected>>", toggle_custom_entry)

time_frame = tk.Frame(schedule_frame)
time_frame.pack(pady=5)

hour_var = tk.StringVar(value="12")
minute_var = tk.StringVar(value="00")
ampm_var = tk.StringVar(value="PM")

hour_menu = ttk.Combobox(time_frame, textvariable=hour_var, values=[f"{h}" for h in range(1, 13)], width=5, state="readonly")
hour_menu.grid(row=0, column=0, padx=2)

minute_menu = ttk.Combobox(time_frame, textvariable=minute_var, values=[f"{m:02d}" for m in range(0, 60)], width=5, state="readonly")
minute_menu.grid(row=0, column=1, padx=2)

ampm_menu = ttk.Combobox(time_frame, textvariable=ampm_var, values=["AM", "PM"], width=5, state="readonly")
ampm_menu.grid(row=0, column=2, padx=2)

freq_var = tk.StringVar(value="Once")
freq_menu = ttk.Combobox(schedule_frame, textvariable=freq_var,
                         values=["Once", "Daily", "Weekly", "Bi-weekly", "Monthly"], state="readonly")
freq_menu.pack(pady=5)

submit_button = tk.Button(schedule_frame, text="Submit", command=lambda: schedule_task())
submit_button.pack(pady=10)

back_from_sched = tk.Button(schedule_frame, text="Back to Day View", command=lambda: show_frame(day_view_frame))
back_from_sched.pack(pady=5)

selected_day = None

def schedule_task():
    task_type = what_var.get()
    task_name = "Magic_Cleaning_Conch.exe" if task_type == "Cleaning" else custom_task_var.get()
    freq_val = freq_var.get()
    time_val = f"{hour_var.get()}:{minute_var.get()} {ampm_var.get()}"
    color = "yellow" if task_type == "Cleaning" else "blue"

    def log_task_for_day(target_day):
        timestamp = datetime.combine(target_day, datetime.strptime(time_val, "%I:%M %p").time())
        write_log({
            "timestamp": timestamp.strftime("%Y-%m-%d %I:%M %p"),
            "task": task_name,
            "choice": task_type.lower(),
            "frequency": freq_val
        })

    # Log task depending on frequency
    days_to_schedule = [selected_day]
    if freq_val == "Weekly":
        days_to_schedule = [selected_day + timedelta(weeks=i) for i in range(4)]
    elif freq_val == "Daily":
        days_to_schedule = [selected_day + timedelta(days=1*i) for i in range(365)]
    elif freq_val == "Bi-weekly":
        days_to_schedule = [selected_day + timedelta(weeks=2*i) for i in range(2)]
    elif freq_val == "Monthly":
        days_to_schedule = [selected_day + timedelta(days=30*i) for i in range(2)]

    for d in days_to_schedule:
        log_task_for_day(d)

    reload_calendar()
    show_frame(calendar_frame)

def day_click(day):
    global selected_day
    selected_day = date(current_year, current_month, day)

    logs = get_logs_by_day(todotyme).get(selected_day, [])
    display_text = []
    bg_color = None

    had_launch = False
    had_completion = False
    has_cleaning_task = False
    has_other_task = False

    for entry in logs:
        if "task" in entry:
            task_text = f"Scheduled Task: {entry['task']} \nDuration:({entry.get('duration')})\nTimer complete, Good job!"
            display_text.append(task_text)
            if entry.get("choice") == "cleaning":
                has_cleaning_task = True
            else:
                has_other_task = True

        if entry.get("timer status") == "complete":
            had_completion = True
        elif "app launched" in entry:    
                task_text = "The app was launched and ignored this day"
                display_text.append(task_text)
                had_launch = True

    if not display_text:
        display_text.append("No logs found for this day.")

    # Determine background color
    if selected_day > date.today():
        if has_cleaning_task:
            bg_color = "yellow"
        elif has_other_task:
            bg_color = "light blue"
    else:
        if had_completion:
            bg_color = "green"
        elif had_launch:
            bg_color = "red"

    # Update label and text area
    day_view_label.config(text=f"{calendar.month_name[current_month]} {day}, {current_year}")
    day_view_frame.configure(bg=bg_color or "SystemButtonFace")
    day_view_label.configure(bg=bg_color or "SystemButtonFace")
    day_view_text.configure(state=tk.NORMAL, bg="white")  # leave text bg white for readability
    day_view_text.delete("1.0", tk.END)
    day_view_text.insert(tk.END, "\n".join(display_text))
    day_view_text.configure(state=tk.DISABLED)

    # Schedule button visibility
    if selected_day >= date.today():
        schedule_button.pack(pady=5)
    else:
        schedule_button.pack_forget()

    show_frame(day_view_frame)

# === Start on calendar view ===
show_frame(calendar_frame)
root.mainloop()
