import tkinter as tk

#window.destroy()

def Tk_done():
    global entry1,entry2,window
    Rows = entry1.get()
    Mines = entry2.get()
    Rows,Mines = int(Rows),int(Mines)
    print(Rows,Mines)
    if Rows > 20 or Mines > (Rows*Rows):
        print ("please choose smaller values")
        Custom()
    else:
        return Rows,Mines
        window.destroy()
        print("ass")



def Custom():
    global entry1,entry2,window
    window = tk.Tk()
    label = tk.Label(window,
                     text = "Custom Game",
                        fg = "white",
                        bg = "blue",
                        width = 10,
                        height = 1)
    frame_a = tk.Frame()
    frame_b = tk.Frame()
    frame_c = tk.Frame()

    labelR = tk.Label(master = frame_a,text = "Rows")
    labelM = tk.Label(master = frame_b,text = "Mines")

    entry1 = tk.Entry(master = frame_a)
    entry2 = tk.Entry(master = frame_b)

    button = tk.Button(master = frame_c,text = "Enter", command = Tk_done)

    label.pack()
    labelR.pack()
    labelM.pack()
    entry1.pack()
    entry2.pack()
    button.pack()
    frame_a.pack()
    frame_b.pack()
    frame_c.pack()

    #window.mainloop()




