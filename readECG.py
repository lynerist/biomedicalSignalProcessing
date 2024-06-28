import wfdb
import wfdb.processing
import signalECG
from AFDetector import AFDetector
import functions as f
from operator import and_, or_
#64

database = "database"
filename = database + "/00"

import time
start_time = time.time()


s = signalECG.Signal(filename)
afd = AFDetector()

rr = s.rrIntervals

rm = afd.ectopicBeatsFiltering(rr)
rt = afd.estimationRRTrend(rr) 
ii = afd.intervalIrregularity(rr)
bt = afd.bigeminySuppression(rr)
O = afd.signalFusion(rr)
detector = afd.detectAF(rr)
print("--- %s seconds ---" % (time.time() - start_time))

plotNames = ["rr", "rm", "rt", "It", "Bt", "O"]

toPlot = [rr, rm, rt, ii, bt, O]
f.plotSerie(plotNames, toPlot)

# print(len(rr), len(rm), len(rt), len(ii), len(bt), len(O))


#wfdb.plot_wfdb(record=s.record, title='Example signals')

#print(rr[:50])

#plotNames = ["rr","bt", "O", "D"]
#toPlot = [rr, bt, O, detector]

#f.plotSerie(plotNames, toPlot)


#for k,v in s.an.__dict__.items():
#    print(f"{k}: {(v if type(v)!=list or len(v) < 2000 else len(v))}")

realAFIntervals = s.getAFBeatsAnnotations()
realAFLabels = s.getAFLabels()

truePositive = sum(map(and_, detector, realAFLabels))
labeledPositive = sum([a.duration() for a in realAFIntervals])
sensibility = labeledPositive==0 and 100 or truePositive/labeledPositive*100 

trueNegative = len(detector)-sum(map(or_, detector, realAFLabels))
labeledNegative = len(detector)-sum([a.duration() for a in realAFIntervals])
specificity = labeledNegative==0 and 100 or trueNegative/labeledNegative*100 

#print(f"{filename} -> sensibility:{sensibility:.2f}% ({truePositive} TP out of {labeledPositive}) specificity:{specificity:.2f}% ({trueNegative} TN out of {labeledNegative})")

print(f"sensitivity:{sensibility:.2f}% specificity:{specificity:.2f}%")
