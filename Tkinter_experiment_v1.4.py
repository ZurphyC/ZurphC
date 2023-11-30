import threading
import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
from PIL import ImageTk, Image
from threading import Thread, Event
import pygame

df_xlsx = pd.read_excel('TS.xlsx')
global previous_delay
previous_delay = 1
LG = '#b0aeb5' # '#6f6c79'

pygame.mixer.init()


# [1] Making text delayed
def delayed_insert(text, delay):
    global previous_delay

    box.after((previous_delay+delay) * 1000 * fast.get(), lambda: box.insert(tk.END, text))
    box.after((previous_delay + delay) * 1000 * fast.get(), lambda: box.yview(END))
    previous_delay += delay


# [3] Choosing a cycle for working
def cycle_choose():
    cycle = Cycle_combobox.get()

    if cycle == Cycle_array[3]:

        global previousDelay, first_pressure_entry, last_pressure_entry
        previousDelay = 0

        box.delete("1.0", "end")
        box.insert(tk.END, "Solving for Rankine Cycle\n"
                   "\nThe Rankine cycle, also called the Rankine vapor "
                   "\ncycle is a thermodynamic cycle that converts heat"
                   "\ninto mechanical energy. The Rankine cycle is name"
                   "\nafter William Johnson Macquorn Rankine, a 19th "
                   "\ncentury Scottish engineer and physicist known"
                   "\nfor his research in the thermodynamic properties"
                   "\nof steam.", 'color')

        # Initial inputs for Rankine Cycle
        user_input_frame.grid_forget()
        rankine_frame.grid(row=1, column=0, padx=20, pady=20)

        first_pressure_label = tkinter.Label(rankine_frame, text="Pressure in Boiler (P1)")
        last_pressure_label = tkinter.Label(rankine_frame, text="Pressure in Condenser (P2)")
        first_pressure_entry = tkinter.Entry(rankine_frame)
        last_pressure_entry = tkinter.Entry(rankine_frame)

        first_pressure_label.grid(row=1, column=1)
        last_pressure_label.grid(row=1, column=4)
        first_pressure_entry.grid(row=1, column=2)
        last_pressure_entry.grid(row=1, column=5)
        back_button.grid(row=3, column=0, sticky='news', padx=10, pady=10)
        button.grid(row=3, column=0, sticky='news', padx=30, pady=10)
        instant.grid(row=2, column=0, sticky='w', padx=40, pady=10)

        for widget in rankine_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

    elif cycle == "":
        box.delete("1.0", "end")
        box.insert(tk.END, "You did not select anything ._. try again", 'color')

    else:
        box.delete("1.0", "end")
        box.insert(tk.END, "Sorry that feature is not available right now, please choose another cycle", 'color')


# [3] After clicking on "input solve", checks values
def input_solve():
    cycle = Cycle_combobox.get()

    if cycle == Cycle_array[3]:
        boiler_p = float(first_pressure_entry.get())
        condenser_p = float(last_pressure_entry.get())

        if boiler_p == "" or condenser_p == "":
            box.delete("1.0", "end")
            box.insert(tk.END, "Insufficient inputs entered, try again.")

        elif boiler_p <= condenser_p:
            box.delete("1.0", "end")
            box.insert(tk.END, "Pressure of steam in the boiler cannot be lower to the condenser")

        else:
            i = 0
            j = 0
            run_test1 = True
            run_test2 = True
            while run_test1:
                check_value1 = df_xlsx.iloc[i, 0]
                print(check_value1)

                if boiler_p == check_value1:
                    run_test1 = False
                    p1_line_number = i

                    print("Pressure 1:" + str(p1_line_number))

                if check_value1 > 221.2 or i == 191:
                    run_test1 = True
                    box.delete("1.0", "end")
                    box.insert(tk.END,
                               "Sorry the value you input isn't available in our Steam Table library. Please try again")
                i += 1

            while run_test2:
                check_value2 = df_xlsx.iloc[j, 0]
                print(check_value2)

                if condenser_p == check_value2:
                    run_test2 = False
                    p2_line_number = j

                    print("Pressure 2:" + str(p2_line_number))

                if check_value2 > 221.2 or j == 191:
                    run_test2 = True
                    box.delete("1.0", "end")
                    box.insert(tk.END,
                               "Sorry the value you input isn't available in our Steam Table library. Please try again")
                j += 1

            if run_test1 is False and run_test2 is False:
                global load_box
                execute_loading()
                execute_rankine(p1_line_number, p2_line_number)


# [3] When input solve is pressed
def execute_loading():
    rankine_frame.grid_forget()
    back_button.grid_forget()
    instant.grid_forget()
    button.grid_forget()
    print("loading executed")

    load_bottom_frame.grid(row=1, column=0, sticky="news", padx=10, pady=10)

    load_box = tk.Label(load_bottom_frame, text="Wait for process to finish")
    load_box.grid(row=0, column=1, columnspan=3, sticky='ew')
    load_box.configure(font=('PT Serif Regular', 12, 'bold'))

    ribbit = PhotoImage(file='Images/cat 1.png')
    ribbit = ribbit.subsample(10, 10)
    img_ribbit = Label(load_bottom_frame, image=ribbit)
    img_ribbit.image = ribbit
    img_ribbit.grid(row=1, column=0, padx=10)

    ribbit1 = PhotoImage(file='Images/cat 10.png')
    ribbit1 = ribbit1.subsample(5, 8)
    img_ribbit1 = Label(load_bottom_frame, image=ribbit1)
    img_ribbit1.image = ribbit1
    img_ribbit1.grid(row=1, column=2, padx=10)

    ribbit2 = PhotoImage(file='Images/cat 4.png')
    ribbit2 = ribbit2.subsample(10, 10)
    img_ribbit2 = Label(load_bottom_frame, image=ribbit2)
    img_ribbit2.image = ribbit2
    img_ribbit2.grid(row=1, column=1, padx=10)

    ribbit3 = PhotoImage(file='Images/cat 2.png')
    ribbit3 = ribbit3.subsample(10, 10)
    img_ribbit3 = Label(load_bottom_frame, image=ribbit3)
    img_ribbit3.image = ribbit3
    img_ribbit3.grid(row=1, column=3, padx=10)

    ribbit4 = PhotoImage(file='Images/cat 7.png')
    ribbit4 = ribbit4.subsample(10, 10)
    img_ribbit4 = Label(load_bottom_frame, image=ribbit4)
    img_ribbit4.image = ribbit4
    img_ribbit4.grid(row=1, column=4, padx=10)


