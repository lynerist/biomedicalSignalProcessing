import signalECG
from AFDetector import AFDetector
from operator import and_, or_

totalTruePositive = 0
totalTrueNegative = 0
totalLabeledPositive = 0
totalLabeledNegative = 0

database = "database"

with open(f"{database}/RECORDS") as r:
    for filename in [x[:-1] for x in r.readlines()]:        
        if filename in ["64", "00735", "03665", "04936", "05091"]: continue #skip wrong annotated files

        s = signalECG.Signal(f"{database}/"+filename)
        afd = AFDetector()

        rr = s.rrIntervals
        detector = afd.detectAF(rr)

        realAFIntervals = s.getAFBeatsAnnotations()
        realAFLabels = s.getAFLabels()

        #every beatGroup beats
        beatsGroup = 1
        detector = [sum(detector[i:i+beatsGroup])>beatsGroup/2 and 1 or 0 for i in range(0,len(detector), beatsGroup)]
        realAFLabels = [sum(realAFLabels[i:i+beatsGroup])>beatsGroup/2 and 1 or 0 for i in range(0,len(realAFLabels), beatsGroup)]

        truePositive = sum(map(and_, detector, realAFLabels))
        labeledPositive = sum(realAFLabels)
        sensibility = labeledPositive==0 and 100 or truePositive/labeledPositive*100

        trueNegative = len(detector)-sum(map(or_, detector, realAFLabels))
        labeledNegative = len(realAFLabels)-labeledPositive
        specificity = labeledNegative==0 and 100 or trueNegative/labeledNegative*100

        print(f"{filename:3} -> sensibility: {sensibility:.2f}% ({truePositive}/{labeledPositive})\t\tspecificity: {specificity:.2f}% ({trueNegative}/{labeledNegative})")

        totalTruePositive += truePositive
        totalTrueNegative += trueNegative
        totalLabeledPositive += labeledPositive
        totalLabeledNegative += labeledNegative

    print(f"At the end, {totalTruePositive/totalLabeledPositive*100:.2f}% total sensibility and {totalTrueNegative/totalLabeledNegative*100:.2f}% specificity")
