import json
import tkinter as tk
import random
import time
import winsound
from datetime import datetime
import os

dirtprompt = f"STOP!\n Look around.\n List all small areas you see that are dirty.\n Use commas.\n (i.e. computer desk, kitchen table, trash can, counter, etc)"
button_clicked = False
litter = (f"Surprise task!\nClean the litter boxes")
fridge = (f"Surprise task!\nClean out the fridge")     
def log_list(current_list):
    
    dirtlist = "dirtlist.json"
    print("Overwriting with new list at:", os.path.abspath(dirtlist))

    list_string = ", ".join(current_list)

    # Overwrite the file with only the new entry
    with open(dirtlist, "w") as f:
        json.dump(list_string, f)

def log_task(task, duration):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
        "task": task,
        "duration": duration
    }
    todotyme = "todotyme.json"
    print("Saving todo and tyme to:", os.path.abspath(todotyme))
    
    # If file exists and has content, load it
    if os.path.exists(todotyme):
        with open(todotyme, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Append new entry and write back
    data.append(log_entry)
    with open(todotyme, "w") as f:
        json.dump(data, f, indent=4)

def log_complete(timer_up):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
        "timer status":timer_up
    }
    todotyme = "todotyme.json"
    print("Saving completion to:", os.path.abspath(todotyme))

    if os.path.exists(todotyme):
        with open(todotyme, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(log_entry)
    with open(todotyme, "w") as f:
        json.dump(data, f, indent=4)

def open_timer_window(task, duration):
    timer_window = tk.Toplevel(root)
    timer_window.title("Timer")
    timer_window.wm_attributes('-topmost', True)
    timer_window.geometry("+1250+400")

    label = tk.Label(timer_window, text=f"{task}\n{duration} minutes", font=22)
    label.pack(pady=10)

    time_var = tk.StringVar()
    time_var.set(f"{duration:02}:00")
    timer_label = tk.Label(timer_window, textvariable=time_var, font=("Courier", 40))
    timer_label.pack(pady=10)

    def countdown(mins, secs):
        if mins == 0 and secs == 0:
            time_var.set("TIME'S UP!"), (log_complete("complete"), (show_continue_button()))
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            return
        time_var.set(f"{mins:02}:{secs:02}")
        if secs == 0:
            mins -= 1
            secs = 59
        else:
            secs -= 1
        timer_window.after(1000, countdown, mins, secs)
    
    def start_timer():
        countdown(duration, 0)
    
    def show_continue_button():
        continue_button = tk.Button(timer_window, text="continue?", command=List_Reroll)
        continue_button.pack(pady=10)
    
    def List_Reroll(): #logic for pushing continue button on timer 
        with open("dirtlist.json", "r") as f:
            data = json.load(f)
        with open("todotyme.json", "r") as g:
            log_data = json.load(g)
        
        #clean_ dirt = [the task before "completed"]
        clean_dirt = None
        for i in range(len(log_data) - 1, -1, -1):
            entry = log_data[i]
            if entry.get("timer status") == "complete":
                if i > 0:
                    previous_entry = log_data[i - 1]
                    if "task" in previous_entry:
                        clean_dirt = previous_entry["task"]
                break
       
        dyrty_list = [item.strip() for item in data.split(",")]
        #                   VVV dyrty_list without clean_dirt but printable
        new_dyrty_list = [item for item in dyrty_list if clean_dirt.lower() not in item.lower()]
        if clean_dirt in dyrty_list:
            dyrty_list.remove(clean_dirt)
        if "trash" in dyrty_list or "can" in dyrty_list or "garbage" in dyrty_list:
            trash_cans = ["trash", "cans", "can", "garbage"]
            dyrty_list = [item for item in dyrty_list if not any(word in item.lower() for word in trash_cans)]
        if not dyrty_list:
            return
           
        if dyrty_list:
            refined_text = "Here's your revised list: \n"
            for item in dyrty_list:
                refined_text += f"- {item.strip()}\n"
            todo = random.choice(new_dyrty_list).strip()
            tyme = random.randint(int(.2),int(.5))
            refined_answer = ""
            if random.randint(1,100) <= 16:
                
                answers = [litter, fridge]
                refined_answer = f"{random.choice(answers)} for at least {tyme} minutes!"
                todo = refined_answer.split('\n')[-1]
            else:
                refined_answer = f"Clean {todo} for {tyme} minutes"        
            refined_text += f"\n{refined_answer}"
            log_task(todo, tyme)
            log_list(new_dyrty_list) 
            open_timer_window(todo, tyme)
        else:
            refined_text = "Do Nothing"   

        result_label.config(text=refined_text)
       

    start_button = tk.Button(timer_window, text="Start Timer", command=start_timer)
    start_button.pack(pady=5)

def proccess_input():
    global button_clicked
    button_clicked = True
    submit_button.config(text = "Pull the string again")
    dirt = entry.get()
    dirty_list = dirt.split(",")
    
    
    if dirt:
        result_text = "Here's what you listed as dirty:\n"
        for item in dirty_list:
            result_text += f"- {item.strip()}\n"
        if "trash" in result_text or "can" in result_text or "garbage" in result_text:
            todo = "trash cans"
            tyme = random.randint(int(.2),int(.5))
        else:
            todo = random.choice(dirty_list).strip()
            tyme = random.randint(int(.2),int(.5))
        cleananswer = ""
        if "trash" in result_text or "can" in result_text or "garbage" in result_text:
            cleananswer = f"clean {todo} for {tyme} minutes"
        if random.randint(1,100) <= 16 and not ("trash" in result_text or "can" in result_text or "garbage" in result_text):
            answers = [litter, fridge]
            cleananswer = f"{random.choice(answers)} for at least {tyme} minutes!"
            todo = cleananswer.split('\n')[-1]  # Extract the task description
            
        else:
            cleananswer = f"Clean {todo} for {tyme} minutes" 
          
        result_text += f"\n{cleananswer}"
        log_task(todo, tyme)
        log_list(dirty_list) 
        open_timer_window(todo, tyme)
        
    else:
        result_text = "Do Nothing"   

    result_label.config(text=result_text)


root = tk.Tk()
root.title("Magic (Cleaning) Conch")
root.wm_attributes('-topmost', True,)
winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
root.geometry("+725+400")

prompt_label =tk.Label(root, text = dirtprompt, fg = 'purple', bg = 'yellow', font=(22))
prompt_label.pack()

entry = tk.Entry(root, width=50, bg = 'white', font=(22))
entry.pack()

submit_button = tk.Button(root, command=proccess_input,text = "Pull the string", bg = 'brown', fg = 'yellow', font=(22)) 
submit_button.pack()


result_label = tk.Label(root, text="", font=(22))
result_label.pack()

root.mainloop()