# [1] Simple rankine cycle working. Just working. No prints
def execute_rankine(p1_line_number, p2_line_number):

        D = 2
        boiler_p = first_pressure_entry.get()
        condenser_p = last_pressure_entry.get()

        length_p1 = 0.01*len(boiler_p)
        length_p2 = 0.01*len(condenser_p)
        print("condenser p length is " + str(len(condenser_p)))
        print("length_p2 is " + str(length_p2))

        create_graph(p1_line_number, p2_line_number)
        save_plot_graph()

        H1 = df_xlsx.iloc[p1_line_number, 6]    # Obtaining H1
        Hg1 = H1                                # Hg1 is H1 as it's on the graph line
        S1 = df_xlsx.iloc[p1_line_number, 3]    # Obtaining S1
        Sg1 = S1                                # Hg1 is H1 as it's on the graph line

        # Solving State 2
        S2 = S1                                 # Straight line down means entropy is the same for State 2
        Hf2 = df_xlsx.iloc[p2_line_number, 5]   # Obtaining all values as per Steam table. Some won't be used
        Hfg2 = df_xlsx.iloc[p2_line_number, 7]
        Hg2 = df_xlsx.iloc[p2_line_number, 6]
        Sf2 = df_xlsx.iloc[p2_line_number, 2]
        Sfg2 = df_xlsx.iloc[p2_line_number, 4]
        Sg2 = df_xlsx.iloc[p2_line_number, 3]

        X2 = (S2 - Sf2) / Sfg2                  # Dryness fraction
        H2 = Hf2 + X2 * Hfg2                    # Enthalpy for State 2

        # Solving State 3
        H3 = Hf2                                # Enthalpy for State 3

        # Solving State 4
        P4 = float(boiler_p)
        P3 = float(condenser_p)
        Vf = 0.001
        Win = Vf * (P4 - P3) * pow(10, 2)       # Work put in
        H4 = Win + H3                           # Enthalpy for State 4

        # Solving Thermal efficiency and the rest
        Wout = H1 - H2                          # Work output
        Wnet = Wout - Win                       # Net work
        Qs = H1 - H4                            # Heat Supplied

        Ther_Eff = Wnet / Qs                    # Thermal efficiency

        # Solving Work Ratio
        WR = Wnet / Wout

        # Solving SSC
        global SSC
        SSC = 3600 / Wnet

        # Graph print
        graph_title.after(4000 * fast.get(), lambda: graph_draw1(p1_line_number, p2_line_number))
        graph_title.after(4000 * fast.get(), lambda: save_plot_graph())
        graph_title.after(11000 * fast.get(), lambda: graph_draw2(p1_line_number, p2_line_number))
        graph_title.after(11000 * fast.get(), lambda: save_plot_graph())
        graph_title.after(16000 * fast.get(), lambda: graph_draw3(p1_line_number, p2_line_number))
        graph_title.after(16000 * fast.get(), lambda: save_plot_graph())
        graph_title.after(19000 * fast.get(), lambda: graph_draw4(p1_line_number, p2_line_number))
        graph_title.after(19000 * fast.get(), lambda: save_plot_graph())

        # Call text print function
        box.tag_configure('color',
                          foreground='#EBE7DD',
                          font=('Meslo LG M DZ', 10))
        box.delete("1.0", "end")
        delayed_insert("\n~~From Steam Table, looking at steam pressure of " + boiler_p + "bar during State 1~~"
                                                                                          "\n[Saturated Water and Steam properties] "
                                                                                          "\n|    Vg    [m^3/kg]|   Uf    [KJ/kg]|    Ug    [KJ/kg]|      Hf      Hfg       Hg     [KJ/kg]"
                                                                                          "|   Sf      Sfg      Sg     [KJ/kgK] |"
                                                                                          "\n\t\t\t\t\t         "
                       + str(Hg1) + "\t\t\t\t\t     "
                       + str(Sg1) + "\t\t       ", 0)

        delayed_insert("\n\nState 4 to State 1 is heat added at constant pressure (→) in boiler [Qs]"
                       "\nSince State 1 is dry saturated steam"
                       "\nS1 = Sg1 = " + str(S1) + " KJ/kgK"
                       "\nH1 = Hg1 = " + str(H1) + " KJ/kg\n", 3)

        delayed_insert("\n~~From Steam Table, looking at steam pressure of " + condenser_p + "bar during State 2~~"
                                                                                             "\n[Saturated Water and Steam properties] "
                                                                                             "\n|    Vg    [m^3/kg]|   Uf    [KJ/kg]|    Ug    [KJ/kg]|      Hf      Hfg       Hg     [KJ/kg]"
                                                                                             "|   Sf      Sfg      Sg     [KJ/kgK] |"
                                                                                             "\n\t\t\t\t\t         "
                       + str(Hf2) + "\t "
                       + str(Hfg2) + "\t "
                       + str(Hg2) + "\t           "
                       + str(round(Sf2, 3)) + "\t"
                       + str(round(Sfg2, 3)) + "\t"
                       + str(round(Sg2, 3)) + "\t\t       ", 4)

        delayed_insert("\n\nState 1 to State 2 is isentropic expansion ( ↓ ) in Turbine [Wout]"
                       "\nS2 = S1 = " + str(round(S1, 3)) + " KJ/kgK"
                                                            "\nSg2 = " + str(round(Sg2, 3)) + " KJ/kgK\n"
                       "\nS2 <= Sg2. State 2 is wet steam with a dryness fraction (X2) of " + str(round(X2, 4)) +
                       "\nH2 = Hf2 + X2 * Hfg2 = " + str(round(H2, D)) + " KJ/kg", 3)

        delayed_insert("\n\nState 2 to 3 is heat rejection at constant pressure (←) in condenser [Qr]"
                       "\nH3 = Hf2 = " + str(round(H3, D)) + " KJ/kg", 5)

        delayed_insert("\n\nState 3 to 4 is Isentropic compression ( ↑ ) in feed pump [Win]"
                       "\nWin = Vf(P4-P3)"
                       "\nWhere specific volume (Vf) is approx 0.001 m^3/kg"
                       "\nWin = H4 - H3"
                       "\nH4 = " + str(H4) + " KJ/kg", 3)

        delayed_insert("\n\nAll states specific enthalpy calculated ✔", 5)

        delayed_insert("\n\nTo find cycle Thermal efficiency (η),"
                       " we need to find Net work (Wnet) and Heat supplied (Qs)"
                       "\n\nWnet = Wout (?) - Win (" + str(round(Win, D)) + ")"
                       "\nWout = H1 - H2 = " + str(round(Wout, D)) + " KJ/kg"
                       "\nWnet = " + str(round(Wout, D)) + " - " + str(round(Win, D)) + " = " + str(round(Wnet, D)) + " KJ/kg", 1)

        delayed_insert("\n\nQs = H1 - H4 = " + str(round(Qs, D)) + " KJ/kg", 4)

        delayed_insert("\n\nη = Wnet / Qs = " + str(round(Ther_Eff, D)) + " or "
                       + str(round(Ther_Eff * 100, D)) + "%", 1)

        delayed_insert("\n\nWork ratio = Wnet / Wgross = " + str(round(WR, 4)) +
                       "\n\nSpecific Steam Consumption = 3600 / Wnet = " + str(round(SSC, D)) + " kg/kWh", 2)

        # Colour
        # Set the colour
        box.tag_config("title", background="#808080", foreground="#1e1f22")
        box.tag_config("title1", background="#bcbec4", foreground="#1e1f22")
        box.tag_config("title_yellow", background="#a68a0d", foreground="#1e1f22")
        box.tag_config("standard", background="#1e1f22", foreground="white")
        box.tag_config("green", background="#1e1f22", foreground="#4c8d28")
        box.tag_config("ding", background="#1e1f22", foreground="#e0a722")
        box.tag_config("info", background="#1e1f22", foreground="#e9c164")

        # Delay reference [1,3,4,3,5,3,5,1,4,1,2]
        # Place the colour
        box.after(1000 * fast.get(), lambda: box.tag_add("title", "2.0", "4.1"))
        box.after(1000 * fast.get(), lambda: box.tag_add("title1", "4.0", "5.100"))
        box.after(1000 * fast.get(), lambda: box.tag_add("title_yellow", "2.49", str(2 + (0.52 + length_p1))))

        box.after(4000 * fast.get(), lambda: box.tag_add("standard", "6.0", "11.0"))
        box.after(4000 * fast.get(), lambda: box.tag_add("info", "7.0", "7.100"))
        box.after(4000 * fast.get(), lambda: box.tag_add("green", "10.11", "10.100"))

        box.after(8000 * fast.get(), lambda: box.tag_add("title", "12.0", "14.1"))
        box.after(8000 * fast.get(), lambda: box.tag_add("title1", "14.0", "15.100"))
        box.after(8000 * fast.get(), lambda: box.tag_add("title_yellow", "12.49", str(12 + (0.52 + length_p2))))

        box.after(11000 * fast.get(), lambda: box.tag_add("info", "17.0", "17.100"))
        box.after(11000 * fast.get(), lambda: box.tag_add("green", "22.22", "22.100"))

        box.after(16000 * fast.get(), lambda: box.tag_add("info", "24.0", "24.100"))
        box.after(16000 * fast.get(), lambda: box.tag_add("green", "25.11", "25.100"))

        box.after(19000 * fast.get(), lambda: box.tag_add("info", "27.0", "27.100"))
        box.after(19000 * fast.get(), lambda: box.tag_add("green", "31.5", "31.100"))

        box.after(24000 * fast.get(), lambda: box.tag_add("ding", "33.0", "33.100"))

        box.after(25000 * fast.get(), lambda: box.tag_add("info", "35.0", "35.100"))
        box.after(25000 * fast.get(), lambda: box.tag_add("green", "39.22", "39.100"))

        box.after(29000 * fast.get(), lambda: box.tag_add("green", "41.15", "41.100"))

        box.after(30000 * fast.get(), lambda: box.tag_add("green", "43.16", "43.100"))

        box.after(32000 * fast.get(), lambda: box.tag_add("green", "45.29", "45.100"))
        box.after(32000 * fast.get(), lambda: box.tag_add("green", "47.42", "47.100"))
        # Finish
        end_bottom_frame.after(35000 * fast.get(), lambda: end_bottom_frame.grid(row=1, column=0, sticky="news", padx=10, pady=10))
        load_box = tk.Label(end_bottom_frame, text="Process Finished", bg=LG, font=('PT Serif Regular', 12, 'bold'))
        load_box.after(35000 * fast.get(), lambda: load_box.grid(row=0, column=0, sticky='news', padx=10, pady=10))
        back_button = tkinter.Button(end_bottom_frame, text="Back", command=back_page)
        back_button.after(35000 * fast.get(), lambda: back_button.grid(row=1, column=0, sticky='ew', padx=10, pady=10))


