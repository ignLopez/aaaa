from tkinter import Tk
from resources.window_screen import MainWindow

window = Tk()
# window.geometry("500x600+300+300")
window.title('Finanzas Domesticas')
app = MainWindow(window)
window.mainloop()