from tkinter import *

root  =  Tk()  # create root window
root.title("Basic GUI Layout with Grid")
root.maxsize(800,  600)  # width x height
root.config(bg="skyblue")
# root.resizable(False, False)

# Create left and right frames

subFrame  =  Frame(root,  width=200,  height=  600,  bg='white')
subFrame.grid_propagate(False)
subFrame.grid(row=0,  column=0, sticky='NESW')

previewImageFrame  =  Frame(subFrame,  width=200,  height=  200,  bg='blue')
previewImageFrame.grid_propagate(False)
previewImageFrame.grid(row=0,  column=0, sticky='NESW')

imageStageFrame  =  Frame(subFrame,  width=200,  height=  200,  bg='purple')
imageStageFrame.grid_propagate(False)
imageStageFrame.grid(row=1,  column=0, sticky='NESW')

getUserNameFrame  =  Frame(subFrame,  width=200,  height=  200,  bg='black')
getUserNameFrame.grid_propagate(False)
getUserNameFrame.grid(row=2,  column=0, sticky='NESW')

mainFrame  =  Frame(root,  width=600,  height=600,  bg='orange')
mainFrame.grid_propagate(False)
mainFrame.grid(row=0,  column=1, sticky='NESW')

userNamePromptFrame  =  Frame(mainFrame,  width=600,  height=50,  bg='red')
userNamePromptFrame.pack_propagate(False)
userNamePromptFrame.grid(row=0, column=0,sticky='NESW')

drawGesturePromptFrame  =  Frame(mainFrame,  width=600,  height=50,  bg='orange')
drawGesturePromptFrame.pack_propagate(False)
drawGesturePromptFrame.grid(row=1, column=0,sticky='NESW')

boardFrame  =  Frame(mainFrame,  width=600,  height=400,  bg='green')
boardFrame.pack_propagate(False)
boardFrame.grid(row=2, column=0,sticky='NESW')

actionButtonFrame = Frame(mainFrame, width = 600, height=100, bg= 'teal')
actionButtonFrame.grid_propagate(False)
actionButtonFrame.grid(row=3, column=0, sticky='NSEW')
actionButtonFrame.columnconfigure((0,1), weight=1)
actionButtonFrame.rowconfigure(0, weight=1)

clearButtonFrame = Button(actionButtonFrame, bg='brown', text='Clear')
clearButtonFrame.grid(row = 0, column= 0, sticky='NSEW')

submitButtonFrame = Button(actionButtonFrame, bg='yellow', text='Submit')
submitButtonFrame.grid(row = 0, column= 1, sticky='NSEW')

userNamePromptLabel = Label(userNamePromptFrame, text = "Prompt 1", bg='purple')
userNamePromptLabel.pack(expand=True, fill=BOTH)

drawGesturePromptLabel = Label(drawGesturePromptFrame, text = "Prompt 2", bg='teal')
drawGesturePromptLabel.pack(expand=True, fill=BOTH)

# board = Canvas(boardFrame, bg='white')
# board.pack(expand=True, fill = BOTH)

# # Create frames and labels in subFrame
# Label(subFrame,  text="Original Image",  relief=RAISED).grid(row=0,  column=0,  padx=5,  pady=5)
# image  =  PhotoImage(file="arrow.gif")  # edit the file name to use a different image
# original_image  =  image.subsample(3,3)

# Label(subFrame,  image=original_image).grid(row=1,  column=0,  padx=5,  pady=5)
# # Label(mainFrame,  image=image,  bg='grey').grid(row=0,  column=0,  padx=5,  pady=5)
# board = Canvas(mainFrame, width=400, height=400, bg='white').grid(row=0,  column=0,  padx=5,  pady=5)

# tool_bar  =  Frame(subFrame,  width=180,  height=185,  bg='grey')
# tool_bar.grid(row=2,  column=0,  padx=5,  pady=5)

# def clicked():
#     '''if button is clicked, display message'''
#     print("Clicked.")

# # Example labels that serve as placeholders for other widgets
# Label(tool_bar,  text="Tools",  relief=RAISED).grid(row=0,  column=0,  padx=5,  pady=3,  ipadx=10)
# Label(tool_bar,  text="Filters",  relief=RAISED).grid(row=0,  column=1,  padx=5,  pady=3,  ipadx=10)

# # For now, when the buttons are clicked, they only call the clicked() method. We will add functionality later.
# Button(tool_bar,  text="Select",  command=clicked).grid(row=1,  column=0,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
# Button(tool_bar,  text="Crop",  command=clicked).grid(row=2,  column=0,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
# Button(tool_bar,  text="Rotate &amp; Flip",  command=clicked).grid(row=3,  column=0,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
# Button(tool_bar,  text="Resize",  command=clicked).grid(row=4,  column=0,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
# Button(tool_bar,  text="Black &amp; White",  command=clicked).grid(row=1,  column=1,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
root.mainloop()