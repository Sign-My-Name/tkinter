logger.info(f"initialazing homePage")
### region Homepage
home_top_frame = tk.Frame(root, bg=BG_COLOR)
home_middle_frame = tk.Frame(root, bg=BG_COLOR)
home_bottom_frame = tk.Frame(root, bg=BG_COLOR)

logo_label = tk.Label(home_top_frame, image=logo_img, bg=BG_COLOR ) #bg=BG_COLOR
logo_label.pack(side='top', fill='x')


left_frame = tk.Frame(home_middle_frame, bg=BG_COLOR)  
left_frame.pack(side="left")

left_button = tk.Button(left_frame, image=het_img, bg=BG_COLOR, borderwidth=0,
                        command=lambda: [start_camera(), show_name_breakdown_frame(home_top_frame, home_middle_frame, home_bottom_frame)])
left_button.pack()
left_button_label = tk.Label(left_frame, text="בואו נלמד כיצד", bg=BG_COLOR, fg="black", font=("Calibri", 20))
left_button_label.pack(pady=0)

practice_label = tk.Label(left_frame, text="לכתוב את השם שלכם", bg=BG_COLOR, fg="black", font=("Calibri", 20))
practice_label.pack(pady=0)

boy_label = tk.Label(home_middle_frame, image=boy_img, bg=BG_COLOR)
boy_label.pack(side="left")

right_frame = tk.Frame(home_middle_frame, bg=BG_COLOR)
right_frame.pack(side="left", padx=10)
right_button = tk.Button(right_frame, image=shin_img, bg=BG_COLOR, borderwidth=0, #bd=0, activebackground=BG_COLOR,
                         command=lambda: [start_camera(),show_identify_frame(home_top_frame, home_middle_frame, home_bottom_frame)])
right_button.pack()
right_button_label = tk.Label(right_frame, text="בואו נתרגל", bg=BG_COLOR, fg="black", font=("Calibri", 20))
right_button_label.pack(pady=2)

practice_label = tk.Label(right_frame, text="אותיות ביחד", bg=BG_COLOR, fg="black", font=("Calibri", 20))
practice_label.pack(pady=0)


welcome_label = tk.Label(home_bottom_frame, text="!היי חברים, ברוכים הבאים", font=("Calibri", 34),  bg=BG_COLOR, fg="black") #bg=BG_COLOR
welcome_label.pack(side='left', padx=30)

######## build a word

build_a_word_button = tk.Button(home_bottom_frame, text = "בנה מילה", font=("Calibri", 34),  bg=BG_COLOR, fg="black",
                                 command= lambda:
                                   [start_camera(),
                                     show_build_a_word_frame(home_top_frame, home_middle_frame, home_bottom_frame)
                                     ])
build_a_word_button.pack(side='bottom', padx=30)

####### build a word




home_top_frame.pack(pady=10)
home_middle_frame.pack()
home_bottom_frame.pack(pady=10)

### end region homepage