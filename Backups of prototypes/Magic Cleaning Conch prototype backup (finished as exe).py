import tkinter as tk
import random
import time
import winsound


dirtprompt = f"STOP!\n Look around.\n List all small areas you see that are dirty.\n Use commas.\n (i.e. computer desk, kitchen table, trash can, counter, etc)"
button_clicked = False
litter = ("Surprise task!\nClean the litter boxes!")
fridge = ("Surprise task!\nClean out the fridge!")
answers = [litter, fridge]

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
            tyme = random.randint(3,10)
        else:
            todo = random.choice(dirty_list).strip()
            tyme = random.randint(3,10)
        cleananswer = ""
        if "trash" in result_text or "can" in result_text or "garbage" in result_text:
            cleananswer = f"clean {todo} for {tyme} minutes"
        if random.randint(1,100) <= 16 and not ("trash" in result_text or "can" in result_text or "garbage" in result_text):
            cleananswer = random.choice(answers)
        else:
            cleananswer = f"Clean {todo} for {tyme} minutes"   
        result_text += f"\n{cleananswer}"
    else:
        result_text = "Do Nothing"


    result_label.config(text=result_text)

root = tk.Tk()
root.title("Magic (Cleaning) Conch")
root.wm_attributes('-topmost', True,)
winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
root.geometry("+800+400")

prompt_label =tk.Label(root, text = dirtprompt, fg = 'purple', bg = 'yellow', font = 22)
prompt_label.pack()

entry = tk.Entry(root, width=50, bg = 'white')
entry.pack()

submit_button = tk.Button(root, command=proccess_input,text = "Pull the string", bg = 'brown', fg = 'yellow',) 
submit_button.pack()


result_label = tk.Label(root, text="", font = 22)
result_label.pack()

root.mainloop()