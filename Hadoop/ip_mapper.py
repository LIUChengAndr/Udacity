import re


f = '10.223.157.186 blah cory [15/Jul/2009:15:50:35 -0700] "GET /assets/js/lowpro.js HTTP/1.1" 200 10469'

data =  map(''.join, re.findall(r'\"(.*?)\"|\[(.*?)\]|(\S+)', f))
host, ident, authuser, date, request, status, bytes = data
r,s,t = request.split()
print r