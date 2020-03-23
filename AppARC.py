import tkinter as tk
import threading
import tkinter.font as tkFont
import gc
from PIL import ImageTk, Image
from tkinter import messagebox
from time import sleep


class AppARC(threading.Thread):

    bg_color = 'antique white'
    font_size = -24

    def __init__(self):
        threading.Thread.__init__(self)
        self.__stop = threading.Event()
        self.fullscreen = False
        self.is_trike_started = False
        self.is_auto_mode = False
        self.root = None
        self.main_frame = None
        self.loading_frame = None
        self.font_title = None
        self.font_txt = None
        self.btn_toggle_fullscreen = None
        self.btn_quit = None
        self.btn_start = None
        self.btn_end = None
        self.btn_toggle_mode = None
        self.canvas = None
        self.image = None

    def start_trip(self):
        """ Set a flag to start the trike.

        """
        self.is_trike_started = True
        self.btn_start.configure(state='disabled', bg=AppARC.bg_color)
        self.btn_end.configure(state='active', bg='pale green')

    def end_trip(self):
        """ Set a flag to stop the trike.

        """
        self.is_trike_started = False
        self.btn_end.configure(state='disabled', bg=AppARC.bg_color)
        self.btn_start.configure(state='active', bg='pale green')

    def toggle_mode(self, set_auto_mode = None):
        """ Set a flag to toggle the mode.
            If optional parameter set_auto_mode is not specified - toggle mode
            If set_auto_mode is specified - set the mode accordingly
                --set_auto_mode = True => change to auto mode
                --set_auto_moe = False => change to manual mode

        """
        if set_auto_mode is not None:
            self.is_auto_mode = set_auto_mode
        else:
            self.is_auto_mode = not self.is_auto_mode

        if self.is_auto_mode:
            self.btn_toggle_mode.configure(text='Switch to Manual Mode')
        else:
            self.btn_toggle_mode.configure(text='Switch to Auto Mode')

    def toggle_fullscreen(self, event=None):
        """ Toggle between fullscreen and windowed modes.

        """
        if self.fullscreen:
            self.btn_toggle_fullscreen.configure(text='Fullscreen')
        else:
            self.btn_toggle_fullscreen.configure(text='Exit Fullscreen')

        self.fullscreen = not self.fullscreen
        self.root.attributes('-fullscreen', self.fullscreen)
        self.resize()

    def end_fullscreen(self, event=None):
        """ End fullscreen mode and return to windowed mode.

        """
        self.fullscreen = False
        self.btn_toggle_fullscreen.configure(text='Fullscreen')
        self.root.attributes('-fullscreen', False)
        self.resize()

    def resize(self, event=None):
        """ Resize font size based on frame height.

        """
        # Minimum font size = 12
        new_size = -max(12, int((self.main_frame.winfo_width() / 50)))
        self.font_txt.configure(size=new_size)
        new_size = -max(12, int((self.main_frame.winfo_height() / 20)))
        self.font_title.configure(size=new_size)

    def config_loading_frame(self):
        """ Configure and draw the widgets for the loading frame

        """
        txt_loading = tk.StringVar()
        txt_loading.set('Loading ARC...\n\nPlease wait')

        # Widgets
        lbl_loading = tk.Label(self.loading_frame,
                               textvariable=txt_loading,
                               font=self.font_txt,
                               fg='black',
                               bg=AppARC.bg_color,
                               justify=tk.CENTER)

        # Lay out widgets in a grid in the frame
        lbl_loading.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        # Make it so that the grid cells expand out to fill window
        self.loading_frame.rowconfigure(0, weight=1)
        self.loading_frame.columnconfigure(0, weight=1)

    def config_main_frame(self):
        """ Configure and draw the widgets for the main frame

        """
        # Instruction string
        txt_instructions = tk.StringVar()
        txt_instructions.set("""INSTRUCTIONS\n
(1) Use the brake levers to stop the trike
        and take manual control at any time.
(2) While in manual mode, you may use
        the thumb joysticks to steer the trike.
(3) Press the emergency stop button to
        turn off power and stop the trike.""")

        # Widgets
        lbl_instructions = tk.Label(self.main_frame,
                                    textvariable=txt_instructions,
                                    font=self.font_txt,
                                    fg='black',
                                    bg=AppARC.bg_color,
                                    justify=tk.LEFT)

        lbl_title = tk.Label(self.main_frame,
                             text='ARC',
                             font=self.font_title,
                             fg='black',
                             bg=AppARC.bg_color,
                             justify=tk.CENTER)

        self.btn_toggle_fullscreen = tk.Button(self.main_frame,
                                               text='Exit Fullscreen',
                                               font=self.font_txt,
                                               command=self.toggle_fullscreen,
                                               borderwidth=3,
                                               relief=tk.GROOVE,
                                               highlightthickness=0,
                                               fg='black',
                                               bg=AppARC.bg_color,
                                               activebackground=AppARC.bg_color)

        self.btn_quit = tk.Button(self.main_frame,
                                  text='Quit',
                                  font=self.font_txt,
                                  command=self.deinit,
                                  borderwidth=3,
                                  relief=tk.GROOVE,
                                  highlightthickness=0,
                                  fg='black',
                                  bg=AppARC.bg_color,
                                  activebackground=AppARC.bg_color)

        self.btn_start = tk.Button(self.main_frame,
                                   text='Start Trip',
                                   font=self.font_txt,
                                   command=self.start_trip,
                                   borderwidth=2,
                                   relief=tk.SOLID,
                                   highlightthickness=0,
                                   fg='black',
                                   bg='pale green',
                                   activebackground='pale green')

        self.btn_end = tk.Button(self.main_frame,
                                 text='End Trip',
                                 font=self.font_txt,
                                 command=self.end_trip,
                                 borderwidth=2,
                                 relief=tk.SOLID,
                                 highlightthickness=0,
                                 fg='black',
                                 bg=AppARC.bg_color,
                                 activebackground='pale green',
                                 state='disabled')

        self.btn_toggle_mode = tk.Button(self.main_frame,
                                         text='Switch to Auto Mode',
                                         font=self.font_txt,
                                         command=self.toggle_mode,
                                         borderwidth=2,
                                         relief=tk.SOLID,
                                         highlightthickness=0,
                                         fg='black',
                                         bg='light sky blue',
                                         activebackground='light sky blue')

        self.canvas = tk.Canvas(self.main_frame)

        # Lay out widgets in a grid in the frame
        lbl_title.grid(row=0, column=0, padx=10, pady=10, sticky='ew', columnspan=2)
        self.btn_start.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        self.btn_end.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        self.btn_toggle_mode.grid(row=2, column=0, padx=10, pady=10, sticky='ew', columnspan=2)
        lbl_instructions.grid(row=3, column=0, padx=10, pady=10, columnspan=1, sticky='w')
        self.canvas.grid(row=3, column=1, padx=10, pady=10, sticky='nsew')
        self.btn_toggle_fullscreen.grid(row=4, column=1, padx=10, pady=10, sticky=tk.E)
        self.btn_quit.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)

        # Make it so that the grid cells expand out to fill window
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
        self.main_frame.rowconfigure(3, weight=6)
        self.main_frame.rowconfigure(4, weight=1)
        self.main_frame.columnconfigure(0, uniform='half', weight=1)
        self.main_frame.columnconfigure(1, uniform='half', weight=1)

    def deinit(self):
        confirm_quit = messagebox.askyesno("Exit ARC", "Are you sure you want to quit?")
        if confirm_quit:
            self.__stop.set()
            self.root.destroy()
            # Setting all the tk objects to None and forcing a garbage
            # collect is necessary to avoid a TclAsync threading error
            self.root = None
            self.main_frame = None
            self.loading_frame = None
            self.font_title = None
            self.font_txt = None
            self.btn_toggle_fullscreen = None
            self.btn_quit = None
            self.btn_start = None
            self.btn_end = None
            self.btn_toggle_mode = None
            self.canvas = None
            gc.collect()

    def raise_main_frame(self):
        self.main_frame.tkraise()

    def display_speed(self, speed_kmph):
        pass

    def show_yesno_prompt(self, title, message):
        response = messagebox.askyesno(title, message)
        return response
    
    def show_info_prompt(self, title, message):
        messagebox.showinfo(title, message)

    def run(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title('ARC')

        # Create and lay out the main container (expand to fit window)
        container = tk.Frame(self.root, bg=AppARC.bg_color)
        container.pack(fill=tk.BOTH, expand=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create the main and loading frames
        self.main_frame = tk.Frame(container, bg=AppARC.bg_color)
        self.loading_frame = tk.Frame(container, bg=AppARC.bg_color)
        self.loading_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Create dynamic font for text
        self.font_txt = tkFont.Font(family='Verdana', size=AppARC.font_size)
        self.font_title = tkFont.Font(family='Verdana', size=AppARC.font_size, weight='bold')

        # Configure widgets
        self.config_main_frame()
        self.config_loading_frame()

        # Bind ESC to end fullscreen
        self.root.bind('<Escape>', self.end_fullscreen)

        # Call resize() when window is resized
        self.root.bind('<Configure>', self.resize)

        # De-initialize when window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.deinit)

        # Start in fullscreen mode, with the loading_frame and run
        self.toggle_fullscreen()
        self.loading_frame.tkraise()
        self.root.mainloop()

    def display_image(self, file_path):
        self.canvas.delete('all')
        img = Image.open(file_path)
        img = img.resize((self.canvas.winfo_width(), self.canvas.winfo_height()), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(img)
        self.canvas.image = self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.image, state='normal')


if __name__ == '__main__':
    newApp = AppARC()
    newApp.start()

    # Loading screen timer - for testing
    i = 0
    while i < 200000:
        print(i)
        i += 1

    # Call newApp.raise_main_frame() when loading is complete
    newApp.raise_main_frame()

    # Test if UI thread is responsive while counter increments and prints
    i = 0
    while i < 200000:
        print(i)
        i += 1

    # display images
    newApp.display_image(r'/home/pi/Pictures/trike1.png')
    sleep(5)
    newApp.display_image(r'/home/pi/Pictures/trike2.png')
    
    response = newApp.show_yesno_prompt('Testing', 'Obstacle detected. Would you like to switch to manual mode?')
    if response:
        newApp.toggle_mode(False) #toggle to manual mode
    sleep(5)
    newApp.show_info_prompt('Testing', 'Completed Testing prompts')

    
