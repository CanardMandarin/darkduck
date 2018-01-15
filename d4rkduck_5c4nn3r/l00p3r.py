from subprocess import call
class l00p3r:
    """
    looper that loops
    """

    def __init__(self, list, split=False):
        self.list = list
        self.split = split

    def l00p(self):
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


class f0rm4t:
    """
    return usr:pwd couple Hydra compatible
    """

    def __init__(self, vict,port, usr, pwd):
        self.vict = vict
        self.usr = usr
        self.pwd = pwd
        self.port = port

    def f0rm4t(self):
        """
        return formatted
        :return: str
        """
        f0rm =  "-v {} -P {} -u {} -p {}".format(self.vict.rstrip(), self.port.rstrip(), self.usr.rstrip(), self.pwd.rstrip())
        return f0rm


class shellproc:
    def __init__(self):
        pass

    def exec(self,cmd):
        return call(cmd)

class cnx:
    def __init__(self,ip,port,usr,password,protocol):
        self.ip = ip
        self.port = port
        self.usr = usr
        self.password = password
        self.protocol = protocol

    def c0nnec7(self):
        if self.protocol == "ftp":
            pass






