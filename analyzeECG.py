import signalECG
from AFDetector import AFDetector
import functions as f
from operator import and_, or_

database = "database"
filename = database + "/00"

filename = database + "/03"
filename = database + "/05"
filename = database + "/06"
filename = database + "/07"
filename = database + "/08"
filename = database + "/10"
filename = database + "/100"
filename = database + "/101"
filename = database + "/102"
filename = database + "/103"

import time
start_time = time.time()

s = signalECG.Signal(filename)
afd = AFDetector()

rr = s.rrIntervals

plotNames = ["rr"]
toPlot = [rr]

rm = afd.ectopicBeatsFiltering(rr); plotNames.append("rm"); toPlot.append(rm)
#rt = afd.estimationRRTrend(rr) ; plotNames.append("rt"); toPlot.append(rt)
ii = afd.intervalIrregularity(rr); plotNames.append("It"); toPlot.append(ii)
#bt = afd.bigeminySuppression(rr); plotNames.append("Bt"); toPlot.append(bt)
#O = afd.signalFusion(rr); plotNames.append("O"); toPlot.append(O)
detector = afd.detectAF(rr)#; plotNames.append("Detector"); toPlot.append(detector)
print(f"--- {(time.time() - start_time):.4f} seconds --- to analyze a {int(s.getDuration()/60/60)}h {int(s.getDuration()/60)%60}m long signal")



f.plotSerie(plotNames, toPlot)

realAFIntervals = s.getAFBeatsAnnotations()
realAFLabels = s.getAFLabels()

truePositive = sum(map(and_, detector, realAFLabels))
labeledPositive = sum([a.duration() for a in realAFIntervals])
sensitivity = labeledPositive==0 and 100 or truePositive/labeledPositive*100 

trueNegative = len(detector)-sum(map(or_, detector, realAFLabels))
labeledNegative = len(detector)-sum([a.duration() for a in realAFIntervals])
specificity = labeledNegative==0 and 100 or trueNegative/labeledNegative*100 

print(f"sensitivity:{sensitivity:.2f}% specificity:{specificity:.2f}%")