# [3] Going back a page
def back_page():
    box.delete("1.0", "end")
    load_box.grid_forget()
    load_box.grid_forget()
    back_button.grid_forget()
    back_button.grid_forget()
    user_input_frame.grid_forget()
    rankine_frame.grid_forget()
    instant.grid_forget()
    button.grid_forget()
    bottom_frame.grid_forget()
    # this was stacked below the end bottom frame. Iif I just forget the end bottom frame, this will still show
    load_bottom_frame.grid_forget()
    end_bottom_frame.grid_forget()

    # resets the fast checkbox
    global fast
    fast = tk.IntVar(value=1)
    instant.configure(variable=fast, onvalue=0)

    # resets the previous delay
    global previous_delay
    previous_delay = 0

    # puts the original image
    graph_title2.grid_remove()
    graph_title.grid(row=0, column=0, padx=10, pady=10)
    img_label.grid(row=0, column=0, padx=86)

    bottom_frame.columnconfigure(0, weight=4)  # Gives the column more sections for a longer combobox
    bottom_frame.grid(row=2, column=0, sticky="news", padx=10, pady=10)

    user_input_frame.grid(row=1, column=0, sticky='news', padx=20, pady=20)

    Cycle_label.grid(row=0, column=1, sticky='n', padx=10, pady=38.5)
    Cycle_combobox.grid(row=0, column=2, sticky='ew')
    cycle_button.grid(row=0, column=3, sticky='ew', padx=10, pady=10)

    box.tag_configure('color',
                      foreground='#EBE7DD',
                      font=('Meslo LG M DZ', 16))
    box.insert(tk.END, "You have returned to the home page\n"
                       "Try another configuration?", 'color')


