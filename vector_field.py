"""
Abstract vector field in 2D.
"""
import numpy as np
from animation import Animation
from matplotlib.pyplot import text, grid
from typing import List


class BaseVectorField2D(Animation):
    """
    Abstract VectorField2D class.
    """

    def __init__(self, bounds: List[int]) -> None:
        """
        Initializer for the BaseVectorField2D class.
        """

        super().__init__(1)

        # Attributes are defined in the methods.
        self.set_coords(*bounds)
        self.set_values()
        self.set_plotting_objects()
        self.place_widgets()
        self.plot_vector_field(init_call=True)

    def f(self, xy, *t) -> None:
        """
        Abstract function that dictates the ODE.
        """
        raise NotImplementedError

    def set_coords(self, xmin: float = -10.0, xmax: float = 10.0,
                   ymin: float = -10.0, ymax: float = 10.0) -> None:
        """
        Set the coordinates for the vector field.
        """

        # Number of points for each axis
        N = 21

        # Dimensions of the plot
        self.bounds = np.array([xmin, xmax, ymin, ymax])

        x = np.outer(np.ones([N]),
                     np.linspace(self.bounds[0], self.bounds[1], N))
        y = np.outer(np.linspace(self.bounds[2], self.bounds[3], N),
                     np.ones([N]))

        self.xy = [x, y]

    def set_values(self) -> None:
        """
        """
        raise NotImplementedError

    def set_title(self) -> None:
        """
        Abstract method to set the title of the plot.
        """
        raise NotImplementedError

    def set_plotting_objects(self) -> None:
        """
        Setup the plotting objects.
        """
        # Initialize plotting objects
        # Create a subplot
        self.ax = self.figure.add_subplot(1, 1, 1)
        self.ax.set_xlim(self.bounds[0], self.bounds[1])
        self.ax.set_ylim(self.bounds[2], self.bounds[3])
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_aspect("equal")
        self.text = text(self.bounds[0] + 1, self.bounds[3] - 1,
                         "", color="black")
        self.text.set_bbox({"facecolor": "white", "alpha": 1.0})
        self.title = text(self.bounds[0]/2 + self.bounds[1]/3,
                          self.bounds[3] 
                          - 0.1*(self.bounds[3] - self.bounds[2]),
                         "", color="black")
        self.title.set_bbox({"facecolor": "white", "alpha": 1.0})
        grid()

    def plot_trajectories(self, init_call: bool = False) -> None:
        """
        Absrtact method to plot trajectories.
        """
        raise NotImplementedError

    def plot_vector_field(self, init_call: bool = False) -> None:
        """
        Plot the vector field.
        """
        xdot, ydot = self.f(self.xy)
        if init_call:
            self.line = self.ax.quiver(self.xy[0], self.xy[1],
                                       xdot, ydot, color="black")

        else:
            self.line.set_UVC(xdot, ydot)
        self.plot_trajectories(init_call=init_call)
        self.set_title()
        
    def update(self):
        """
        Update the animation
        """
        pass
        # self.plot_vector_field(init_call = False)
