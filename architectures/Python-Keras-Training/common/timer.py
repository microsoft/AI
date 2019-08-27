import collections
import functools
import logging
from timeit import default_timer


class Timer(object):

    """

    Keyword arguments:
        output:   if True, print output after exiting context.
                  if callable, pass output to callable.
        format:   str.format string to be used for output; default "took {} seconds"
        prefix:   string to prepend (plus a space) to output
                  For convenience, if you only specify this, output defaults to True.
    """

    def __init__(self,
                 timer=default_timer,
                 factor=1,
                 output=None,
                 fmt="took {:.3f} seconds",
                 prefix=""):
        self._timer = timer
        self._factor = factor
        self._output = output
        self._fmt = fmt
        self._prefix = prefix
        self._end = None
        self._start = None

    def start(self):
        self._start = self()

    def stop(self):
        self._end = self()

    def __call__(self):
        """ Return the current time """
        return self._timer()

    def __enter__(self):
        """ Set the start time """
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """ Set the end time """
        self.stop()

        if self._output is True or (self._output is None and self._prefix):
            self._output = print

        if callable(self._output):
            output = " ".join([self._prefix, self._fmt.format(self.elapsed)])
            self._output(output)

    def __str__(self):
        return '%.3f' % (self.elapsed)

    @property
    def elapsed(self):
        """ Return the elapsed time
        """
        if self._end is None:
            # if elapsed is called in the context manager scope
            return (self() - self._start) * self._factor
        else:
            # if elapsed is called out of the context manager scope
            return (self._end - self._start) * self._factor


def timer(logger=None,
          level=logging.INFO,
          fmt="function %(function_name)s execution time: %(execution_time).3f",
          *func_or_func_args,
          **timer_kwargs):
    """ Function decorator displaying the function execution time
    """
    def wrapped_f(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            with Timer(**timer_kwargs) as t:
                out = f(*args, **kwargs)
            context = {
                'function_name': f.__name__,
                'execution_time': t.elapsed,
            }
            if logger:
                logger.log(
                    level,
                    fmt % context,
                    extra=context)
            else:
                print(fmt % context)
            return out

        return wrapped

    if (len(func_or_func_args) == 1
            and isinstance(func_or_func_args[0], collections.Callable)):
        return wrapped_f(func_or_func_args[0])
    else:
        return wrapped_f
