import re

s = "online    8-rk39-15              3.0               102        011025010010040130   GWSL       15         cc4b731d863c   1.1.251"
S = "offline   gw01-192.168.111.104   3.0               102        011025010010040130   GWSL       51         5410ec337f26   1.1.251"
s = re.sub("\s+",":",s).split(":")
print(s)
S = re.sub("\s+",":",S).split(":")
print(S)