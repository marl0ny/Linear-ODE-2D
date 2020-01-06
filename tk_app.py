"""
This is the tkinter gui
"""
from locate_mouse import locate_mouse
import tkinter as tk
from linear_vector_field import LinearVectorField2D
from matplotlib.backends import backend_tkagg


class App(LinearVectorField2D):
    """
    Main app.
    
    Attributes:
    window [tk.Tk]: Main tkinter gui window
    canvas [backend_tkagg.FigureCanvasTkAgg]: Canvas to graph on
    sliderslist [List[tk.Scale]]: List of tkinter sliders
    quit_button [tk.Button]: The quit button
    """
    
    def __init__(self) -> None:
        """
        This is the constructor.
        """

        #Initialize the parent class
        LinearVectorField2D.__init__(self)

        # Tkinter GUI Objects
        self.window = None
        self.canvas = None
        self.sliderslist = []
        self.quit_button = None

        self.place_widgets()


    def slider_update(self, event: tk.Event) -> None:
        """
        Respond to slider events from the slider widgets.
        """

        tmplist = []
        for i in range(len(self.sliderslist)):
            tmplist.append(self.sliderslist[i].get())

        self.set_matrix(*tuple(tmplist))
        self.plot_vector_field()

    def mouse_listener(self, event: tk.Event) -> None:
        """
        Handle mouse input.
        """
        ax = self.figure.get_axes()[0]
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        pixel_xlim = [ax.bbox.xmin, ax.bbox.xmax]
        pixel_ylim = [ax.bbox.ymin, ax.bbox.ymax]
        height = self.canvas.get_tk_widget().winfo_height()
        mx = (xlim[1] - xlim[0])/(pixel_xlim[1] - pixel_xlim[0])
        my = (ylim[1] - ylim[0])/(pixel_ylim[1] - pixel_ylim[0])
        x = (event.x - pixel_xlim[0])*mx + xlim[0]
        y = (height - event.y - pixel_ylim[0])*my + ylim[0]
        self.set_interactive_line(x, y)

    def place_widgets(self) -> None:
        """
        Add tkinter gui widgets.
        """

        # Primary Tkinter GUI
        self.window = tk.Tk()
        self.window.title("Linear Vector Field in 2D")
        self.window.configure()

        # Canvas
        # A short example of how to integrate a Matplotlib animation into a
        # Tkinter GUI is given here:
        # https://stackoverflow.com/a/21198403
        # [Answer by HYRY: https://stackoverflow.com/users/772649/hyry]
        # Link to question: https://stackoverflow.com/q/21197728
        # [Question by user3208454:
        # https://stackoverflow.com/users/3208454/user3208454]
        self.canvas = backend_tkagg.FigureCanvasTkAgg(
            self.figure,
            master=self.window
        )
        maxrowspan = 15
        self.canvas.get_tk_widget().grid(
                row=0, column=0, rowspan=maxrowspan, columnspan=3)
        self._canvas_height = self.canvas.get_tk_widget().winfo_height()
        self.canvas.get_tk_widget().bind("<B1-Motion>", self.mouse_listener)

        # Quit button
        self.quit_button = tk.Button(
                self.window, text='QUIT', command=self.quit)
        self.quit_button.grid(row=maxrowspan - 1, column=4, pady=(10, 10))

        # Sliders
        rnge = 10.0
        self.sliderslist = []
        for i, char in enumerate(('a', 'b', 'c', 'd')):
            self.sliderslist.append(tk.Scale(self.window,
                                             label="change " + char + ":",
                                             from_=-rnge, to=rnge,
                                             resolution=0.01,
                                             orient=tk.HORIZONTAL,
                                             length=200,
                                             command=self.slider_update))
            self.sliderslist[i].grid(row=i + 1, column=4,
                                     padx=(10, 10), pady=(0, 0))
        self.sliderslist[0].set(-0.5)
        self.sliderslist[1].set(-1.5)
        self.sliderslist[2].set(1.5)
        self.sliderslist[3].set(-0.5)

        # Thanks to stackoverflow user rudivonstaden for
        # giving a way to get the colour of the tkinter widgets:
        # https://stackoverflow.com/questions/11340765/
        # default-window-colour-tkinter-and-hex-colour-codes
        #
        #     https://stackoverflow.com/q/11340765
        #     [Question by user user2063:
        #      https://stackoverflow.com/users/982297/user2063]
        #
        #     https://stackoverflow.com/a/11342481
        #     [Answer by user rudivonstaden:
        #      https://stackoverflow.com/users/1453643/rudivonstaden]
        #
        colour = self.window.cget('bg')
        if colour == 'SystemButtonFace':
            colour = "#F0F0F0"
        # Thanks to stackoverflow user user1764386 for
        # giving a way to change the background colour of a plot.
        #
        #    https://stackoverflow.com/q/14088687
        #    [Question by user user1764386:
        #     https://stackoverflow.com/users/1764386/user1764386]
        #
        self.figure.patch.set_facecolor(colour)

    def quit(self, *event: tk.Event) -> None:
        """
        Quit the application.
        """
        self.window.quit()
        self.window.destroy()


if __name__ == "__main__":
    app = App()
    app.animation_loop()
    tk.mainloop()
