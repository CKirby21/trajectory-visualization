from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Frame, Entry, Label, Button, Tk, TOP
from body_arm_trajectory import Main

# def plot(s, d):

#     frm_plot = Frame(ROOT, padx=10, pady=10)
#     frm_plot.pack(side=RIGHT)
#     pb['value'] = 0
#     ROOT.update_idletasks()
#     responses = []
#     for i in range(3):
#         r = report.GetQuanitity(headers_authorization, s, d, i)
#         responses.append(r)
#         pb['value'] += 25
#         ROOT.update_idletasks()
#     responses = list(filter(None, responses))
#     figure = report.PlotThreeQuantities(responses, 3, sites[s] + ' - ' + devices[s][d])
#     pb['value'] += 25
#     ROOT.update_idletasks()
    
#     # Populates window with matplotlib figure
#     canvas = FigureCanvasTkAgg(figure, frm_plot)
#     canvas.get_tk_widget().pack(fill=BOTH)

#     # Remove the old plot
#     global frm_old_plot
#     if frm_old_plot != None:
#         frm_old_plot.destroy()
#     frm_old_plot = frm_plot


# def site_submit(s):
    
#     frm_device = Frame(ROOT, padx=10, pady=10)
#     frm_device.pack(side=LEFT)
#     if len(devices[s]) > 1:
        
#         lbl = Label(frm_device, text="Choose a device:", font = ("Times New Roman", 16, 'bold'))
#         lbl.pack(side=TOP, pady=5)
#         device_choice = IntVar()
#         device_choice.set(-1)
#         for i,device_name in enumerate(devices[s]):
#             btn_rad = Radiobutton(frm_device, text=device_name, indicatoron=0, variable=device_choice, value=i, command=lambda: plot(s, device_choice.get()))
#             btn_rad.configure(font=("Times New Roman", 12))
#             btn_rad.pack(side=TOP, pady=5)
            
#     else:
#         plot(s, 0)
    
#     # Remove the old device frame
#     global frm_old_device
#     if frm_old_device != None:
#         frm_old_device.destroy()
#     frm_old_device = frm_device

def click(entBodyHeight:Entry, entArmLength:Entry, entArmVelocity:Entry):
    bodyHeight = float(entBodyHeight.get())
    armLength = float(entArmLength.get())
    armVelocity = float(entArmVelocity.get())
    Main(bodyHeight,armLength,armVelocity)

def quit_me():
    ROOT.quit()
    ROOT.destroy()


if __name__ == '__main__':

    # Configure Window
    ROOT = Tk()
    ROOT.protocol("WM_DELETE_ROOT", quit_me)
    ROOT.geometry('+120+20') #1200x800
    ROOT.resizable(False,False)
    FONT = ("Times New Roman", 14, 'bold')


    frame = Frame(ROOT, pady=10, padx=10)
    frame.pack()
    lbl = Label(frame, text="Trajectory Visualization", font = ("Times New Roman", 20, 'bold'))
    lbl.pack(side=TOP)

    subframe = Frame(frame, pady=5)
    subframe.pack()
    lbl = Label(subframe, text="Height of Body (ft):", font = FONT)
    lbl.pack(side='left')
    entBodyHeight = Entry(subframe)
    entBodyHeight.insert(0, '212')
    entBodyHeight.pack(side='left')

    subframe = Frame(frame, pady=5)
    subframe.pack()
    lbl = Label(subframe, text="Length of Arm (ft):", font = FONT)
    lbl.pack(side='left')
    entArmLength = Entry(subframe)
    entArmLength.insert(0, '116')
    entArmLength.pack(side='left')

    subframe = Frame(frame, pady=5)
    subframe.pack()
    lbl = Label(subframe, text="Velocity of Arm (mph):", font = FONT)
    lbl.pack(side='left')
    entArmVelocity = Entry(subframe)
    entArmVelocity.insert(0, '180')
    entArmVelocity.pack(side='left')

    btn = Button(frame, text="Plot", font = FONT, command=lambda: click(entBodyHeight,entArmLength,entArmVelocity))
    btn.pack(side='bottom')

    ROOT.mainloop()

        