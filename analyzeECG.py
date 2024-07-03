import signalECG
from AFDetector import AFDetector
import functions as f
from operator import and_, or_

database = "database"
filename = database + "/22"

import time
start_time = time.time()

s = signalECG.Signal(filename)
afd = AFDetector()

rr = s.rrIntervals

print(len(rr))

rm = afd.ectopicBeatsFiltering(rr)
rt = afd.estimationRRTrend(rr) 
ii = afd.intervalIrregularity(rr)
bt = afd.bigeminySuppression(rr)
O = afd.signalFusion(rr)
detector = afd.detectAF(rr)
print(f"--- {(time.time() - start_time):.4f} seconds --- to analyze a {int(s.getDuration()/60/60)}h {int(s.getDuration()/60)%60}m long signal")

plotNames = ["rr", "rm"]#, "rt", "It", "Bt", "O"]

toPlot = [rr, rm,]# rt, ii, bt, O]

f.plotSerie(plotNames, toPlot)

realAFIntervals = s.getAFBeatsAnnotations()
realAFLabels = s.getAFLabels()

truePositive = sum(map(and_, detector, realAFLabels))
labeledPositive = sum([a.duration() for a in realAFIntervals])
sensibility = labeledPositive==0 and 100 or truePositive/labeledPositive*100 

trueNegative = len(detector)-sum(map(or_, detector, realAFLabels))
labeledNegative = len(detector)-sum([a.duration() for a in realAFIntervals])
specificity = labeledNegative==0 and 100 or trueNegative/labeledNegative*100 

print(f"sensitivity:{sensibility:.2f}% specificity:{specificity:.2f}%")
