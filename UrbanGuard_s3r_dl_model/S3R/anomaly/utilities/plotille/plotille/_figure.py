
from __future__ import absolute_import, division, print_function, unicode_literals























from collections import namedtuple
from datetime import timedelta
from itertools import cycle
import os
import re

from six.moves import zip

from ._canvas import Canvas
from ._colors import color
from ._input_formatter import InputFormatter
from ._util import hist, mk_timedelta, timestamp





class Figure(object):
    """Figure class to compose multiple plots.

    Within a Figure you can easily compose many plots, assign labels to plots
    and define the properties of the underlying Canvas. Possible properties that
    can be defined are:

        width, height: int    Define the number of characters in X / Y direction
                              which are used for plotting.
        x_limits: float       Define the X limits of the reference coordinate system,
                              that will be plottered.
        y_limits: float       Define the Y limits of the reference coordinate system,
                              that will be plottered.
        color_mode: str       Define the used color mode. See `plotille.color()`.
        with_colors: bool     Define, whether to use colors at all.
        background: multiple  Define the background color.
        x_label, y_label: str Define the X / Y axis label.
    """
    _COLOR_SEQ = [
        {'names': 'white', 'rgb': (255, 255, 255), 'byte': 0X7},
        {'names': 'red', 'rgb': (255, 0, 0), 'byte': 0x1},
        {'names': 'green', 'rgb': (0, 255, 0), 'byte': 0x2},
        {'names': 'yellow', 'rgb': (255, 255, 0), 'byte': 0x3},
        {'names': 'blue', 'rgb': (0, 0, 255), 'byte': 0x4},
        {'names': 'magenta', 'rgb': (255, 0, 255), 'byte': 0x5},
        {'names': 'cyan', 'rgb': (0, 255, 255), 'byte': 0x6},
    ]

    def __init__(self):
        self._color_seq = iter(cycle(Figure._COLOR_SEQ))
        self._width = None
        self._height = None
        self._x_min = None
        self._x_max = None
        self._y_min = None
        self._y_max = None
        self._color_mode = None
        self._with_colors = True
        self._origin = True
        self.linesep = os.linesep
        self.background = None
        self.x_label = 'X'
        self.y_label = 'Y'
        self._plots = []
        self._in_fmt = InputFormatter()

        self._y_axis_right_align = False

    @property
    def width(self):
        if self._width is not None:
            return self._width
        return 80

    @width.setter
    def width(self, value):
        if not (isinstance(value, int) and value > 0):
            raise ValueError('Invalid width: {}'.format(value))
        self._width = value

    @property
    def height(self):
        if self._height is not None:
            return self._height
        return 40

    @height.setter
    def height(self, value):
        if not (isinstance(value, int) and value > 0):
            raise ValueError('Invalid height: {}'.format(value))
        self._height = value

    @property
    def color_mode(self):
        if self._color_mode is not None:
            return self._color_mode
        return 'names'

    @color_mode.setter
    def color_mode(self, value):
        if value not in ('names', 'byte', 'rgb'):
            raise ValueError('Only supports: names, byte, rgb!')
        if self._plots != []:
            raise RuntimeError('Change color mode only, when no plots are prepared.')
        self._color_mode = value

    @property
    def with_colors(self):
        return self._with_colors

    @with_colors.setter
    def with_colors(self, value):
        if not isinstance(value, bool):
            raise ValueError('Only bool allowed: "{}"'.format(value))
        self._with_colors = value

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        if not isinstance(value, bool):
            raise ValueError('Invalid origin: {}'.format(value))
        self._origin = value

    def register_label_formatter(self, type_, formatter):
        self._in_fmt.register_formatter(type_, formatter)

    def register_float_converter(self, type_, converter):
        self._in_fmt.register_converter(type_, converter)

    def x_limits(self):
        return self._limits(self._x_min, self._x_max, False)

    def set_x_limits(self, min_=None, max_=None):
        self._x_min, self._x_max = self._set_limits(self._x_min, self._x_max, min_, max_)

    def y_limits(self):
        return self._limits(self._y_min, self._y_max, True)

    def set_y_limits(self, min_=None, max_=None):
        self._y_min, self._y_max = self._set_limits(self._y_min, self._y_max, min_, max_)

    def _set_limits(self, init_min, init_max, min_=None, max_=None):
        if min_ is not None and max_ is not None:
            if min_ >= max_:
                raise ValueError('min_ is larger or equal than max_.')
            init_min = min_
            init_max = max_
        elif min_ is not None:
            if init_max is not None and min_ >= init_max:
                raise ValueError('Previous max is smaller or equal to new min_.')
            init_min = min_
        elif max_ is not None:
            if init_min is not None and init_min >= max_:
                raise ValueError('Previous min is larger or equal to new max_.')
            init_max = max_
        else:
            init_min = None
            init_max = None

        return init_min, init_max

    def _limits(self, low_set, high_set, is_height):
        if low_set is not None and high_set is not None:
            return low_set, high_set

        low, high = None, None
        for p in self._plots:
            if is_height:
                _min, _max = _limit(p.height_vals())
            else:
                _min, _max = _limit(p.width_vals())
            if low is None:
                low = _min
                high = _max

            low = min(_min, low)
            high = max(_max, high)

        return _choose(low, high, low_set, high_set)

    def _y_axis(self, ymin, ymax, label='Y'):
        delta = abs(ymax - ymin)
        if isinstance(delta, timedelta):
            y_delta = mk_timedelta(timestamp(delta) / self.height)
        else:
            y_delta = delta / self.height

        res = [self._in_fmt.fmt(i * y_delta + ymin, abs(ymax - ymin), chars=10) + ' | '
               for i in range(self.height)]
        if self._y_axis_right_align:
            tmp_res = []
            for y_val in res:
                pattern = r'\d.\d+'
                match = re.match(pattern, y_val)
                if match is not None:
                    new_y_val = '{val:.1f}'.format(val=float(match[0])).rjust(10, ' ')
                    new_y_val = '{} | '.format(new_y_val)
                    tmp_res.append(new_y_val)
                else:
                    tmp_res.append(y_val)
            res = tmp_res

        
        res += [self._in_fmt.fmt(self.height * y_delta + ymin, abs(ymax - ymin), chars=10) + ' |']

        
        if self._y_axis_right_align:
            pattern = r'\d.\d+'
            match = re.match(pattern, res[-1])
            if match is not None:
                new_y_val = '{val:.1f}'.format(val=float(match[0])).rjust(10, ' ')
                new_y_val = '{} | '.format(new_y_val)
            res[-1] = new_y_val

        ylbl = '[{}]'.format(label)
        ylbl_left = (10 - len(ylbl)) // 2
        ylbl_right = ylbl_left + len(ylbl) % 2

        res += [' ' * (ylbl_left) + ylbl + ' ' * (ylbl_right) + ' ^']
        return list(reversed(res))

    def _x_axis(self, xmin, xmax, label='X', with_y_axis=False):
        delta = abs(xmax - xmin)
        if isinstance(delta, timedelta):
            x_delta = mk_timedelta(timestamp(delta) / self.width)
        else:
            x_delta = delta / self.width
        starts = ['', '']
        if with_y_axis:
            starts = ['-' * 11 + '|-', ' ' * 11 + '| ']
        res = []

        
        
        
        res += [starts[0] + '|---------' * (self.width // 10) + '|' + '-' * (self.width % 10-2) + '|-> [' + label + ']']

        """ print last value on x-axis """
        _x_axis_info = starts[1] + ' '.join(self._in_fmt.fmt(\
                    i * 10 * x_delta + xmin, delta, left=True, chars=9)
                    for i in range(self.width // 10 + 1))
        _x_axis_info = '{base}{space}{suffix}'.format(base=_x_axis_info.rstrip(),\
                        space=' '*(self.width%10-len(str(self.width))-1), suffix=self.width-1)
        res += [_x_axis_info]
        return res

    def clear(self):
        self._plots = []

    def plot(self, X, Y, lc=None, interp='linear', label=None):  
        if len(X) > 0:
            if lc is None:
                lc = next(self._color_seq)[self.color_mode]
            self._plots += [Plot.create(X, Y, lc, interp, label)]

    def scatter(self, X, Y, lc=None, label=None):  
        if len(X) > 0:
            if lc is None:
                lc = next(self._color_seq)[self.color_mode]
            self._plots += [Plot.create(X, Y, lc, None, label)]

    def histogram(self, X, bins=160, lc=None):  
        if len(X) > 0:
            if lc is None:
                lc = next(self._color_seq)[self.color_mode]
            self._plots += [Histogram.create(X, bins, lc)]

    def show(self, legend=False):
        xmin, xmax = self.x_limits()
        ymin, ymax = self.y_limits()
        if all(isinstance(p, Histogram) for p in self._plots):
            ymin = 0
        
        canvas = Canvas(self.width, self.height,
                        self._in_fmt.convert(xmin), self._in_fmt.convert(ymin),
                        self._in_fmt.convert(xmax), self._in_fmt.convert(ymax),
                        self.background, self.color_mode)

        plot_origin = False
        for p in self._plots:
            p.write(canvas, self.with_colors, self._in_fmt)
            if isinstance(p, Plot):
                plot_origin = True

        if self.origin and plot_origin:
            
            canvas.line(self._in_fmt.convert(xmin), 0, self._in_fmt.convert(xmax), 0)
            canvas.line(0, self._in_fmt.convert(ymin), 0, self._in_fmt.convert(ymax))

        res = canvas.plot(linesep=self.linesep)

        
        yaxis = self._y_axis(ymin, ymax, label=self.y_label)
        res = (
            yaxis[0] + self.linesep +  
            yaxis[1] + self.linesep +  
            self.linesep.join(lbl + line for lbl, line in zip(yaxis[2:], res.split(self.linesep)))
        )

        
        xaxis = self._x_axis(xmin, xmax, label=self.x_label, with_y_axis=True)
        res = (
            res + self.linesep +  
            self.linesep.join(xaxis)
        )

        if legend:
            res += '\n\nLegend:\n-------\n'
            res += '\n'.join([
                color('⠤⠤ {}'.format(p.label if p.label is not None else 'Label {}'.format(i)),
                      fg=p.lc, mode=self.color_mode, no_color=not self.with_colors)
                for i, p in enumerate(self._plots)
                if isinstance(p, Plot)
            ])

        return res


class Plot(namedtuple('Plot', ['X', 'Y', 'lc', 'interp', 'label'])):

    @classmethod
    def create(cls, X, Y, lc, interp, label):  
        if len(X) != len(Y):
            raise ValueError('X and Y dim have to be the same.')
        if interp not in ('linear', None):
            raise ValueError('Only "linear" and None are allowed values for `interp`.')

        return cls(X, Y, lc, interp, label)

    def width_vals(self):
        return self.X

    def height_vals(self):
        return self.Y

    def write(self, canvas, with_colors, in_fmt):
        
        from_points = zip(map(in_fmt.convert, self.X), map(in_fmt.convert, self.Y))
        to_points = zip(map(in_fmt.convert, self.X), map(in_fmt.convert, self.Y))

        
        next(to_points)

        color = self.lc if with_colors else None
        
        for (x0, y0), (x, y) in zip(from_points, to_points):
            canvas.point(x0, y0, color=color)

            canvas.point(x, y, color=color)
            if self.interp == 'linear':
                canvas.line(x0, y0, x, y, color=color)


class Histogram(namedtuple('Histogram', ['X', 'bins', 'frequencies', 'buckets', 'lc'])):
    @classmethod
    def create(cls, X, bins, lc):  
        frequencies, buckets = hist(X, bins)

        return cls(X, bins, frequencies, buckets, lc)

    def width_vals(self):
        return self.X

    def height_vals(self):
        return self.frequencies

    def write(self, canvas, with_colors, in_fmt):
        
        x_diff = (canvas.dots_between(in_fmt.convert(self.buckets[0]), 0,
                                      in_fmt.convert(self.buckets[1]), 0)[0] or 1)
        bin_size = (in_fmt.convert(self.buckets[1]) - in_fmt.convert(self.buckets[0])) / x_diff

        color = self.lc if with_colors else None
        for i in range(self.bins):
            
            if self.frequencies[i] > 0:
                for j in range(x_diff):
                    
                    x_ = in_fmt.convert(self.buckets[i]) + j * bin_size

                    if canvas.xmin <= x_ <= canvas.xmax:
                        canvas.line(x_, 0,
                                    x_, self.frequencies[i],
                                    color=color)


def _limit(values):
    _min = 0
    _max = 1
    if len(values) > 0:
        _min = min(values)
        _max = max(values)

    return (_min, _max)


def _diff(low, high):
    if low == high:
        if low == 0:
            return 0.5
        else:
            return abs(low * 0.1)
    else:
        delta = abs(high - low)
        if isinstance(delta, timedelta):
            return mk_timedelta(timestamp(delta) * 0.1)
        else:
            return delta * 0.1


def _default(low_set, high_set):
    if low_set is None and high_set is None:
        return 0.0, 1.0  

    if low_set is None and high_set is not None:
        if high_set <= 0:
            return high_set - 1, high_set
        else:
            return 0.0, high_set

    if low_set is not None and high_set is None:
        if low_set >= 1:
            return low_set, low_set + 1
        else:
            return low_set, 1.0

    


def _choose(low, high, low_set, high_set):
    no_data = low is None and high is None
    if no_data:
        return _default(low_set, high_set)

    else:  
        if low_set is None and high_set is None:
            
            diff = _diff(low, high)
            return low - diff, high + diff

        if low_set is None and high_set is not None:
            
            if high_set < low:
                
                return high_set - 1, high_set

            diff = _diff(low, high_set)
            return low - diff, high_set

        if low_set is not None and high_set is None:
            
            if low_set > high:
                
                return low_set, low_set + 1

            diff = _diff(low_set, high)
            return low_set, high + diff

        