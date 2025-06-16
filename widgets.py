import os
import threading
import time
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import customtkinter as ct


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
    def __init__(self, container: tk.Tk):
        self.container = container
        self.line_colour = 0
        self.switch_state = None
        self.sending_percentage = 0
        self.receiving_percentage = 0
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.layout("sending.Horizontal.TProgressbar", [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
                              {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}),
              ('Horizontal.Progressbar.label', {'sticky': 'nswe'})])
        self.style.configure("sending.Horizontal.TProgressbar", troughcolor="gray20", bordercolor="gray10", background="gray100", foreground="gray0", text="0%", anchor="center", font=("Ariel", 12))

        self.style.layout("receiving.Horizontal.TProgressbar", [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
                              {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}),
              ('Horizontal.Progressbar.label', {'sticky': 'nswe'})])

        self.style.configure("receiving.Horizontal.TProgressbar", troughcolor="gray20", bordercolor="gray10", background="gray100", foreground="gray0", text="0%", anchor="center", font=("Ariel", 12))


        self.topPageMenu()
        self.transmitter_page_frame, self.pair_button, self.pair_entry, self.choose_file_button, self.file_path_entry, self.file_name_entry, self.send_button, self.username_entry, self.auto_accept_switch = self.transmitterPage()
        self.console_page_frame, self.console, self.sending_progress_bar, self.receiving_progress_bar, self.sending_file_name_label, self.receiving_file_name_label = self.consolePage()
        self.display_acceptance_frame = self.displayAcceptanceInfo(" ",False)

    def topPageMenu(self):
        def underLineAnimationToRight():
            if under_line.winfo_x() == 100:
                self.transmitter_page_frame.place(x=self.container.winfo_width() / 2 - 800, y=self.container.winfo_height() / 2 + 60, anchor="center")
                self.console_page_frame.place(x=400, y=self.container.winfo_height() / 2 + 60, anchor="center")
                under_line.configure(width=160)
                under_line.place(x=600, y=70, anchor="center")

        def underLineAnimationToLeft():
            if under_line.winfo_x() == 520:
                self.transmitter_page_frame.place(x=self.container.winfo_width() / 2, y=self.container.winfo_height() / 2 + 60, anchor="center")
                self.console_page_frame.place(x=1200, y=self.container.winfo_height() / 2 + 60, anchor="center")
                under_line.configure(width=200)
                under_line.place(x=200, y=70, anchor="center")

        menu_frame = tk.Frame(self.container, width=800, height=80, bg="gray5")
        menu_frame.columnconfigure(0, weight=1)
        menu_frame.columnconfigure(1, weight=1)

        transmitter_page = tk.Button(menu_frame, text="Transmitter", width=16, background="gray5", foreground="gray100", borderwidth=0, activebackground="gray10", activeforeground="gray100", font=("Ariel", 30), relief=tk.SUNKEN, command=lambda: threading.Thread(target=underLineAnimationToLeft).start())
        transmitter_page.grid(column=0, row=0, padx=15)
        transmitter_page.bind("<Enter>", lambda x: transmitter_page.configure(background="gray2"))
        transmitter_page.bind("<Leave>", lambda x: transmitter_page.configure(background="gray5"))

        extras_page = tk.Button(menu_frame, text="Console", width=16, background="gray5", foreground="gray100", borderwidth=0, activebackground="gray10", activeforeground="gray100", font=("Ariel", 30), relief=tk.SUNKEN, command=lambda: threading.Thread(target=underLineAnimationToRight).start())
        extras_page.grid(column=1, row=0, padx=15)
        extras_page.bind("<Enter>", lambda x: extras_page.configure(background="gray2"))
        extras_page.bind("<Leave>", lambda x: extras_page.configure(background="gray5"))

        button_separator = tk.Canvas(self.container, background="gray100", width=3, height=40, highlightthickness=0)
        button_separator.place(x=400, y=48, anchor="center")

        under_line = tk.Canvas(self.container, background="gray100", width=200, height=3, highlightthickness=0)
        under_line.place(x=200, y=70, anchor="center")

        menu_frame.place(x=self.container.winfo_width() / 2, y=48, anchor="center")

    def transmitterPage(self):
        page_frame = tk.Frame(self.container, width=800, height=520, bg="gray5")

        pair_button = ct.CTkButton(page_frame, text="Pair", bg_color="gray5", fg_color="gray2", hover_color="gray8", text_color="gray100", width=200, height=60, font=("Ariel", 30), corner_radius=10, border_width=3, border_color="#00ff00")#, command=lambda: threading.Thread(target=self.client.acquireAddress).start())
        pair_button.place(x=125, y=40, anchor="center")
        CreateToolTip(pair_button, "Using the receivers public IP address you may pair to them and than send files over", 2000)

        pair_entry = ct.CTkEntry(page_frame, text_color="gray100", corner_radius=10, fg_color="gray2", bg_color="gray5", placeholder_text_color="gray100", placeholder_text="XXX.XXX.XXX.XXX", height=60, width=525, border_color="gray10", justify="center", font=("Ariel", 30))
        pair_entry.place(x=515, y=40, anchor="center")

        choose_file_button = ct.CTkButton(page_frame, text="Choose File", bg_color="gray5", fg_color="gray2", hover_color="gray8", text_color="gray100", width=200, height=60, font=("Ariel", 30), corner_radius=10, border_width=2, border_color="#ff0000", command=lambda: self.throwLog("WARNING", "You have yet to pair"))
        choose_file_button.place(x=125, y=160, anchor="center")
        CreateToolTip(choose_file_button,"Choose a file and file name to send over once paired",2000)

        file_path_entry = ct.CTkEntry(page_frame, text_color="gray100", corner_radius=10, fg_color="gray2", bg_color="gray5", placeholder_text_color="gray100", placeholder_text="", height=60, width=525, border_color="gray10", justify="center", font=("Ariel", 30))
        file_path_entry.place(x=515, y=120, anchor="center")

        file_name_entry = ct.CTkEntry(page_frame, text_color="gray100", corner_radius=10, fg_color="gray2", bg_color="gray5", placeholder_text_color="gray100", placeholder_text="", height=60, width=525, border_color="gray10", justify="center", font=("Ariel", 30))
        file_name_entry.place(x=515, y=200, anchor="center")

        name_label = ct.CTkLabel(page_frame, text_color="gray100", bg_color="gray5", text="File Directory:", font=("Ariel", 20), wraplength=515)
        name_label.place(x=250, y=115, anchor="e")

        directory_label = ct.CTkLabel(page_frame, text_color="gray100", bg_color="gray5", text="File Name:", font=("Ariel", 20), wraplength=515)
        directory_label.place(x=250, y=205, anchor="e")

        send_button = ct.CTkButton(page_frame, text="Send File Over", bg_color="gray5", fg_color="gray2", hover_color="gray8", text_color="gray100", width=755, height=60, font=("Ariel", 30), corner_radius=10, border_width=3, border_color="#ff0000", command=lambda: self.throwLog("WARNING", "You have yet to pair"))
        send_button.place(x=self.container.winfo_width()/2, y=280, anchor="center")

        username_entry_label = ct.CTkLabel(page_frame, text_color="gray100", bg_color="gray5", text="Username:", font=("Ariel", 30))
        username_entry_label.place(x=380, y=375, anchor="center")

        username_entry = ct.CTkEntry(page_frame, width=250, height=50, fg_color="gray2", bg_color="gray5", corner_radius=10, text_color="gray100", font=("Ariel", 25), placeholder_text="GUEST", placeholder_text_color="gray100", justify="center")
        username_entry.place(x=380, y=430, anchor="center")

        auto_accept_label = ct.CTkLabel(page_frame, text_color="gray100", bg_color="gray5", text="Auto Accept Files:", font=("Ariel", 30))
        auto_accept_label.place(x=150, y=350, anchor="center")

        use_at_own_risk_label = ct.CTkLabel(page_frame, text_color="gray30", bg_color="gray5", text="USE AT YOUR OWN RISK!", font=("Ariel", 15))
        use_at_own_risk_label.place(x=150, y=385, anchor="center")

        auto_accept_switch = ct.CTkSwitch(page_frame, width=100, height=40, switch_width=100, switch_height=40, fg_color="gray2", bg_color="gray5", corner_radius=100, border_width=0, text="", progress_color="gray10", button_color="gray80", button_hover_color="gray100")
        auto_accept_switch.place(x=150, y=430, anchor="center")
        CreateToolTip(auto_accept_switch, f"Auto accept anyone trying to pair with you\n\n{"!!!USE AT YOUR OWN RISK!!!": ^50}",1000)

        page_frame.place(x=self.container.winfo_width() / 2, y=self.container.winfo_height() / 2 + 60, anchor="center")

        return page_frame, pair_button, pair_entry, choose_file_button, file_path_entry, file_name_entry, send_button, username_entry, auto_accept_switch

    def consolePage(self):
        page_frame = tk.Frame(self.container, width=800, height=520, bg="gray5")

        console = ct.CTkTextbox(page_frame, width=560, height=480, font=("Arial", 15, "bold"), state="disabled", corner_radius=10)
        console._textbox.configure(wrap=tk.WORD)
        console.place(x=500, y=self.container.winfo_height() / 2 - 60, anchor="center")

        sending_file_name_label = ct.CTkLabel(page_frame, text_color="gray100", bg_color="gray5", text="", font=("Ariel", 12), wraplength=200)
        sending_file_name_label.place(x=110, y=120, anchor="center")

        sending_progress_bar = ttk.Progressbar(page_frame, style="sending.Horizontal.TProgressbar", length=200, value=0, maximum=100, mode="determinate")
        sending_progress_bar.place(x=110, y=150, anchor="center")

        sending_label = ct.CTkLabel(page_frame, text_color="gray100", bg_color="gray5", text="Sending\nName:", font=("Ariel", 15))
        sending_label.place(x=110, y=60, anchor="center")

        receiving_file_name_label = ct.CTkLabel(page_frame, text_color="gray100", bg_color="gray5", text="", font=("Ariel", 12), wraplength=200)
        receiving_file_name_label.place(x=110, y=320, anchor="center")

        receiving_progress_bar = ttk.Progressbar(page_frame, style="receiving.Horizontal.TProgressbar", length=200, value=0, maximum=1000, mode="determinate")
        receiving_progress_bar.place(x=110, y=350, anchor="center")

        receiving_label = ct.CTkLabel(page_frame, text_color="gray100", bg_color="gray5", text="Receiving\nName:", font=("Ariel", 15))
        receiving_label.place(x=110, y=260, anchor="center")

        page_frame.place(x=1200, y=self.container.winfo_height() / 2 + 60, anchor="center")

        return page_frame, console, sending_progress_bar, receiving_progress_bar, sending_file_name_label, receiving_file_name_label

    def throwLog(self, error_type: str, text: str):
        allowed_types = ["ERROR", "WARNING", "INFO"]
        error_type_icon = None
        if error_type not in allowed_types:
            error_type = "INFO"
        if error_type == "ERROR":
            error_type_icon = "⛔"
        elif error_type == "WARNING":
            error_type_icon = "⚠︎"
        elif error_type == "INFO":
            error_type_icon = "✔"
        self.console.configure(state="normal")
        self.console.insert("end", f"[{time.strftime('%H:%M:%S')}] {error_type_icon} {text}\n")
        self.console.tag_add(f"log{self.line_colour}", index1=f"{(float(self.console.index("end")) - 2 + 0.1):.2f}", index2=f"{float(self.console.index("end")) - 1}")
        if error_type == "ERROR":
            self.console.tag_config(f"log{self.line_colour}", foreground="#ff0000")
        elif error_type == "WARNING":
            self.console.tag_config(f"log{self.line_colour}", foreground="#ffb400")
        elif error_type == "INFO":
            self.console.tag_config(f"log{self.line_colour}", foreground="#00ff00")
        self.line_colour+=1
        self.console.configure(state="disabled")

    def changeButtonColour(self, state: bool):
        if state is False:
            self.send_button.configure(border_color="#ff0000")
            self.choose_file_button.configure(border_color="#ff0000")
        elif state is True:
            self.send_button.configure(border_color="#00ff00")
            self.choose_file_button.configure(border_color="#00ff00")
        elif state is None:
            self.configurePairButton(None)
            self.send_button.configure(border_color="#ff0000")
            self.choose_file_button.configure(border_color="#ff0000")

    def configurePairButton(self, state: bool):
        if state is True:
            self.pair_button.configure(text="Pair", border_color="#00ff00")#, command=lambda: threading.Thread(target=self.client.acquireAddress).start())
        if state is False:
            self.pair_button.configure(text="Unpair", border_color="#ff0000")#, command=lambda: threading.Thread(target=self.client.disconnect).start())
        if state is None:
            self.pair_button.configure(text="Pairing", border_color="#00b1ff")#, command=lambda: threading.Thread(target=self.client.disconnect).start())

    def configureSendButton(self, state: bool):
        def chooseFile():
            def pickFile():
                filepath = '{}'.format(
                    askopenfilename(title='Choose a file to Upload',
                                    initialdir=f"{os.environ['USERPROFILE']}\\Desktop"),
                    filetypes=[("all files", "*.*")])
                if filepath == "":
                    return "", ""
                filename = filepath.rsplit('/', 1)[-1]
                return filepath, filename

            if self.client.acceptance is True:
                try:
                    file_path, file_name = pickFile()
                    if file_path != "" and file_name != "":
                        self.file_name_entry.delete(0, "end")
                        self.file_path_entry.delete(0, "end")
                        self.file_name_entry.insert(0, f"{file_name}")
                        self.file_path_entry.insert(0, f"{file_path}")
                except TypeError:
                    pass

            else:
                self.throwLog("WARNING", "You have yet to connect")

        if state is True:
            self.send_button.configure(border_color="#00ff00")#, command=lambda: threading.Thread(target=self.client.sendFileOverChecks).start())
            self.choose_file_button.configure(border_color="#00ff00", command=chooseFile)
        if state is False:
            self.send_button.configure(border_color="#ff0000", command=lambda: self.throwLog("WARNING", "You have yet to pair"))
            self.choose_file_button.configure(border_color="#ff0000", command=lambda: self.throwLog("WARNING", "You have yet to pair"))
        if state is None:
            self.send_button.configure(border_color="#ff0000", command=lambda: self.throwLog("WARNING", "File sending already in progress"))
            self.choose_file_button.configure(border_color="#00ff00", command=chooseFile)

    def displayAcceptanceInfo(self, username: str, state: bool):
        display_acceptance_frame = tk.Frame(self.transmitter_page_frame, width=250, height=150, bg="gray10")

        username_text = ct.CTkLabel(display_acceptance_frame, text=f"{username}", text_color="gray100", bg_color="gray10", font=("Ariel", 20, "bold"))
        username_text.place(x=125, y=25, anchor="center")

        info_label = ct.CTkLabel(display_acceptance_frame, text=f"wants to send files over", text_color="gray50", bg_color="gray10", font=("Ariel", 15))
        info_label.place(x=125, y=60, anchor="center")

        accept_button = ct.CTkButton(display_acceptance_frame, text="Accept", bg_color="gray10", fg_color="gray2", hover_color="gray8", text_color="gray100", width=100, height=40, font=("Ariel", 18), corner_radius=10, border_width=0)#, command=lambda: threading.Thread(target=self.server.decisionConfirmation, args=[True]).start() == display_acceptance_frame.place_forget())
        accept_button.place(x=65, y=110, anchor="center")

        decline_button = ct.CTkButton(display_acceptance_frame, text="Decline", bg_color="gray10", fg_color="gray2", hover_color="gray8", text_color="gray100", width=100, height=40, font=("Ariel", 18), corner_radius=10, border_width=0)#, command=lambda: threading.Thread(target=self.server.decisionConfirmation, args=[False]).start() == display_acceptance_frame.place_forget())
        decline_button.place(x=185, y=110, anchor="center")

        if state is True:
            try:
                self.display_acceptance_frame.place_forget()
            except AttributeError:
                pass
            display_acceptance_frame.place(x=652, y=405, anchor="center")
        elif state is False:
            try:
                self.display_acceptance_frame.place_forget()
            except AttributeError:
                pass

        return display_acceptance_frame
    
    def changeProgressbar(self, witch_one: str, reset: bool, data: bytes, file_size: int):
        len_data = len(data)
        percentage = len_data/file_size * 100
        if witch_one == "sending":
            if reset is True:
                self.sending_progress_bar.configure(maximum=100, value=0)
                self.style.configure("sending.Horizontal.TProgressbar", text="0%")
                self.changeNameLabel("sending", "")
                self.sending_percentage = 0
                return
            self.sending_progress_bar.step(len_data)
            self.sending_percentage += percentage
            self.style.configure("sending.Horizontal.TProgressbar", text=f"{round(self.sending_percentage)}%")
        if witch_one == "receiving":
            if reset is True:
                self.receiving_progress_bar.configure(maximum=100, value=0)
                self.style.configure("receiving.Horizontal.TProgressbar", text="0%")
                self.changeNameLabel("receiving", "")
                self.receiving_percentage = 0
                return
            self.receiving_progress_bar.step(len_data)
            self.receiving_percentage += percentage
            self.style.configure("receiving.Horizontal.TProgressbar", text=f"{round(self.receiving_percentage)}%")

    def changeNameLabel(self, witch_one: str, name: str):
        if witch_one == "sending":
            self.sending_file_name_label.configure(text=f"{name}")
        if witch_one == "receiving":
            self.receiving_file_name_label.configure(text=f"{name}")