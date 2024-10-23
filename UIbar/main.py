import tkinter as tk
 
root = tk.Tk()
root.geometry('400x600')
root.title('SlideBar_Menu') 

menu_bar_colour = '#383838' 

#icon
toggle_icon = tk.PhotoImage(file='images/toggle_btn_icon.png')
home_icon =tk.PhotoImage(file='images/home_icon.png')
service_icon =tk.PhotoImage(file='images/services_icon.png')
update_icon =tk.PhotoImage(file='images/updates_icon.png')
contact_icon =tk.PhotoImage(file='images/contact_icon.png')
about_icon =tk.PhotoImage(file='images/about_icon.png')

def switch_indication(indicator_lb):
    
    home_btn_indicator.config(bg=menu_bar_colour)
    service_btn_indicator.config(bg=menu_bar_colour)
    update_btn_indicator.config(bg=menu_bar_colour)
    contact_btn_indicator.config(bg=menu_bar_colour)
    about_btn_indicator.config(bg=menu_bar_colour)
    
    indicator_lb.config(bg='white')
    
    if menu_bar_frame.winfo_width() > 45:
        fold_menu_bar()

close_btn_icon = tk.PhotoImage(file='images/close_btn_icon.png')

def extending_animation():
    current_width = menu_bar_frame.winfo_width()
    if not current_width >200:
        current_width += 10
        menu_bar_frame.config(width=current_width)
    
        root.after(ms=8, func=extending_animation)
    
def extend_menu_bar():
    extending_animation()
    toggle_menu_btn.config(image=close_btn_icon)
    toggle_menu_btn.config(command=fold_menu_bar)
    
def folding_animation():
    current_width = menu_bar_frame.winfo_width()
    if current_width !=45:
        current_width -= 10
        menu_bar_frame.config(width=current_width)
    
        root.after(ms=8, func=folding_animation)
def fold_menu_bar():
    folding_animation()
    toggle_menu_btn.config(image=toggle_icon)
    toggle_menu_btn.config(command=extend_menu_bar)

menu_bar_frame = tk.Frame(root, bg=menu_bar_colour)

toggle_menu_btn =tk.Button(menu_bar_frame, image=toggle_icon, bg=menu_bar_colour, bd=0, activebackground=menu_bar_colour, command=extend_menu_bar)
toggle_menu_btn.place(x=4, y=10)

home_btn = tk.Button(menu_bar_frame,image=home_icon, bg=menu_bar_colour, bd=0, activebackground=menu_bar_colour, command=lambda: switch_indication(indicator_lb=home_btn_indicator))
home_btn.place(x=9, y=130, width=30, height=40)

home_btn_indicator = tk.Label(menu_bar_frame, bg='white')
home_btn_indicator.place(x=3, y=130, height=40, width=3)

home_page_lb = tk.Label(menu_bar_frame, text='Home', bg=menu_bar_colour, fg='white', font=('Bold', 15), anchor=tk.W)
home_page_lb.place(x=45, y=130, width=100, height=40)

home_page_lb.bind('<Button-1>', lambda e: switch_indication(indicator_lb=home_btn_indicator))

service_btn = tk.Button(menu_bar_frame,image=service_icon, bg=menu_bar_colour, bd=0, activebackground=menu_bar_colour, command=lambda: switch_indication(indicator_lb=service_btn_indicator))
service_btn.place(x=9, y=190, width=30, height=40)

service_btn_indicator = tk.Label(menu_bar_frame, bg=menu_bar_colour)
service_btn_indicator.place(x=3, y=190, height=40, width=3)

service_page_lb = tk.Label(menu_bar_frame, text='Service', bg=menu_bar_colour, fg='white', font=('Bold', 15), anchor=tk.W)
service_page_lb.place(x=45, y=190, width=100, height=40)

service_page_lb.bind('<Button-1>', lambda e: switch_indication(indicator_lb=service_btn_indicator))

update_btn = tk.Button(menu_bar_frame,image=update_icon, bg=menu_bar_colour, bd=0, activebackground=menu_bar_colour, command=lambda: switch_indication(indicator_lb=update_btn_indicator))
update_btn.place(x=9, y=250, width=30, height=40)

update_btn_indicator = tk.Label(menu_bar_frame, bg=menu_bar_colour)
update_btn_indicator.place(x=3, y=250, height=40, width=3)

update_page_lb = tk.Label(menu_bar_frame, text='Update', bg=menu_bar_colour, fg='white', font=('Bold', 15), anchor=tk.W)
update_page_lb.place(x=45, y=250, width=100, height=40)

update_page_lb.bind('<Button-1>', lambda e: switch_indication(indicator_lb=update_btn_indicator))

contact_btn = tk.Button(menu_bar_frame,image=contact_icon, bg=menu_bar_colour, bd=0, activebackground=menu_bar_colour, command=lambda: switch_indication(indicator_lb=contact_btn_indicator))
contact_btn.place(x=9, y=310, width=30, height=40)

contact_btn_indicator = tk.Label(menu_bar_frame, bg=menu_bar_colour)
contact_btn_indicator.place(x=3, y=310, height=40, width=3)

contact_page_lb = tk.Label(menu_bar_frame, text='Contact', bg=menu_bar_colour, fg='white', font=('Bold', 15), anchor=tk.W)
contact_page_lb.place(x=45, y=310, width=100, height=40)

contact_page_lb.bind('<Button-1>', lambda e: switch_indication(indicator_lb=contact_btn_indicator))

about_btn = tk.Button(menu_bar_frame,image=about_icon, bg=menu_bar_colour, bd=0, activebackground=menu_bar_colour, command=lambda: switch_indication(indicator_lb=about_btn_indicator))
about_btn.place(x=9, y=370, width=30, height=40)

about_btn_indicator = tk.Label(menu_bar_frame, bg=menu_bar_colour)
about_btn_indicator.place(x=3, y=370, height=40, width=3)

about_page_lb = tk.Label(menu_bar_frame, text='About', bg=menu_bar_colour, fg='white', font=('Bold', 15), anchor=tk.W)
about_page_lb.place(x=45, y=370, width=100, height=40)

about_page_lb.bind('<Button-1>', lambda e: switch_indication(indicator_lb=about_btn_indicator))

menu_bar_frame.pack(side=tk.LEFT, fill=tk.Y, pady=4, padx=3)
menu_bar_frame.pack_propagate(flag=False)

menu_bar_frame.configure(width=45)
root.mainloop()

