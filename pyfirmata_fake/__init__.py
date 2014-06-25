
class Pin(object):
    def __init__(self, *args, **kwargs):
        self.args = list(args)

    def write(self, data):
        print "WRITE %s" % data,
        print self.args

class Arduino(object):
    """
    A board that will set itself up as a normal Arduino.
    """
    def __init__(self, *args, **kwargs):
        self.name = 'Arduino'
        args = list(args)

    def __str__(self):
        return 'Arduino %s ' % self.name

    def exit(self):
        pass

    def get_pin(self, data):
        return Pin(pin=data)
