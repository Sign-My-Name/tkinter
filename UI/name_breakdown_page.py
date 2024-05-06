### region name_breakdown
logger.info(f"initialazing name breakdown page")
# Create frames for name_breakdown
name_breakdown_top_frame = tk.Frame(root, bg=BG_COLOR)
name_breakdown_middle_frame = tk.Frame(root, bg=BG_COLOR)
name_breakdown_bottom_frame = tk.Frame(root, bg=BG_COLOR)

# Add widgets to the top frame
name_breakdown_header = tk.Label(name_breakdown_top_frame, text="?מה השם שלך", font=("Calibri", 20),  bg=BG_COLOR, fg="black") #bg=BG_COLOR
name_breakdown_header.pack(side="top", padx=0)

submit_button = tk.Button(name_breakdown_top_frame, image=submit_img, bg=BG_COLOR, borderwidth=0,
                          highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0,
                          command=lambda: break_down_name(name_entry.get(), letter_label, congrats_label))
submit_button.pack(side="left", padx=10)

name_entry = tk.Entry(name_breakdown_top_frame, font=("Calibri", 20), justify="right")
name_entry.pack(side="left", padx=10)

name_back_button = tk.Button(name_breakdown_top_frame, image=back_img, bg=BG_COLOR, borderwidth=0,
                             highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0,
                             command=lambda: [close_camera(), show_home_frame(name_breakdown_top_frame, name_breakdown_middle_frame, name_breakdown_bottom_frame, video_label)])
name_back_button.pack(side="right", padx=10)



# Add widgets to the middle frame

next_button = tk.Button(name_breakdown_middle_frame, image=next_img, bg=BG_COLOR, borderwidth=0,
                        highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0,
                        command=lambda: display_next_letter(name_letters, letter_label, next_button, congrats_label))
next_button.pack_forget()  

congrats_label = tk.Label(name_breakdown_middle_frame, bg=BG_COLOR, font=("Arial", 20))
congrats_label.pack(side="bottom", pady=0)

letter_label = tk.Label(name_breakdown_middle_frame, bg=BG_COLOR)
letter_label.pack(side="left", padx=0)

# Function to break down the name into letters
def break_down_name(name, letter_label,  congrats_label):
    global name_letters, current_letter_index
    name_letters = list(name)
    if len(name_letters) <=0:
        return
    display_letter_image(name_letters[0], letter_label)
    congrats_label.config(text="")
    current_letter_index = 0
    # next_button.pack(side="left", padx=20)  # Move this line here

def check_prediction(letter_label, current_letter, ):
    flag = 0
    lock_prediction.acquire()
    try:
        if prediction == current_letter:
            next_button.pack(side="left", padx=20)  # Show the next_button
            flag = 1
            image = Image.open(r"letters\empty.png")
            image = ImageOps.exif_transpose(image)  
            image = ImageTk.PhotoImage(image.resize((300, 300), Image.LANCZOS))
            letter_label.config(image=image)
        else:
            letter_label.config(fg="red")
    finally:
        lock_prediction.release()
    
    if flag:
        return
    root.after(100, check_prediction, letter_label, current_letter)

# Function to display the letter image
def display_letter_image(letter, label):
    if letter =='ן':
        letter = "נ"
    image_file = f"letters/{letter}.png"
    if os.path.exists(image_file):
        image = Image.open(image_file)
        image = ImageOps.exif_transpose(image)  # Rotate the image based on EXIF metadata
        image = ImageTk.PhotoImage(image.resize((300, 300), Image.LANCZOS))
        label.config(image=image, fg="black")  # Reset the foreground color
        label.image = image  # Keep a reference to prevent garbage collection
        root.after(100, check_prediction, label, letter)  # Start the prediction checking loop
    else:
        label.config(text=letter, image="")  # Clear the image reference

# Function to display the next letter
def display_next_letter(name_letters, letter_label, next_button, congrats_label):
    global current_letter_index
    try:
        next_button.pack_forget()  # Hide the next_button
        current_letter_index += 1
        if current_letter_index < len(name_letters):
            display_letter_image(name_letters[current_letter_index], letter_label)
            congrats_label.config(text="")
        else:
            congrats_label.config(text="!כל הכבוד")
    except Exception as e:
        print(f"Error: {e}")

### end region name_breakdown