# [0] Here's the Tkinter start. Basically the GUI [Frame] -> [LabelFrame] -> [Label]
window = tk.Tk()
window.geometry("1920x1080")
window.config(bg='#01060F')

window.overrideredirect(True)


def move_app(e):
    window.geometry(f'+{e.x_root}+{e.y_root}')


def quitter(e):
    window.quit()


title_bar = Frame(window, bg="#de3d3a", relief="raised")
title_bar.grid(row=0, column=0, columnspan=5, sticky='ew')
title_bar.bind("<B1-Motion>", move_app)

title_label = Label(title_bar, text="Steam Graph Generator by @Murphy_Chin", bg="#de3d3a", fg="white")
title_label.pack(side=LEFT, pady=0)

close_label = Label(title_bar, text="  X  ", bg="#de3d3a", fg="white", relief="raised", border=1)
close_label.pack(side=RIGHT, pady=4, padx=4)
close_label.bind("<Button-1>", quitter)

left_frame = tk.Frame(window, bg=LG)  # create and defines the frame
left_frame.grid(row=1, column=0, sticky='ne', padx=10, pady=10)  # pack/place/grid position the frame
right_frame = tk.Frame(window, bg=LG)
right_frame.grid(row=1, column=1, sticky='news', pady=10)
bottom_frame = tk.Frame(window, bg=LG)
bottom_frame.columnconfigure(0, weight=4)  # Gives the column more sections for a longer combobox
bottom_frame.grid(row=2, column=0, sticky="news", padx=10, pady=5)
bottom_right_frame = tk.Frame(window, bg=LG)
bottom_right_frame.grid(row=2, column=1, sticky="we", pady=5)

ack_frame = tk.Frame(window, bg=LG)
ack_frame.grid(row=2, column=2, sticky="news", padx=10, pady=5)
ack_labelframe = tk.LabelFrame(ack_frame, text="Acknowledgements & Credits", bg=LG)
ack_labelframe.grid(row=0, column=0, padx=10, pady=10)
ack_label = tk.Label(ack_labelframe, text="Thank you for using Steam Graph Generator by @Murphy_Chin"
                                          "\nSteam Table provided by LearnChemE.com"
                                          "\n\n[Cats drawings]                   [Inspiration]"
                                          "\n@Spooky_bum                    Professor Behrang"
                                          "\n\n[Music MP3]"
                                          "\nCat at the Cafe - fazethecat"
                                          "\nCat Cafe - Tsundere Twintails, James Wiggan"
                                          "\nNeko Atsume BGM"
                                          "\n2010 Toyota Corolla - 2003 Toyota Corolla"
                                          "\nTemmie Village - Toby Fox"
                                          "\nUn Dos Tres"
                                          "\nPortal Radio - GLaDOS"
                                          "\n\n[Code Gurus]"
                                          "\nCode with Hala, Keith Galil, Giraffe Academy", width=53, height=17, bg=LG, justify='left')
ack_label.grid(row=0, column=0, padx=10, pady=10)


music_num = 0


# [5] Play sweet music
def play_music_track(music_num):
    global img_cat
    img_cat.grid_forget()
    if music_num == 0:
        pygame.mixer.music.load("mp3/Cat1Cafe.mp3")
        pygame.mixer.music.play(loops=0)
        cat = PhotoImage(file='Images/cat_nod.gif')
        cat = cat.subsample(2, 2)
    elif music_num == 1:
        pygame.mixer.music.load("mp3/TsundereTwintails.mp3")
        pygame.mixer.music.play(loops=0)
        cat = PhotoImage(file='Images/Loving cat.png')
        cat = cat.subsample(3, 3)
    elif music_num == 2:
        pygame.mixer.music.load("mp3/NekoBGM.mp3")
        pygame.mixer.music.play(loops=0)
        cat = PhotoImage(file='Images/neko atsume.png')
        cat = cat.subsample(1, 1)
    elif music_num == 3:
        pygame.mixer.music.load("mp3/2010TC.mp3")
        pygame.mixer.music.play(loops=0)
        cat = PhotoImage(file='Images/toyota cat.png')
        cat = cat.subsample(1, 1)
    elif music_num == 4:
        pygame.mixer.music.load("mp3/Temmie.mp3")
        pygame.mixer.music.play(loops=0)
        cat = PhotoImage(file='Images/Temmie.png')
        cat = cat.subsample(4, 4)
    elif music_num == 5:
        pygame.mixer.music.load("mp3/123.mp3")
        pygame.mixer.music.play(loops=0)
        cat = PhotoImage(file='Images/mexican-cat-mexican.gif')
        cat = cat.subsample(2, 2)

    img_cat = Label(play_music_labelframe, image=cat, bg=LG)
    img_cat.image = cat
    img_cat.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    track_no.config(text="Now Playing Track " + str(music_num+1) + "/6")


def stop_music():
    global img_cat
    pygame.mixer_music.stop()
    track_no.config(text="Music stopped >:(")

    img_cat.grid_forget()
    cat = PhotoImage(file='Images/base cat.png')
    cat = cat.subsample(1, 1)
    img_cat = Label(play_music_labelframe, image=cat, bg=LG)
    img_cat.image = cat
    img_cat.grid(row=0, column=0, columnspan=3, padx=10, pady=10)


def play_music_current():
    global music_num
    play_music_track(music_num)


def music_prev():
    global music_num
    if music_num == 0:
        print("stop")
    else:
        music_num = music_num - 1
        play_music_track(music_num)


