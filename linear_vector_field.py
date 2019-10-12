"""
Linear homogeneous vector field in 2D.
"""
import numpy as np
import tkinter as tk
from locate_mouse import locate_mouse
from matplotlib.backends import backend_tkagg
from vector_field import BaseVectorField2D


class LinearVectorField2D(BaseVectorField2D):
    """
    Linear Vector Field 2D class.

    Reference:
    Strogatz, S. (2015). Linear Systems.
    In Nonlinear Dynamics and Chaos,
    With Applications to Physics, Chemistry, and Engineering,
    chapter 5. Routledge.
    """
    def __init__(self) -> None:
        """
        Initializer.

        Attributes:
        window [tk.Tk]: Main tkinter gui window
        canvas [backend_tkagg.FigureCanvasTkAgg]: Canvas to graph on
        sliderslist [List[tk.Scale]]: List of tkinter sliders
        quit_button [tk.Button]: The quit button
        m [np.ndarray]: ODE matrix
        eivals [np.ndarray]: Eigenvalues of m
        eigvects [np.ndarray]: Eigenvectors of m
        lines [List[Line2D]]: List of Line2D
        interactive_line [Line2D]: Line2D object that can be mutated
                                   from mouse input.
        interactive_line_coeffs [Tuple[float, float]]:
            IC for interactive_line
        """

        # Tkinter GUI Objects
        self.window = None
        self.canvas = None
        self.sliderslist = []
        self.quit_button = None

        # Numpy objects for computations
        self.m = np.array([[0.0, 0.0], [0.0, 0.0]])
        self.eigvals = np.array([0.0, 0.0])
        self.eigvects = np.array([[0.0, 0.0], [0.0, 0.0]])
        self._t = np.linspace(-4.0, 4.0, 200, np.float64)

        # Matplotlib graphing objects
        self.lines = []
        self.interactive_line = None
        self.interactive_line_coeffs = 0.0, 0.0

        try:
            arr = np.loadtxt("./resources/linear_vector_field_constants.txt")
            arr = arr.T
            bounds = list(arr[0:4])
            self._axes_location = list(arr[4:10])
        except FileNotFoundError:
            bounds = [-10.0, 10.0, -10.0, 10.0]
            self._axes_location = [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0]
        except IndexError:
            bounds = [-10.0, 10.0, -10.0, 10.0]
            self._axes_location = [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0]
        BaseVectorField2D.__init__(self, bounds)

    def set_values(self) -> None:
        """
        Set the values used.
        """
        self.set_matrix()

    def f(self, xy: np.ndarray, *t: float) -> None:

        # v is (dx/dt, dy/dt)
        v = [self.m[0][0]*xy[0] + self.m[0][1]*xy[1],
             self.m[1][0]*xy[0] + self.m[1][1]*xy[1]]

        return v if (type(xy) == list) else np.array(v)

    def classify_fixed_point(self) -> str:
        """
        Determine the nature fixed points.
        The complete classification of fixed points can be
        found on page 133 of Strogatz.
        """
        # TODO: refactor the if statements.
        fptype = ""
        if np.linalg.det(self.m) == 0.0:
            fptype = "Non-isolated"
        elif self.m[0][0] == self.m[1][1] and (
            self.m[1][0] == 0.0 or self.m[0][1] == 0.0):
            if self.m[1][0] == self.m[0][1] == 0.0:
                fptype = "Star"
            elif (self.m[1][0] == 0.0 and self.m[0][1] != 0.0) or (
                self.m[1][0] != 0.0 and self.m[0][1] == 0.0):
                fptype = "Degernate Node"
        else:
            w = self.eigvals
            if np.abs(np.imag(w[0])) < 1e-30:
                if np.real(w[0]) > 0 and np.real(w[1]) < 0:
                    fptype = "Saddle Node"
                elif np.real(w[0]) < 0 and np.real(w[1]) > 0:
                    fptype = "Saddle Node"
                elif np.real(w[0]) > 0 and np.real(w[1]) > 0:
                    fptype = "Unstable Node"
                elif np.real(w[0]) < 0 and np.real(w[1]) < 0:
                    fptype = "Stable Node"
                else:
                    fptype = ""
            elif np.abs(np.imag(w[0])) > 1e-130:
                if np.abs(np.real(w[0])) < 1e-10 and \
                   np.abs((np.real(w[1])) < 1e-10):
                    fptype = "Centre"
                elif np.real(w[0]) > 0 and np.real(w[1]) > 0:
                    fptype = "Unstable Spiral"
                elif np.real(w[0]) < 0 and np.real(w[1]) < 0:
                    fptype = "Stable Spiral"
                else:
                    fptype = ""
        return fptype

    def set_title(self) -> None:
        """
        Set the title
        """

        m00 = np.float(np.round(self.m[0][0], 2))
        m01 = np.float(np.round(self.m[0][1], 2))
        xstring = str(m00) + "x" if np.abs(m00) > 1e-30 else ""
        xstring += "+" if (m01 > 1e-30 and np.abs(m00) > 1e-30) else ""
        xstring += str(m01) + "y" if np.abs(m01) > 1e-30 else ""
        if xstring == "":
            xstring = "0"
        # if ("1x" in xstring): xstring = xstring.replace("1x","x")
        # if ("1y" in xstring): xstring = xstring.replace("1x","x")

        m10 = np.float(np.round(self.m[1][0], 2))
        m11 = np.float(np.round(self.m[1][1], 2))
        ystring = str(m10) + "x" if np.abs(m10) > 1e-30 else ""
        ystring += "+" if (m11 > 1e-30 and np.abs(m10) > 1e-30) else ""
        ystring += str(m11) + "y" if np.abs(m11) > 1e-30 else ""
        if ystring == "":
            ystring = "0"
        # if "1" in ystring: ystring = ystring.replace("1","")

        # Latex rendering is slow, so we completely avoid it.
        self.title.set_text(r"x' = ax+by = " + xstring + " \n " +
                            r"y' = cx+dy = " + ystring)
        fptype = self.classify_fixed_point()
        self.text.set_text(fptype)

    def _plot_trajectory(self, x: list, y: list, a: float, b: float) -> None:
        """
        Helper function for plot_trajectories. This plots a single trajectory.
        """
        t = np.linspace(-4, 4, 200)
        x_elem = a*self.eigvects[0][0]*np.exp(
                self.eigvals[0]*t) + b*self.eigvects[0][1]*np.exp(
                        self.eigvals[1]*t)
        y_elem = a*self.eigvects[1][0]*np.exp(
                self.eigvals[0]*t) + b*self.eigvects[1][1]*np.exp(
                        self.eigvals[1]*t)
        x.append(np.real(x_elem))
        y.append(np.real(y_elem))

    def plot_trajectories(self, init_call: bool = False) -> None:
        """
        Plot the trajectories.
        """

        t = np.linspace(-4, 4, 200)
        x = []
        y = []

        # Plot some trajectories
        self._plot_trajectory(x, y, 4.0, 4.0)
        self._plot_trajectory(x, y, 4.0, -4.0)
        self._plot_trajectory(x, y, -4.0, 4.0)
        self._plot_trajectory(x, y, -4.0, -4.0)

        # Plot the eigentrajectories.
        self._plot_trajectory(x, y, 4.0, 0.0)
        self._plot_trajectory(x, y, -0.0, 4.0)
        self._plot_trajectory(x, y, -4.0, 0.0)
        self._plot_trajectory(x, y, 0.0, -4.0)

        if (init_call):

            # Initialize the trajectories
            for i in range(len(x)):
                linewidth = 0.75 if i < 4 else 1.75
                color = "blue" if i < 4 else "black"
                line, = self.ax.plot(x[i], y[i],
                                     # color=(
                                     # i/len(x),0.5,(len(x)-i)/len(x)),
                                     color=color,
                                     linewidth=linewidth)
                self.lines.append(line)

            # Initialize the interactive trajectory
            line, = self.ax.plot(np.array([0]), np.array([0]), color="orange",
                                 linewidth=linewidth)
            self.interactive_line = line

            self.add_plots(self.lines)

        else:
            a, b = self.interactive_line_coeffs
            x_arr = a*self.eigvects[0][0]*np.exp(
                    self.eigvals[0]*t) + b*self.eigvects[0][1]*np.exp(
                            self.eigvals[1]*t)
            y_arr = a*self.eigvects[1][0]*np.exp(
                    self.eigvals[0]*t) + b*self.eigvects[1][1]*np.exp(
                            self.eigvals[1]*t)
            self.interactive_line.set_xdata(np.real(x_arr))
            self.interactive_line.set_ydata(np.real(y_arr))
            for i in range(len(x)):
                self.lines[i].set_xdata(x[i])
                self.lines[i].set_ydata(y[i])

    def set_interactive_line(self, x: float, y: float) -> None:
        """
        Set the initial conditions of the trajectory.
        """
        t = self._t
        t = np.linspace(0.0, 4.0, 200)
        a, b = np.linalg.solve(self.eigvects, np.array([x, y]))
        x_arr = a*self.eigvects[0][0]*np.exp(
          self.eigvals[0]*t) + b*self.eigvects[0][1]*np.exp(
                self.eigvals[1]*t)
        y_arr = a*self.eigvects[1][0]*np.exp(
          self.eigvals[0]*t) + b*self.eigvects[1][1]*np.exp(
                self.eigvals[1]*t)
        self.interactive_line_coeffs = a, b
        self.interactive_line.set_xdata(np.real(x_arr))
        self.interactive_line.set_ydata(np.real(y_arr))

    def set_matrix(self, c1: float = -0.5, c2: float = -1.5,
                   c3: float = 1.5, c4: float = -0.5) -> None:
        """
        Set the matrix attribute m.
        Also compute its eigenvalues and eigenvectors.
        """
        self.m = np.array([[c1, c2], [c3, c4]])
        w, v = np.linalg.eig(self.m)
        self.eigvals = w
        self.eigvects = v

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
    v = LinearVectorField2D()
    v.animation_loop()
    tk.mainloop()
