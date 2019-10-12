"""
Locate mouse function
"""
from tkinter import Event
from typing import List, Tuple


def locate_mouse(event: Event,
                 bounds: List[int],
                 window_height: int,
                 axes_location: List[int]
                 ) -> Tuple[float, float]:
    """
    Locate the position of the mouse with respect to the
    coordinates displayed on the plot axes.
    
    event: Tkinter event
    bounds: A list storing the xmin, xmax, ymin, and ymax boundaries of the
            plot in this order.
    window_height: The height of the canvas.
                   This can be obtained by calling
                   [ref to gui].canvas.get_tk_widget().winfo_height()
    axes_location: A list of exactly 6 ints where:
                    -The first two items are where the x and y axis begin
                     (in terms of pixels starting from the *bottom left corner*
                     of the canvas).
                    -The next two values give the location of the origin
                    -The last two are where the axis end.
    """

    xmin, xmax, ymin, ymax = bounds
    xrange = xmax - xmin
    yrange = ymax - ymin

    x_canvas = event.x
    y_canvas = window_height - event.y
    pxi, pyi, px0, py0, pxf, pyf = axes_location

    pxrange = pxf - pxi
    pyrange = pyf - pyi

    x_pxl_plot = x_canvas - px0
    y_pxl_plot = y_canvas - py0

    x = x_pxl_plot*(xrange/pxrange)
    y = y_pxl_plot*(yrange/pyrange)

    # Use the following to find the canvas coordinate
    # locations of where the axes intersect and where they end:
    # self.ax.grid()
    # print ("x: %d, y: %d"%(x_canvas, y_canvas))
    # print (self.bounds)
    # print(x, y)

    return x, y
