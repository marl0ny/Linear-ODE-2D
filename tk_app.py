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
        Listen to mouse input on the canvas and then call further
        functions in order to handle this.
        """
        x, y = locate_mouse(event, self.bounds, self._canvas_height,
                            self._axes_location)
        self.set_interactive_line(x, y)

    def place_widgets(self) -> None:
        """
        Add tkinter gui widgets.
        """

        # Primary Tkinter GUI
        self.window = tk.Tk()
        self.window.title("Linear Vector Field in 2D")
        self.window.configure(background="white")

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
