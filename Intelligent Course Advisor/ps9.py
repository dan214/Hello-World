
# Intelligent Course Advisor
#


SUBJECT_FILENAME = "subjects.txt"
SHORT_SUBJECT_FILENAME = "shortened_subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """

    # The following sample code reads lines from the specified file and prints
    # each one.
    inputFile = open(filename,'r')
    
    myDict = {}
    myTuple = []
    discardHeader = inputFile.readline()
    for line in inputFile:
        name,value,work = line.split()
        myDict[name] = (value, work)
    return myDict
               
        

    # TODO: Instead of printing each line, modify the above to parse the name,
    # value, and work of each subject and create a dictionary mapping the name
    # to the (value, work).

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res

#
# Problem 2: Subject Selection By Greedy Optimization
#

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    return subInfo1[0] > subInfo2[0]

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    return subInfo1[1] < subInfo2[1]

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    ratio1 = (float(subInfo1[0])/float(subInfo1[1]))
    ratio2 = (float(subInfo2[0])/float(subInfo2[1]))
    return ratio1 > ratio2
    
def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    subjectsCopy = sorted(subjects, reverse = True)
    newDict = {}
    totalWork = 0.0
    totalList = []
    i = 0
    work = []
    value = []
    myTuple = ()
    for x in subjects:
        work.append(subjects[x][1])
        value.append(subjects[x][0])
    z = 0
    for y in subjects:
        mylist = []
        mylist.append(y)
        mylist.append(work[z])
        mylist.append(value[z])
        totalList.append(mylist)
        z += 1
    subjectsCopy = sorted(totalList,reverse = True)   
    while totalWork < maxWork and i + 1< len(subjectsCopy):
        if cmpValue((value[i],work[i]),(value[i + 1],work[i + 1])) == True:
            newDict[subjectsCopy[i][0]] = (value[i],work[i])
            totalWork += work[i]
        i += 1
    return newDict
            
        
def dToB(n, numDigits):
    """requires: n is a natural number less than 2**numDigits
      returns a binary string of length numDigits representing the
              the decimal number n."""
    assert type(n)==int and type(numDigits)==int and\
           n >=0 and n < 2**numDigits
    bStr = ''
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n//2
    while numDigits - len(bStr) > 0:
        bStr = '0' + bStr
    return bStr
def genPset(Items):
    """Generate a list of lists representing the power set of Items"""
    numSubsets = 2**len(Items)
    templates = []
    for i in range(numSubsets):
        templates.append(dToB(i, len(Items)))
    pset = []
    for t in templates:
        elem = []
        for j in range(len(t)):
            if t[j] == '1':
                elem.append(Items[j])
        pset.append(elem)
    return pset
#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    totalList = []
    work = []
    value = []

    for x in subjects:
        work.append(subjects[x][1])
        value.append(subjects[x][0])
    z = 0
    for y in subjects:
        mylist = []
        mylist.append(y)
        mylist.append(work[z])
        mylist.append(value[z])
        totalList.append(mylist)
        z += 1
    pset = genPset(totalList)
    bestVal = 0.0
    bestSet = None
    otherDict = {}
    for item in pset:
        
        ItemsVal = 0
        ItemsWeight = 0
        for i in item:
            ItemsVal += float(i[1])
            ItemsWeight += float(i[2])   
        if ItemsWeight <= maxWork and ItemsVal > bestVal:
            bestVal = ItemsVal
            
            bestSet = item
    for x in bestSet:
        otherDict[x[0]] = (x[1],x[2])       
    return otherDict
            
subjects = loadSubjects(SHORT_SUBJECT_FILENAME)
print bruteForceAdvisor(subjects, 3)
            
        
            
        















    
    
        


