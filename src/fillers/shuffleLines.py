fileName = input("fileName: ")
splitChr = input("splitChr \\n ?: ")
if splitChr == "":
	splitChr = "\n"
lines = open(fileName).read().split(splitChr)
lines = list(filter(lambda x: len(x)>0, lines))
from random import shuffle
shuffle(lines)
open(fileName, "w").writelines(splitChr.join(lines))