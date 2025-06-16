import os
import subprocess
import sys
import threading
import time
import tkinter as tk
import ctypes as ct
import webbrowser

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Window(tk.Tk):
    def __init__(self, resolution: str, title: str, icon: str):#, server, client):
        super().__init__()
        self.withdraw()
        self.resizable(False, False)
        self.geometry(f"{resolution}+{round(self.winfo_screenwidth() / 2) - 400}+{round(self.winfo_screenheight() / 2) - 300}")
        self.title(title)
        _icon = tk.PhotoImage(file=icon)
        self.iconphoto(False, _icon)
        self.configure(bg="gray5", takefocus=True)

        try:
            hwnd = ct.windll.user32.GetParent(self.winfo_id())
            value = ct.c_int(2)
            if ct.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ct.byref(value), ct.sizeof(value)) != 0:
                ct.windll.dwmapi.DwmSetWindowAttribute(hwnd, 19, ct.byref(ct.c_int(value)), ct.sizeof(ct.c_int(value)))
        except TypeError:
            pass

        from widgets import Widgets, CreateToolTip
        self.widgets = Widgets(self)

        locate_output_file_button_image = tk.PhotoImage(file="assets\\output.png").subsample(6, 6)
        locate_output_file_button = tk.Button(self, image=locate_output_file_button_image, command=lambda: subprocess.Popen(f'explorer "{os.getcwd()}\\output"'), height=48, width=48, background="gray5", foreground="gray100", borderwidth=0, activebackground="gray10", activeforeground="gray100", relief=tk.SUNKEN)
        locate_output_file_button.place(x=0, y=600, anchor="sw")
        CreateToolTip(locate_output_file_button, "Opens the output folder where your files end up after receiving them", 1000)

        locate_default_gateway_button_image = tk.PhotoImage(file="assets\\gateway.png").subsample(6, 6)
        locate_default_gateway_button = tk.Button(self, image=locate_default_gateway_button_image, command=lambda: webbrowser.open_new_tab(f"{self.widgets.server.default_gateway}"), height=48, width=48, background="gray5", foreground="gray100", borderwidth=0, activebackground="gray10", activeforeground="gray100", relief=tk.SUNKEN)
        locate_default_gateway_button.place(x=48, y=600, anchor="sw")
        CreateToolTip(locate_default_gateway_button, "Opens the default gateway in the browser so you can portforward the secret port *5609*", 1000)


        self.protocol('WM_DELETE_WINDOW', lambda: self.destroy())# == threading.Thread(target=server.stop, daemon=True).start())

        self.deiconify()
        self.focus_force()

        self.mainloop()

if __name__ == '__main__':
    Window("800x600", "Personal File Transmitter", f"{resource_path("assets\\gateway.png")}")
    time.sleep(1)
