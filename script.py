# Script to convert IBM DB2 Load Files to SQL Format Files
# © 0x540 fg@naturalsecure.com
import os
import re
import sys

cwd = os.getcwd()
filename = cwd + '\\' + sys.argv[1]
print(filename)
with open(filename) as f:
    lines = f.read().splitlines()
    print(lines)

databasename = lines[3].replace("\"", '')
tablename = lines[4].replace("\"", '')
numberrecords = lines[5]
columnname = 'random'
cnames = []
types = []
lengths = []
prefix = []
del lines[:6]
lines.pop()
p = re.compile("\"(.*?)\"")
for line in lines:
    # Get column name with regex "(.*?)
    if "\"" in line:
        columnname = re.findall(r'"(.*?)"', line)
        cnames.append(columnname[0])
    else:
        if "CHAR(" in line:
            types.append('SQLCHAR')
            s = re.findall(r'CHAR\((.*?)\)', line)
            s = int(s[0].replace("0", ""))
            lengths.append(s)
            prefix.append(2)
        elif "DECIMAL" in line:
            types.append('SQLDECIMAL')
            s = re.findall(r'\((.*?)\)', line)
            s = s[0].replace("0", "")
            l1 = s.split(':')
            subtracted = int(l1[1]) - int(l1[0]) + 1
            lengths.append(subtracted)
            prefix.append(1)
        elif "VARCHAR" in line:
            types.append('SQLCHAR')
            s = re.findall(r'\((.*?)\)', line)
            s = s[0].replace("0", "")
            l1 = s.split(':')
            subtracted = int(l1[1]) - int(l1[0]) + 1
            lengths.append(subtracted)
            prefix.append(2)

finallines = []
finallines.append('13.0')  # Edit for BCP utility version SQL Server 2016
finallines.append(str(len(cnames)))
print('CREATE TABLE ' + '[' + tablename + ']')
print('\t(')
for i in range(0, len(cnames)):
    print(cnames[i] + ' ' + types[i] + ',')
    newline = str(i) + '  ' + types[i] + '  ' + str(prefix[i]) + str(lengths[i]) + '  ' + '\"\\r\\n\"' + '  ' + str(
        i) + '  ' + cnames[i] + '  ' + 'SQL_Latin1_General_CP1_CI_AS'
    finallines.append(newline)
print('\t);')
f = open(tablename, 'w')

for fline in finallines:
    f.write(fline + '\r\n')  # python will convert \n to os.linesep
f.close()  # you can omit in most cases as the destructor will call it
