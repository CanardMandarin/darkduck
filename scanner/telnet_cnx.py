import telnetlib

thost="10.3.107.82"
tuser="support"
tpass="support"

tn = telnetlib.Telnet(thost, 23)
tn.set_debuglevel(2)
tn.read_until("ogin: ")
tn.write(tuser + "\n")
tn.read_until("assword: ")
tn.write(tpass + "\n")
n, match, previous_text = tn.expect([r'incorrect', r'\$'], 4)
if n == 0:
        print("FAILED")
else:
        print("SUCCESS")

