class Looper:
    """
    Looper that loops
    """

    def __init__(self, list, split=False):
        self.list = list
        self.split = split

    def loop(self):
        """
        loop over txt file as usr:pwd source
        :return:
        """
        _4rr4y = []
        with open(self.list, 'r') as list:
            for l in list:
                spl = l.split(":")
                if self.split:
                    _4rr4y.append(spl)
                else:
                    _4rr4y.append(l)

        return _4rr4y