def music_next():
    global music_num
    if music_num == 5:
        print("stop")
    else:
        music_num = music_num + 1
        play_music_track(music_num)


play_music_frame = tk.Frame(window, bg="#6f6c79")
play_music_frame.grid(row=1, column=2, sticky="news", padx=10, pady=10)
play_music_labelframe = tk.LabelFrame(play_music_frame, text="meow mp3 player ( ͡° ᴥ ͡°)", bg="#6f6c79")
play_music_labelframe.grid(row=0, column=0, padx=10, pady=10)

card = Label(play_music_labelframe, bg='#1b1c1f', height=25, width=54)
card.grid(row=0, column=0, columnspan=3, padx=10, pady=5)

track_no = Label(play_music_labelframe, text="Track 0/6", bg='#212024', fg='white')
track_no.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
'''
card = PhotoImage(file='Music_Cardsize.png')
card = card.subsample(1, 1)
img_card = Label(play_music_labelframe, image=card)
img_card.image = card
img_card.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

cat = PhotoImage(file='cat_nod.gif')
cat = cat.subsample(2, 2)
img_cat = Label(play_music_labelframe, image=cat, bg="#959698")
img_cat.image = cat
img_cat.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
'''
cat = PhotoImage(file='Images/cat_nod.gif')
cat = cat.subsample(2, 2)
img_cat = Label(play_music_labelframe, image=cat, bg=LG)
img_cat.image = cat

play_music = Button(play_music_labelframe, text="♫", font=("Helvetica", 30), bg='#bdb7ce', command=play_music_current, activebackground="#bdb7ce")
play_music.grid(row=1, column=0, padx=15, pady=10, columnspan=3, sticky="ew")
prev_music = Button(play_music_labelframe, text=" ◄ ", font=("Helvetica", 30), bg='#bdb7ce', command=music_prev, activebackground="#bdb7ce")
prev_music.grid(row=3, column=0, pady=5)
stop_music = Button(play_music_labelframe, text="   ⬛   ", font=("Helvetica", 20), bg='#bdb7ce', command=stop_music, activebackground="#bdb7ce")
stop_music.grid(row=3, column=1, pady=5, sticky="ns")
next_music = Button(play_music_labelframe, text=" ► ", font=("Helvetica", 30), bg='#bdb7ce', command=music_next, activebackground="#bdb7ce")
next_music.grid(row=3, column=2, pady=5)


# [1] Chatting interface
welcome_msg_title = tk.LabelFrame(left_frame, text="Zurph BOT (⌐■_■)", bg=LG, fg='#212024')  # Outline part
welcome_msg_title.grid(row=0, column=0, padx=10, pady=10)

scrollbar = Scrollbar(welcome_msg_title)  # add a scrollbar
scrollbar.pack(side=RIGHT, fill=Y)

box = tk.Text(welcome_msg_title, yscrollcommand=scrollbar.set)  # Main section
box.configure(height=37.5, width=100, background='#212024', foreground='#EBE7DD', font=('PT Serif Regular', 10, 'bold'))
box.pack()
box.tag_configure('color',
                  foreground='#EBE7DD',
                  font=('Meslo LG M DZ', 16))
box.insert(tk.END, "Hi! Welcome to Steam Graph Generator.exe, a"
                   "\nThermofluids cycle graph and smart calculator"
                   "\napp designed to be used as a tool for learning"
                   "\nand visualising the steam process.\n\n"
                   "Hey I'm Zurph BOT and this box will be used for "
                   "\ngenerating explanations and workings\n\n"
                   "To begin, select the type of Cycle you are working "
                   "\nwith below\n",
           'color')

scrollbar.config(command=box.yview)

# [2] Graph Section
graph_title = tk.LabelFrame(right_frame, text="Graph Plot ⍏❒", bg=LG)
graph_title.grid(row=0, column=0, padx=10, pady=10)

graph_title2 = tk.LabelFrame(right_frame, text="Graph Plotted ⍏❒", bg=LG)

image1 = PhotoImage(file='Images/Aperture.png')
image1 = image1.subsample(1, 1)
img_label = Label(graph_title, image=image1, bg=LG)
img_label.image = image1
img_label.grid(row=0, column=0, padx=86)


def portal_radio():
    global img_cat
    pygame.mixer.music.load("mp3/PortalRadio.mp3")
    pygame.mixer.music.play(loops=0)
    track_no.config(text="Special Track : Portal Radio")

    img_cat.grid_forget()

    cat = PhotoImage(file='Images/Portal Radio.png')
    cat = cat.subsample(2, 2)
    img_cat = Label(play_music_labelframe, image=cat, bg=LG)
    img_cat.image = cat
    img_cat.grid(row=0, column=0, columnspan=3, padx=10, pady=10)


Spooked = PhotoImage(file='Images/cat 6.png')
Spooked = Spooked.subsample(6, 6)
img_label2 = Button(graph_title, image=Spooked, bg=LG, bd=0, command=portal_radio, activebackground=LG)
img_label2.image = Spooked
img_label2.grid(row=0, column=0, padx=86)

graph_text_bot = tk.Label(graph_title, text="Graph will be generated here", bg=LG)
graph_text_bot.grid(row=2, column=0, padx=10, pady=10)


