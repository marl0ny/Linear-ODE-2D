"""
Abstract animation class.
"""
import matplotlib.pyplot as plt
# from matplotlib.artist import Artist
from matplotlib.lines import Line2D
from matplotlib.text import Text
from matplotlib.collections import Collection
from matplotlib.quiver import QuiverKey, Quiver
import matplotlib.animation as animation
from .animation_constants import AnimationConstants
from typing import List
from time import perf_counter

artists = [Line2D, Collection, Text, QuiverKey, Quiver]


class Animation(AnimationConstants):
    """
    Abstract animation class that adds a small layer of abstraction
    over the matplotlib animation functions and interfaces.
    
    To use this class:
        -Inherit this in a derived class.
        -The Figure object is already instantiated in this class as the
         attribute self.figure. Create instances of 
         plotting objects from this, such as Line2D. Ensure that all
         all matplotlib objects are set as attributes.
        -either set this class's attribute self.autoaddartists
         to True (in which case plot attributes  will be automatically added,
         except for those inside lists and tuples),
         or add plots individually using the add_plot and
         add_plots method.
        -Update the plots inside the update method, which must be
         overriden.
        -Call the animation_loop method to show the animation.

    Attributes:
    figure [Figure]: Use this to obtain plot elements.
    autoaddartists [bool]: Automatically add plot attributes if True.
    self.delta_t [float]: The time between each frame in seconds of
                          the animation.                
    """

    def __init__(self, autoaddartists: bool = False) -> None:
        """
        Initializer
        """
        AnimationConstants.__init__(self)
        self.autoaddartists = autoaddartists
        self.figure = None
        self._plots = []
        self.figure = plt.figure(
                dpi=self.dots_per_inches)
        self.delta_t = 1.0/60.0
        self._t = perf_counter()
        # TODO: Figure out a better way to do this!
        self.backendiskivy = False

    def make_plots(self) -> None:
        """
        Initialize all plot objects 
        """
        # Create a subplot
        # self.ax = self.figure.add_subplot(1, 1, 1)

        # Set axis labels
        # self.ax.set_xlabel("x")
        # self.ax.set_ylabel("y")

        # Set dimensions of plot
        # self.ax.set_xlim(-10, 10)
        # self.ax.set_ylim(-10, 10)

        # Create a Line2D instance
        # line, = self.ax.plot([1, 2, 3], [1, 2, 3])
        # self.line = line

        # Add it to the list of plots that
        # will be animated.
        # self.add_plots([self.line])
        pass

    def add_plot(self, plot: plt.Artist) -> None:
        """
        Add a list of plot objects so that they can be animated.
        """
        self._plots.append(plot)

    def add_plots(self, plot_objects: List[plt.Artist]) -> None:
        """
        Add a single plot to be animated.
        """
        for i in range(len(plot_objects)):
            self._plots.append(plot_objects[i])

    def update(self) -> None:
        """
        Update how each plots will change between each animation frame.
        This must be implemented in the inherited classes.
        """
        raise NotImplementedError

    def _make_frame(self, i: int) -> list:
        """
        Generate a single animation frame.
        """
        self.update()
        t = perf_counter()
        self.delta_t = t - self._t
        self._t = t
        if not self.backendiskivy:
            return self._plots
        else:
            return []

    def animation_loop(self) -> None:
        """This method plays the animation. This must be called in order
        for an animation to be shown.
        """
        text_objects = []  # Ensure that text boxes are rendered last
        if self.autoaddartists:
            self_dict = self.__dict__
            for key in self_dict:
                if any([isinstance(self_dict[key], artist) for
                        artist in artists]):
                    if self_dict[key] not in self._plots:
                        # Ensure that text boxes are rendered last
                        if isinstance(self_dict[key], Text):
                            text_objects.append(self_dict[key])
                        else:
                            self._plots.append(self_dict[key])
            self._plots.extend(text_objects)

        self.main_animation = animation.FuncAnimation(
                self.figure,
                self._make_frame,
                blit=True,
                interval=self.animation_interval
        )
