import logging

class Base(object):
    """A base command."""
    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs
        logging.basicConfig(filename='debug.log',level=logging.INFO, format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')

    def run(self):
        raise NotImplementedError('You must implement the run() method yourself')