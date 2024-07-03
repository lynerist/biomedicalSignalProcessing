import functions as f

class AFDetector:
    """
        Each function is a block from the Atrial Fibrillation Detector.
    """

    @staticmethod
    def ectopicBeatsFiltering(rrIntervals):
        rrIntervals = f.checkTypeList(rrIntervals)
        return [rrIntervals[0]] + [f.median3(rrIntervals[i-1],rrIntervals[i],rrIntervals[i+1]) 
                for i in range(1, len(rrIntervals)-1)] + [rrIntervals[-1]]
        
    @staticmethod
    def estimationRRTrend(rrIntervals, alpha=f.ALPHA):
        rrIntervals = list(rrIntervals).copy()
        return f.exponentialAverager(rrIntervals, alpha)
        
    @staticmethod
    def intervalIrregularity(rrIntervals, N=f.WINDOWLEN, gamma=f.GAMMA):
        rrIntervals = f.checkTypeList(rrIntervals)
        rrIntervals = AFDetector.ectopicBeatsFiltering(rrIntervals) #Va fatto?!?!?!

        M = [(2/(N*(N-1))) * sum([
                                sum([
                                    (1 if abs((f.IDEAL_RR_INTERVAL if i-j<0 else rrIntervals[i-j]) -
                                                (f.IDEAL_RR_INTERVAL if i-k<0 else rrIntervals[i-k]))-gamma > 0 else 0) 
                                        for k in range(j+1, N)]) # I USE N INSTEAD OF N+1 THAT WAS TAKING THE Nth+1 VALUE
                            for j in range(0, N)]) 
            for i in range(0, len(rrIntervals))]       
        
        return [m/r for m,r in zip(f.exponentialAverager(M), AFDetector.estimationRRTrend(rrIntervals))]
            
    @staticmethod
    def bigeminySuppression(rrIntervals, N=f.WINDOWLEN):
        rrIntervals = f.checkTypeList(rrIntervals)
        rm = AFDetector.ectopicBeatsFiltering(rrIntervals)
        return f.exponentialAverager([(sum([rm[n-j]for j in range(0, N)]) / sum([rrIntervals[n-j]for j in range(0, N)]) -1)**2 for n in range(0, len(rrIntervals))])

    @staticmethod
    def signalFusion(rrIntervals, N=f.WINDOWLEN, gamma=f.GAMMA, delta=f.DELTA):
        It = AFDetector.intervalIrregularity(rrIntervals, N, gamma)
        Bt = AFDetector.bigeminySuppression(rrIntervals, N)
        return [It[i] if Bt[i]>=delta else Bt[i] for i in range(len(rrIntervals))]
    
    @staticmethod
    def detectAF(rrIntervals, eta=f.ETA):
        O = AFDetector.signalFusion(rrIntervals)
        return [1 if x > eta else 0 for x in O]