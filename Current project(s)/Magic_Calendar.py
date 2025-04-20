import tkinter as tk
import calendar
from datetime import datetime

# Get current date info
now = datetime.now()
current_year = now.year
current_month = now.month

# Create main window
root = tk.Tk()
root.title("ToDoTyme Calendar")

# Month and Year Label
header = tk.Label(root, text=f"{calendar.month_name[current_month]} {current_year}", font=("Arial", 16))
header.grid(row=0, column=0, columnspan=7, pady=10)

# Day of week labels
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
for i, day in enumerate(days):
    tk.Label(root, text=day, font=("Arial", 12, "bold")).grid(row=1, column=i)

# Calendar body
cal = calendar.monthcalendar(current_year, current_month)
for week_num, week in enumerate(cal):
    for day_num, day in enumerate(week):
        if day == 0:
            label = tk.Label(root, text="", width=4, height=2)
        else:
            label = tk.Button(root, text=str(day), width=4, height=2)
        label.grid(row=week_num+2, column=day_num)

# Run the app
root.mainloop()