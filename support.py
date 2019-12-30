import re

def getdict(filename):
    rst = []
    file1 = open(filename,"r")
    for line in file1:
        words = line.split(',')
        for word in words:
            word = word.strip()
            if word != '':
                rst.append(word)
    file1.close()
    return rst
def getregax(filename):
    return_dict = {}
    file1 = open(filename, 'r')
    for line in file1:
        line = line.split('->')
        return_dict[line[0].strip()] = line[1].strip()
    file1.close()
    return return_dict

def checkpattern(link):
    rst = {}
    rst = getregax('re_patterns.txt')
    regax = re.compile(rst['linkpattern'])
    if regax.search(link):
        return True
    else:
        return False