# [2] Generates a graph
def create_graph(p1_line_number, p2_line_number):

    graph_title.grid_forget()
    graph_title2.grid(row=0, column=0, padx=10, pady=10)

    data1 = {'x1': df_xlsx.Sf_T,
             'y': df_xlsx.Temperature}
    df1 = pd.DataFrame(data1)

    data2 = {'x2': df_xlsx.Sg_T,
             'y': df_xlsx.Temperature}
    df2 = pd.DataFrame(data2)

    line1_data = {'line_x1': [df_xlsx.iloc[p1_line_number, 2], df_xlsx.iloc[p1_line_number, 3]],
                  'line_y1': [df_xlsx.iloc[p1_line_number, 1], df_xlsx.iloc[p1_line_number, 1]]}
    line1 = pd.DataFrame(line1_data)

    line2_data = {'line_x2': [df_xlsx.iloc[p2_line_number, 2], df_xlsx.iloc[p2_line_number, 3]],
                  'line_y2': [df_xlsx.iloc[p2_line_number, 1], df_xlsx.iloc[p2_line_number, 1]]}
    line2 = pd.DataFrame(line2_data)

    # Curved Part
    P1_Y_ref = float(df_xlsx.iloc[p1_line_number, 1])
    P1_X_ref = float(df_xlsx.iloc[p1_line_number, 2])
    P2_Y_ref = float(df_xlsx.iloc[p2_line_number, 1])
    P2_X_ref = float(df_xlsx.iloc[p2_line_number, 2])
    P_diff = (P1_Y_ref * 0.12 - P2_Y_ref * 0.12)

    global p1curve_x
    global p1curve_y

    p1curve_x = [0, 0, 0, 0, 0, (P1_X_ref - P2_X_ref)*0.33 + P2_X_ref, (P1_X_ref - P2_X_ref)*0.66 + P2_X_ref, P1_X_ref]
    p1curve_y = [0, 0, 0, 0, 0, (P1_Y_ref - P2_Y_ref)*0.39 + P2_Y_ref, (P1_Y_ref - P2_Y_ref)*0.68 + P2_Y_ref, P1_Y_ref]

    p2curve_x = [0, P2_X_ref * 0.25, P2_X_ref * 0.4, P2_X_ref * 0.66, P2_X_ref]
    p2curve_y = [P2_Y_ref * 0.12, P2_Y_ref * 0.29, P2_Y_ref * 0.415, P2_Y_ref * 0.66, P2_Y_ref]

    for i in range(5):
        #calc = p1curve_y[i]+P_diff
        #p1curve_y.append(calc)
        p1curve_y[i] = p2curve_y[i] + P_diff
        p1curve_x[i] = p2curve_x[i]

    # Num1 curve
    p1curve_data = {'p1curve_x': p1curve_x,
                    'p1curve_y': p1curve_y}
    p1curve = pd.DataFrame(p1curve_data)
    # Num2 curve
    p2curve_data = {'p2curve_x': p2curve_x,
                    'p2curve_y': p2curve_y}
    p2curve = pd.DataFrame(p2curve_data)

    p1curve_extend_x = [0, 2*0.2, 2*0.4, 2*0.55, 2*0.78, 2]
    p1curve_extend_y = [0, 200*0.11, 200*0.26, 200*0.4, 200*0.68, 200]

    p1curve_x_cont = [0, 0, 0, 0, 0, 0]
    p1curve_y_cont = [0, 0, 0, 0, 0, 0]
    p2curve_x_cont = [0, 0, 0, 0, 0, 0]
    p2curve_y_cont = [0, 0, 0, 0, 0, 0]

    for j in range(6):
        p1curve_x_cont[j] = p1curve_extend_x[j] + float(df_xlsx.iloc[p1_line_number, 3])
        p1curve_y_cont[j] = p1curve_extend_y[j] + P1_Y_ref
        p2curve_x_cont[j] = p1curve_extend_x[j] + float(df_xlsx.iloc[p2_line_number, 3])
        p2curve_y_cont[j] = p1curve_extend_y[j] + P2_Y_ref

    # Num1 curve cont
    p1curve_cont_data = {'p1curve_x_cont': p1curve_x_cont,
                         'p1curve_y_cont': p1curve_y_cont}
    p1curve_cont = pd.DataFrame(p1curve_cont_data)
    p2curve_cont_data = {'p2curve_x_cont': p2curve_x_cont,
                         'p2curve_y_cont': p2curve_y_cont}
    p2curve_cont = pd.DataFrame(p2curve_cont_data)

    global linegraph, figure, figure_plot
    # Resize your Graph (dpi specifies pixels per inch. When saving probably should use 300 if possible)
    # Creates a new figure - a container for the actual plot
    # Figsize is width/height in inches
    figure = plt.figure(figsize=(9, 8), dpi=300)
    # Adds an axes to the figure
    # Input is number of rows, number of cols, index position
    # Assumes a grid layout
    # small "f" lets the plt. function behave
    figure_plot = figure.add_subplot(1, 1, 1)

    # Place figure on window

    linegraph = FigureCanvasTkAgg(figure, graph_title)
    linegraph.get_tk_widget().grid(row=1, column=0, padx=10, pady=10)

    df1 = df1[['x1', 'y']].groupby('x1').sum()
    df1.plot(kind='line', legend=False, ax=figure_plot,
             color='#1f77b4', linestyle='-.', linewidth=3.5, fontsize=15)

    df2 = df2[['x2', 'y']].groupby('x2').sum()
    df2.plot(kind='line', legend=False, ax=figure_plot,
             color='#1f77b4', linestyle='-.', linewidth=3.5, fontsize=15)

    line1 = line1[['line_x1', 'line_y1']].groupby('line_x1').sum()
    line1.plot(kind='line', legend=False, ax=figure_plot,
               color='#d11181', linestyle='-', linewidth=3.5)

    line2 = line2[['line_x2', 'line_y2']].groupby('line_x2').sum()
    line2.plot(kind='line', legend=False, ax=figure_plot,
               color='#0c30e8', linestyle='-', linewidth=3.5)

    p1curve = p1curve[['p1curve_x', 'p1curve_y']].groupby('p1curve_x').sum()
    p1curve.plot(kind='line', legend=False, ax=figure_plot,
                 color='#d11181', linestyle='-', linewidth=3.5)

    p2curve = p2curve[['p2curve_x', 'p2curve_y']].groupby('p2curve_x').sum()
    p2curve.plot(kind='line', legend=False, ax=figure_plot,
                 color='#0c30e8', linestyle='-', linewidth=3.5)

    p1curve_cont = p1curve_cont[['p1curve_x_cont', 'p1curve_y_cont']].groupby('p1curve_x_cont').sum()
    p1curve_cont.plot(kind='line', legend=False, ax=figure_plot,
                      color='#d11181', linestyle='-', linewidth=3.5)

    p2curve_cont = p2curve_cont[['p2curve_x_cont', 'p2curve_y_cont']].groupby('p2curve_x_cont').sum()
    p2curve_cont.plot(kind='line', legend=False, ax=figure_plot,
                      color='#0c30e8', linestyle='-', linewidth=3.5)

    figure_plot.text((df_xlsx.iloc[p1_line_number, 2]+df_xlsx.iloc[p1_line_number, 3])/2 - 0.5, df_xlsx.iloc[p1_line_number, 1] + 10,
                     str(df_xlsx.iloc[p1_line_number, 0]) + r'bar', fontsize=15, c='red')
    figure_plot.text((df_xlsx.iloc[p2_line_number, 2] + df_xlsx.iloc[p2_line_number, 3]) / 2 - 0.5,
                     df_xlsx.iloc[p2_line_number, 1] + 10,
                     str(df_xlsx.iloc[p2_line_number, 0]) + r'bar', fontsize=15, c='red')


