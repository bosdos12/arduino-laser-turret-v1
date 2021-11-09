import tkinter as tk

from pygame import mouse

def clickTargetButtonF(self, ClickIndex, mousePosition):
    print(mousePosition)

    # Creating a "menu" gui consisting of "lock, re-select, delete, cancel";
    root = tk.Tk()
    root.overrideredirect(1)
    root.attributes('-topmost', True)
    root.geometry(f"100x100+{str(mousePosition[0])}+{str(mousePosition[1])}")

    tk.Button(root, text="Lock", command=lambda: lockF(self, ClickIndex, root)).pack()
    tk.Button(root, text="Re Select", command=lambda: reSelectF()).pack()
    tk.Button(root, text="Delete", command=lambda: deleteF(self, root, ClickIndex)).pack()
    tk.Button(root, text="Cancel", command=root.destroy).pack()


    root.mainloop()


def lockF(self, ClickIndex, root):
    # Setting the old locked targets "isCurrentLockedTarget" attribute to False;
    for targetsData in self.ALLTARGETBBOXDATAOBJECTSARRAY:
        targetsData["isCurrentLockedTarget"] = False
    
    # Setting the new locked target;
    self.ALLTARGETBBOXDATAOBJECTSARRAY[ClickIndex]["isCurrentLockedTarget"] = True # Setting its properties to the currentLockedTarget: True;
    self.currentLockedTarget = self.ALLTARGETBBOXDATAOBJECTSARRAY[ClickIndex]


    # Closing the menu bar;
    root.destroy()

def reSelectF():
    print("reSelected")

def deleteF(self, root, ClickIndex):
    del self.ALLTARGETBBOXDATAOBJECTSARRAY[ClickIndex]
    root.destroy()

