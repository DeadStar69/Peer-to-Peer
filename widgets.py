import customtkinter


class CreateToolTip:
    def __init__(self, widget, text: str, wait_time: int):
        self.wait_time = wait_time
        self.wrap_length = 250
        self.widget = widget
        self.text = text
        self.root = self.widget.winfo_toplevel()
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.wait_time, self.showtip)

    def unschedule(self):
        _id = self.id
        self.id = None
        if _id:
            self.widget.after_cancel(_id)

    def showtip(self, event=None):
        x = self.widget.winfo_pointerx() + 20
        y = self.widget.winfo_pointery()
        self.hidetip()
        self.tw = tk.Toplevel(self.widget, bg="gray50")
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}")
        tk.Label(self.tw, text=self.text, justify='left', foreground="gray100",
                         background="gray5", relief='solid', borderwidth=0,
                         wraplength = self.wrap_length).pack(padx=2, pady=2)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()
class Widgets:
    def __init__(self):
        pass