def save_plot_graph():

    figure_plot.set_title('TS Diagram', pad=15, fontsize=20)
    figure_plot.set_ylabel('T', rotation_mode='anchor', rotation=0, labelpad=15, fontsize=18)
    figure_plot.set_xlabel('S    ', labelpad=-5, fontsize=18)

    figure_plot.set_yticks([0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500])
    figure_plot.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    plt.savefig('graph.png', dpi=300)
    linegraph.get_tk_widget().grid_forget()

    image2 = PhotoImage(file='graph.png')
    image2 = image2.subsample(4, 4)
    img_label2 = Label(graph_title2, image=image2)
    img_label2.image = image2
    img_label2.grid(row=0, column=0)


def graph_draw1(p1_line_number, p2_line_number):
    line3_data = {'line_x3': [df_xlsx.iloc[p1_line_number, 2], df_xlsx.iloc[p1_line_number, 3]],
                  'line_y3': [df_xlsx.iloc[p1_line_number, 1], df_xlsx.iloc[p1_line_number, 1]]}
    line3 = pd.DataFrame(line3_data)

    line3 = line3[['line_x3', 'line_y3']].groupby('line_x3').sum()
    line3.plot(kind='line', legend=False, ax=figure_plot,
               color='#b50514', linestyle='-', linewidth=3.5, marker='o', markevery=[-1], markerfacecolor="white", markersize=7)

    P1_Y_ref = float(df_xlsx.iloc[p1_line_number, 1])
    P1_X_ref = float(df_xlsx.iloc[p1_line_number, 2])
    P2_Y_ref = float(df_xlsx.iloc[p2_line_number, 1])
    P2_X_ref = float(df_xlsx.iloc[p2_line_number, 2])

    p1curve_data = {'p1curve_x': p1curve_x[4:],
                    'p1curve_y': p1curve_y[4:]}
    p1curve = pd.DataFrame(p1curve_data)

    p1curve = p1curve[['p1curve_x', 'p1curve_y']].groupby('p1curve_x').sum()
    p1curve.plot(kind='line', legend=False, ax=figure_plot,
                 color='#b50514', linestyle='-', linewidth=3.5, marker='o', markevery=[0], markerfacecolor="white", markersize=7)

    # figure_plot.text(P1_X_ref - 0.5, P1_Y_ref - 70, '→', rotation=60, fontsize=40)
    # figure_plot.text((P1_X_ref+(df_xlsx.iloc[p1_line_number, 3]))/2 - 0.5, P1_Y_ref - 40, '⟶', fontsize=40)
    figure_plot.text(P2_X_ref-0.2, P2_Y_ref + 25, '4', fontsize=15)
    figure_plot.text(df_xlsx.iloc[p1_line_number, 3], P1_Y_ref + 15, '1', fontsize=15)


def graph_draw2(p1_line_number, p2_line_number):
    line3_data = {'line_x3': [df_xlsx.iloc[p1_line_number, 3], df_xlsx.iloc[p1_line_number, 3] + 0.0001],
                  'line_y3': [df_xlsx.iloc[p1_line_number, 1], df_xlsx.iloc[p2_line_number, 1]]}
    line3 = pd.DataFrame(line3_data)

    line3 = line3[['line_x3', 'line_y3']].groupby('line_x3').sum()
    line3.plot(kind='line', legend=False, ax=figure_plot,
               color='#b50514', linestyle='-', linewidth=3.5, marker='o', markevery=[0, -1], markerfacecolor="white", markersize=7)

    # figure_plot.text(df_xlsx.iloc[p1_line_number, 3]-0.8, (df_xlsx.iloc[p1_line_number, 1]+df_xlsx.iloc[p2_line_number, 1])/2, '→', rotation=270, fontsize=40)
    figure_plot.text(df_xlsx.iloc[p1_line_number, 3]-0.1, df_xlsx.iloc[p2_line_number, 1] - 25, '2', fontsize=15)


def graph_draw3(p1_line_number, p2_line_number):
    line4_data = {'line_x4': [df_xlsx.iloc[p1_line_number, 3], df_xlsx.iloc[p2_line_number, 2]],
                  'line_y4': [df_xlsx.iloc[p2_line_number, 1], df_xlsx.iloc[p2_line_number, 1]]}
    line4 = pd.DataFrame(line4_data)

    line4 = line4[['line_x4', 'line_y4']].groupby('line_x4').sum()
    line4.plot(kind='line', legend=False, ax=figure_plot,
               color='#b50514', linestyle='-', linewidth=3.5, marker='o', markevery=[0, -1], markerfacecolor="white", markersize=7)

    # figure_plot.text((df_xlsx.iloc[p2_line_number, 2]+df_xlsx.iloc[p1_line_number, 3])/2, df_xlsx.iloc[p2_line_number, 1] + 40, '⟶', rotation=180, fontsize=40)
    figure_plot.text(df_xlsx.iloc[p2_line_number, 2], df_xlsx.iloc[p2_line_number, 1] - 25, '3', fontsize=15)


