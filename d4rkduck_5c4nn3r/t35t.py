from d4rkduck_5c4nn3r.l00p3r import l00p3r
from d4rkduck_5c4nn3r.l00p3r import f0rm4t
from d4rkduck_5c4nn3r.l00p3r import cnx

__u5Er_p455w0rd = l00p3r("pwd.txt", True).l00p()
__1p5 = l00p3r("f4k3_ip5.txt").l00p()
__pr0t0c0l5 = l00p3r("pr0t0c0l5.txt", True).l00p()

for ip in __1p5:
    for pr in __pr0t0c0l5:
        for u in __u5Er_p455w0rd:
            print(f0rm4t(ip, pr[0], u[0], u[1]).f0rm4t())
            if cnx(ip, pr[0], u[0], u[1], pr[1]).c0nnec7():
                print(f0rm4t(ip, pr[0], u[0], u[1]).f0rm4t())

