"""
N= 100  # normal
NT = 9+26
NF = 91+156
S = 100  # special
ST = 5
SF = 95
P(A|B) = B發生的條件下，A發生的機率

"""
TP = 95+155
FN = 5+5
FP = 9+24
TN = 91+156

ACC = (TP+TN)/(TP+FN+FP+TN)
PRE = TP/(TP+FP)
REC = TP/(TP+FN)
F1 = 2*(PRE*REC)/(PRE+REC)
print("ACC:", ACC, "PRE:", PRE)
print("REC:", REC, " F1:", F1)