def graph_draw4(p1_line_number, p2_line_number):
    P1_Y_ref = float(df_xlsx.iloc[p1_line_number, 1])
    P2_Y_ref = float(df_xlsx.iloc[p2_line_number, 1])
    line5_data = {'line_x5': [df_xlsx.iloc[p2_line_number, 2], df_xlsx.iloc[p2_line_number, 2] + 0.0001],
                  'line_y5': [df_xlsx.iloc[p2_line_number, 1], df_xlsx.iloc[p2_line_number, 1] + (P1_Y_ref * 0.12 - P2_Y_ref * 0.12)]}
    line5 = pd.DataFrame(line5_data)

    line5 = line5[['line_x5', 'line_y5']].groupby('line_x5').sum()
    line5.plot(kind='line', legend=False, ax=figure_plot,
               color='#b50514', linestyle='-', linewidth=3.5, marker='o', markevery=[0, -1], markerfacecolor="white", markersize=7)

    # figure_plot.text((df_xlsx.iloc[p2_line_number, 2] + df_xlsx.iloc[p1_line_number, 3]) / 3, df_xlsx.iloc[p2_line_number, 1] + 55, '↑', fontsize=30)


# [3] User input frame, starting with choosing the cycle
user_input_frame = tkinter.LabelFrame(bottom_frame, text="User input section", bg=LG)
user_input_frame.grid(row=1, column=0, sticky='news', padx=20, pady=20)
rankine_frame = tkinter.LabelFrame(bottom_frame)

back_button = tkinter.Button(rankine_frame, text="Back", command=back_page)

Cycle_label = tkinter.Label(user_input_frame, text="Cycle type", font=14)
Cycle_combobox = ttk.Combobox(user_input_frame, values=["Otto cycle", "Diesel cycle", "Dual Combustion cycle",
                                                        "Simple Rankine cycle (Available)", "Rankine cycle with Superheat",
                                                        "Rankine cycle with Reheat",
                                                        "Theoretical cycle with clearance volume",
                                                        "Theoretical cycle with no clearance volume"], font=14)

Cycle_array = ["Otto cycle", "Diesel cycle", "Dual Combustion cycle",
               "Simple Rankine cycle (Available)", "Rankine cycle with Superheat",
               "Rankine cycle with Reheat",
               "Theoretical cycle with clearance volume",
               "Theoretical cycle with no clearance volume"]

Cycle_label.grid(row=0, column=1, sticky='n', padx=10, pady=38.5)
user_input_frame.columnconfigure(2, weight=3)
user_input_frame.columnconfigure(3, weight=1)
Cycle_combobox.grid(row=0, column=2, sticky='ew')

# [3] Solve button
button = tkinter.Button(bottom_frame, text="Enter input and solve", command=input_solve)

# [3] Instant text
fast = tk.IntVar(value=1)
instant = tkinter.Checkbutton(bottom_frame, text="Fast Solve Option", variable=fast, onvalue=0, offvalue=1)

# [3] Cycle Confirm Button
cycle_button = tkinter.Button(user_input_frame, text="Confirm", command=cycle_choose, font=14)
cycle_button.grid(row=0, column=3, sticky='ew', padx=10, pady=10)

# [4] Making the bottom right equation formula
equations_formulas = tk.LabelFrame(bottom_right_frame, text="Equations and Diagrams", bg=LG)
equations_formulas.grid(row=0, column=0, padx=10, pady=15)

'''
equations_formulas_text = tk.Text(equations_formulas, bg='#1e1f22', yscrollcommand=scrollbar.set)  # Main section
equations_formulas_text.configure(height=12, width=75, background='#1e1f22', foreground='#EBE7DD',
                                  font=('Meslo LG M DZ', 10, 'bold'))

equations_formulas_text.grid(row=0, rowspan=2, column=0, padx=10, pady=10)
equations_formulas_text.insert(tk.END, "Work Ratio = Net work/Gross work\n"
                                       "           = (turbine work-feed pump work)/turbine work\n"
                                       "           = ((h1-h2)-(h4-h3))/(h1-h2)\n"
                                       "Heat supplied = (h1-h4)\n"
                                       "Net work = (h1-h2)-(h4-h3)"
                                       "W34 = vf(p4-p3)")
'''

# The card section
card = PhotoImage(file='Cards/Card1.png')
card = card.subsample(1, 1)
img_card = Label(equations_formulas, image=card, bg=LG)
img_card.image = card
img_card.grid(row=0, rowspan=3, column=0, padx=5)

card_num = 0


def card_draw(card_num):

    if card_num == 0:
        card_put = PhotoImage(file='Cards/Card1.png')
    elif card_num == 1:
        card_put = PhotoImage(file='Cards/Card2.png')
    elif card_num == 2:
        card_put = PhotoImage(file='Cards/Card3.png')
    elif card_num == 3:
        card_put = PhotoImage(file='Cards/Card4.png')
    elif card_num == 4:
        card_put = PhotoImage(file='Cards/Card5.png')

    card_put = card_put.subsample(1, 1)
    img_card_put = Label(equations_formulas, image=card_put, bg=LG)
    img_card_put.image = card_put
    img_card_put.grid(row=0, rowspan=3, column=0, padx=5)

    card_no.config(text="Card " + str(card_num+1) + "/5", font=("Helvetica", 10), bg='#212024', fg='white')


def card_move_up():
    global card_num
    if card_num == 0:
        print("stop")
    else:
        card_num = card_num - 1
        card_draw(card_num)


def card_move_down():
    global card_num
    if card_num == 4:
        print("stop")
    else:
        card_num = card_num + 1
        card_draw(card_num)


up_card = Button(equations_formulas, text="▲", font=("Helvetica", 30), bg='#bdb7ce', command=card_move_up)
up_card.grid(row=0, column=1, padx=5)
card_no = Label(equations_formulas, text="Card " + str(card_num+1) + "/5", font=("Helvetica", 10), bg='#212024', fg='white')
card_no.grid(row=1, column=1, padx=5)
down_card = Button(equations_formulas, text="▼", font=("Helvetica", 30), bg='#bdb7ce', command=card_move_down)
down_card.grid(row=2, column=1, padx=5)

load_bottom_frame = tk.LabelFrame(bottom_frame, text="...")
end_bottom_frame = tk.LabelFrame(bottom_frame, text="Done", bg=LG)
end_bottom_frame.columnconfigure(0, weight=4)
load_box = tk.Label(bottom_frame, text="Process Finished")

window.mainloop()