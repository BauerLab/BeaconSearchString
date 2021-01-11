import sys, os
from Bio import SeqIO

withN = False
results = []
bases = ["a", "c", "g", "t"]
refName = ">hCoV-19/Wuhan/WIV04/2019|EPI_ISL_402124|2019-12-30"
refSeq = ""
newSeq = ""
newStrain = ""
cwd = os.getcwd()

def read_fasta(fp):
    name, seq = None, []
    for line in fp:
        line = line.rstrip()
        if line.startswith(">"):
            if name: yield (name, ''.join(seq))
            name, seq = line, []
        else:
            seq.append(line)
    if name: yield (name, ''.join(seq))

for filename in os.scandir(cwd+"/tempFolder"):
	if (filename.path.endswith("_alignment.txt")):
		with open(filename) as f:
			for name, sequence in read_fasta(f):
				if name == refName:
					refSeq = sequence.lower()
				else:
					newSeq = name
					newStrain = sequence.lower()
		missing = set([pos for pos, char in enumerate(refSeq) if char == "-"]) #position of deletions in ref
		fixedStrain = "".join([char for idx, char in enumerate(newStrain) if idx not in missing]) #remove these positions from other sequence
		if withN:
			for i, (x,y) in enumerate(zip(refSeq, fixedStrain)):
				if x != y and y != "-":
					results.append(x.upper()+str(i+1)+y.upper())
		else:
			for i, (x,y) in enumerate(zip(refSeq, fixedStrain)):
				if x != y and y != "-" and y in bases and x in bases:
					results.append(x.upper()+str(i+1)+y.upper())
		print(newSeq, "&".join(results))
		results = []