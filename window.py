import random
import tkinter as tk
import customtkinter as ctk

from PIL import Image
from pathlib import Path
from filter import process_message
from elements import create_circle_animation

root = ctk.CTk()
typing_after_id = None

# Functions / Definitions (I love em)
def type_greeting(text):
    global typing_after_id

    if typing_after_id is not None:
        root.after_cancel(typing_after_id)
    typing_after_id = None
    greeting_msg.configure(text="")

    def show_next_character(index):
        global typing_after_id

        greeting_msg.configure(text=text[:index])
        if index < len(text):
            typing_after_id = root.after(35, show_next_character, index + 1)
        else:
            typing_after_id = None

    if text:
        show_next_character(1)


def send_msg(event=None):
    msg = text_box.get()

    if msg.strip():
        filtered_msg = process_message(msg)
        type_greeting(filtered_msg)
        print("Sending to LLM:", filtered_msg)
        text_box.delete(0, tk.END)

    return "break"

def optionmenu_command(choice): # TODO  fix the themes, so that the dropdown menu actually works 
    if choice == "Dark Blue":
        ctk.set_default_color_theme("themes/dark-blue.json")
    if choice == "Light":
        ctk.set_default_color_theme("themes/blue.json")
    if choice == "Dark":
        ctk.set_default_color_theme("themes/gold.json")

# Useless / Useful Variables
no = False
yes = True

window_width = 350
window_height = 520
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cord = (screen_width - window_width) // 2
y_cord = (screen_height - window_height) // 2

outline_color_codes = [
    "#25465A",  # Steel blue - separator and default outline
    "#006B68",  # Deep teal - focused outline and button
    "#632A78",  # Dark violet - accent
    "#702C3B",  # Burgundy - alternative accent
    "#28634D"   # Forest green - alternative accent
]

greeting_messages = [
    "Well, look who's here.",
    "A little moment for yourself, perhaps?",
    "What's been on your mind lately?",
    "Come get comfy. We've got things to talk about.",
    "I was just waiting for a little conversation.",
    "So, what's the mood today?",
    "Take a breath. You're right where you need to be.",
    "Got a thought you can't quite put into words?",
    "Let's make this little moment yours.",
    "No rush, no pressure. What shall we get into today?"
]

background_color = "#2c3142"
button_hover_color = "#008078"
text_color = "#E2E8F0"

# Text Box + Send Button (Footer)
bottom_Frame = ctk.CTkFrame(root, fg_color=background_color, corner_radius=0)
bottom_Frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

separator = ctk.CTkFrame(bottom_Frame, height=2, fg_color=outline_color_codes[0], corner_radius=0)
separator.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))

input_row = ctk.CTkFrame(bottom_Frame, fg_color=background_color, corner_radius=0)
input_row.pack(side=tk.BOTTOM, fill=tk.X)

text_box = ctk.CTkEntry(
    input_row, height=38, border_width=2,
    border_color=outline_color_codes[0], font=("Orbitron", 11),
    fg_color=background_color, text_color=text_color,
    placeholder_text="Type a message...", corner_radius=8)
text_box.pack(side=tk.LEFT, fill=tk.X, expand=yes)
text_box.bind("<Return>", send_msg)

send_button = ctk.CTkButton(
    input_row, text="Send", corner_radius=8,
    cursor="hand2", command=send_msg, fg_color=outline_color_codes[1],
    text_color=text_color, hover_color=button_hover_color,
    width=70, height=38)
send_button.pack(side=tk.RIGHT)

# Header 
header = ctk.CTkFrame(root, fg_color=background_color, border_color=background_color, corner_radius=0, height=48, border_width=5)

header.grid_columnconfigure(0, weight=1)
header.grid_columnconfigure(1, weight=0)

header.pack(side=tk.TOP, fill=tk.X)
header.pack_propagate(no)

header_separator = ctk.CTkFrame(
    root,
    height=2,
    fg_color=outline_color_codes[0],
    corner_radius=0,
)
header_separator.pack(side=tk.TOP, fill=tk.X, padx=20, pady=(0, 8))

label = ctk.CTkLabel(header, text="Online", font=("Aral", 16))
label.pack(side="left", padx= 10)

settings_image_path = Path(__file__).resolve().parent / "img" / "settings.png"
settings_image = ctk.CTkImage(
    light_image=Image.open(settings_image_path),
    size=(24, 24),
)

option_menu = tk.Menu(
    header,
    tearoff=no,
    bg=outline_color_codes[1],
    fg=text_color,
    activebackground=button_hover_color,
    activeforeground=text_color,
    font=("Orbitron", 10),
    borderwidth=0,
)
for choice in ["Dark Blue", "Light", "Dark"]:
    option_menu.add_command(
        label=choice,
        command=lambda selected_choice=choice: optionmenu_command(selected_choice),
    )

def show_option_menu():
    try:
        option_menu.tk_popup(
            option_button.winfo_rootx(),
            option_button.winfo_rooty() + option_button.winfo_height(),
        )
    finally:
        option_menu.grab_release()

option_button = ctk.CTkButton(
    header,
    text="",
    image=settings_image,
    command=show_option_menu,
    width=40,
    height=40,
    fg_color=outline_color_codes[1],
    hover_color=button_hover_color,
)
option_button.pack(side="right")

# Animations and greeting

main_content = ctk.CTkFrame(root, fg_color=background_color, corner_radius=0)
main_content.pack(side=tk.TOP, fill=tk.BOTH, expand=yes)

animation_canvas = create_circle_animation(main_content, background_color)
animation_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=yes, padx=20, pady=(20, 0))

greeting_msg = ctk.CTkLabel(
    main_content,
    text="",
    font=("Orbitron", 16),
    wraplength=250,
    justify="center",
    width=250,
    height=140,
)
greeting_msg.pack(side=tk.TOP, pady=(0, 20))

# Window Specifics
root.title("Anna")
root.geometry(f"{window_width}x{window_height}+{x_cord}+{y_cord}")
root.resizable(no, no)
root.configure(fg_color=background_color)

icon_path = Path(__file__).resolve().parent / "img" / "window.png"
icon_image = tk.PhotoImage(master=root, file=str(icon_path))
root.iconphoto(no, icon_image)
root.iconbitmap(str(icon_path.with_suffix(".ico")))

type_greeting(random.choice(greeting_messages))
root.after_idle(text_box.focus_set)

root.mainloop()
