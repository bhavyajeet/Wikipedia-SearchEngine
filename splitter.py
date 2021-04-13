totfiles = 0
import os
def fileSplit():
    lines = []
    filecount = 0
    threshold=10000
    file = open('./complete/index0.txt', 'r')
    sec = open('./complete/secondary.txt', 'w')
    line = file.readline().strip('\n')
    while line:
        word = line.split(':')[0]
        if not (word[0:7].isdecimal() and len(word)>10 ):
            #print(line)
            lines.append(line)
        if len(lines) % threshold == 0 and lines != [] :
            sec.write(lines[0].split(":")[0] + '\n')
            writ = open('complete/fin'+str(filecount)+'.txt', 'w')
            for l in lines:
                writ.write(l + '\n')
            filecount += 1
            lines = []
        line = file.readline().strip('\n')
    if len(lines) > 0:
        sec.write(lines[0].split(":")[0] + '\n')
        writ = open('complete/fin'+str(filecount)+'.txt', 'w')
        for l in lines:
            writ.write(l + '\n')
        filecount += 1
        lines = []
    #os.remove('./10inddir/full.txt')
    file.close()
    sec.close()
    return filecount

totfiles = fileSplit()
