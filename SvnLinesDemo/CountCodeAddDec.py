__author__ = 'Administrator'
import os
import MySQLdb

homedir = os.getcwd()
print homedir

dirs = homedir.split('\\') #only work in windows
homedir = dirs[len(dirs)-1]

output = os.popen('svn log')
list_of_all_the_lines = output.readlines()



# def getMiddleStr(content, startStr, endStr):
#     startIndex = content.index(startStr)
#     if startIndex >= 0:
#         startIndex += len(startStr)
#         endIndex = content[startIndex:].index(endStr) + startIndex
#         return content[startIndex:endIndex]


def getAddDecLinesCount(version):
    version2=int(version)-1
    cmd= 'svn diff -r r%d:r%s'% (version2,version)
    output = os.popen(cmd)
    list_of_all_the_lines = output.readlines()

    # file_object = open('b.txt')
    # try:
    #     list_of_all_the_lines = file_object.readlines()
    # finally:
    #     file_object.close()

    skipLine = 0
    addLinesCount = 0
    decLinesCount = 0

    for l in list_of_all_the_lines:
        if skipLine > 0:
            skipLine = skipLine - 1
        else:
            if l.find("Index: ") == 0:
                skipLine = 4
            else:
                if l.find("@@") == 0:
                    i = 0
                else:
                    if l[0] == '+':
                        addLinesCount = addLinesCount + 1
                        #print l
                    if l[0] == '-':
                        decLinesCount = decLinesCount + 1
                        #print l

    return addLinesCount, decLinesCount

db = MySQLdb.connect("xxx","root","xxx","svnstat" )

cursor = db.cursor()


for l in list_of_all_the_lines:
    if ( l.find('|')>0 ) and (l.find('r')==0):
        ll=l.split('|')
        version = ll[0].strip()
        user = ll[1].strip()
        versiondate=ll[2].strip()

        version = version[1:]
        if version!="":
            addCount,decCount= getAddDecLinesCount(version)
            versiondate=versiondate[0:19]
            print version,user,versiondate,addCount,decCount
            sql="insert into svnstat(version,user,version_date,add_line_count,dec_line_count,homedir) values (%s,'%s','%s',%d,%d,'%s')" % ( version,user,versiondate,addCount,decCount,homedir)
            print sql
            try:
                cursor.execute(sql )
                db.commit()
            except Exception, e:
                print e

#select sum(add_line_count-dec_line_count),user from svnstat group by user
#db.commit()

