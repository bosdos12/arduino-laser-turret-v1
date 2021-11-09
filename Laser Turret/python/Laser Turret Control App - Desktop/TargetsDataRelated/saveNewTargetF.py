from tkinter import messagebox
import tkinter as tk
import cv2 as cv

def saveNewTargetF(self, maxTargetsCount):

    # New target data holders;


    
    # Making sure current target's count is less then the max targets count;
    tkWindow = tk.Tk()
    if len(self.ALLTARGETBBOXDATAOBJECTSARRAY) < maxTargetsCount:
        # Success;
        successfull, cameraframe = self.CAMERACAPTURE.read()
        bbox = cv.selectROI("Select new target", cameraframe, False)

        # Asking for the data from the user;
        tkWindow.geometry("200x200")
        tkWindow.resizable(False, False)
        tkWindow.title("Name the new target.")


        nameNewTargetEntry = tk.Entry(tkWindow, width=28)
        nameNewTargetEntry.place(x=10, y=10)


        tk.Button(tkWindow, text="Save", bg="green", fg="white", width=5, height=1, command=lambda: actuallySaveTheNewTargetF(self, nameNewTargetEntry.get(), bbox, cameraframe, tkWindow)).place(x=50, y=40)
        tk.Button(tkWindow, text="Cancel", bg="red", fg="white", width=5, height=1, command=lambda: tkWindow.destroy()).place(x=100, y=40)

        




        tkWindow.mainloop()




    else:
        tkWindow.withdraw()
        messagebox.showinfo("Cant add new target.", "You already have the max amount of targets selected.")

def actuallySaveTheNewTargetF(self, name, bbox, cameraframe, tkWindow):
    if (len(name) > 0):
        # Adding the target to the targets list;
        self.ALLTARGETBBOXDATAOBJECTSARRAY.insert(0, {"bbox": bbox, "tracker": cv.TrackerMOSSE_create(), "name": name, "visible": True, "isCurrentLockedTarget": False})
        # Initialising the tracker;
        self.ALLTARGETBBOXDATAOBJECTSARRAY[0]["tracker"].init(self.CURRENTCAMERAFRAME, self.ALLTARGETBBOXDATAOBJECTSARRAY[0]["bbox"])

        # Clearing the window;
        tkWindow.destroy()
    else:
        messagebox.showinfo("Invalid name", "Please name the target")
        