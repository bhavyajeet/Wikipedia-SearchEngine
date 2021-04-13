import os



def mergefiles(a,b):
    print ("merging files "+ str(a)+" and "+str(b))
    file1 = open('inddir10/index'+str(a)+'.txt','r')
    file2 = open('inddir10/index'+str(b)+'.txt','r')
    newfile = open('inddir10/'+"strb"+'.txt','w')
    line1 = file1.readline()
    line2 = file2.readline()
    while (line1 and line2 ):
        linespl1 = line1.split(':')
        linespl2 = line2.split(':')
        if linespl1[0] < linespl2[0]:
            newfile.write(line1)
            line1 = file1.readline()
        elif linespl2[0] < linespl1[0] : 
            newfile.write(line2)
            line2 = file2.readline()
        elif linespl1[0] == linespl2[0] :
            newfile.write(linespl1[0]+':' + linespl1[1].strip() + linespl2[1]) 
            line1 = file1.readline()
            line2 = file2.readline() 
    while (line1):
        newfile.write(line1)
        line1 = file1.readline()
    while (line2):
        newfile.write(line2)
        line2 = file2.readline()
    file1.close()
    file2.close()
    newfile.close()
    os.remove('inddir10/index'+str(a)+'.txt')
    os.remove('inddir10/index'+str(b)+'.txt')
    os.rename('inddir10/'+"strb"+'.txt', 'inddir10/index'+str(a//2)+'.txt')


r=6553
while r != 1:
    for i in range(0, r, 2):
        if i + 1 == r:
            os.rename('inddir10/index'+str(i)+'.txt', 'inddir10/index'+str((i)//2)+'.txt')
            break
        mergefiles((i), i+1)
    if (r % 2):
        r = r // 2 + 1
    else:
        r = r // 2
    print("files left: " , r)