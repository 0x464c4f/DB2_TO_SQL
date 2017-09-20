# Script to convert IBM DB2 Load Files to SQL Format Files
# © 0x540 fg@naturalsecure.com
import os
import re
import sys

columnname = 'random'
cnames = []
types = []
lengths = []
prefix = []
typesbcp = []

# 1. Open Format File
cwd = os.getcwd()
filename = cwd + '\\' + sys.argv[1]
print(filename)
with open(filename) as f:
    lines = f.read().splitlines()
    print(lines)

# 2. Remove unnecessary data
databasename = lines[3].replace("\"", '')
tablename = lines[4].replace("\"", '')
numberrecords = lines[5]
del lines[:6]
lines.pop()

# 3. Read line by line and append data to lists
p = re.compile("\"(.*?)\"")
for line in lines:
    # Get column name with regex "(.*?)
    if "\"" in line:
        columnname = re.findall(r'"(.*?)"', line)
        cnames.append(columnname[0])
    else:
        if "CHAR(" in line:
            types.append('VARCHAR')
            typesbcp.append('SQLCHAR')
            s = re.findall(r'CHAR\((.*?)\)', line)
            s = int(s[0].lstrip("0"))
            lengths.append(s)
            prefix.append('0')
        elif "DECIMAL" in line:
            typesbcp.append('SQLCHAR')
            types.append('VARCHAR')
            s = re.findall(r'\((.*?)\)', line)
            s = s[0].lstrip("0")
            l1 = s.split(':')
            subtracted = int(l1[1]) - int(l1[0]) + 1
            lengths.append(subtracted)
            prefix.append('0')
        elif "VARCHAR" in line:
            types.append('VARCHAR')
            typesbcp.append('SQLCHAR')
            s = re.findall(r'\((.*?)\)', line)
            s = s[0].lstrip("0")
            l1 = s.split(':')
            subtracted = int(l1[1]) - int(l1[0]) + 1
            lengths.append(subtracted)
            prefix.append('0')

finallines = []
finallines.append('13.0')  # BCP utility version SQL Server 2016
finallines.append(str(len(cnames)))

# 4. Print SQL Create Table Query
print('___________________________')
print('CREATE TABLE SQL COMMAND')
print('___________________________')
print()
print("CREATE TABLE " + tablename)
print("\t(")

# 5. Generate SQL Format .fmt file and write content to it
delimiter = "\"\""
for i in range(0, len(cnames)):
    print(cnames[i] + ' ' + types[i] + '(' + str(lengths[i]) + ') ' + 'NULL' + ' ,')
    if i == len(cnames) - 1:
        delimiter = '\"\\r\\n\"'
    newline = str(i + 1) + '  ' + typesbcp[i] + '  ' + prefix[i] + '  ' + str(
        lengths[i]) + '  ' + delimiter + '  ' + str(i + 1) + '  ' + cnames[i] + '  ' + 'SQL_Latin1_General_CP1_CI_AS'
    finallines.append(newline)
print("\t);")
f = open(tablename[1:] + '.fmt', 'w')
for fline in finallines:
    f.write(fline + '\n')  # python will convert \n to os.linesep
f.close()  # you can omit in most cases as the destructor will call it

# 6. Generate SQL BULK Insert Command
print('___________________________')
print('TABLE IMPORT SQL COMMAND')
print('___________________________')
print()
print('TRUNCATE TABLE' + tablename + ';')
print('GO')
print('BULK INSERT dbo.' + tablename[1:])
print("	FROM \'" + cwd + '\\' + tablename[1:] + '.txt\'')
print(" WITH (FORMATFILE = \'C:\\Users\\Steve\\Downloads\\script\\" + tablename[1:] + ".fmt\' " + ");")
