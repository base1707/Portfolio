import telnetlib

tn = telnetlib.Telnet(host = "localhost", port = "9090")
tn.write(b"0002 B2 08:17:07.167 01\r")
tn.write(b"0001 A1 01:13:02.257 00\r")
tn.write(b"exit")
tn.close()