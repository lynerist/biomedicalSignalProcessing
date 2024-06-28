import functions as f
import numpy as np

class AFDetector:
    IDEAL_RR_INTERVAL = 0.8 if f.SECONDS else 800

    @staticmethod
    def ectopicBeatsFiltering(rrInterval):
        rrInterval = (rrInterval.tolist() if rrInterval.__class__.__name__ == "ndarray" else rrInterval) 
        return [rrInterval[0]] + [f.median3(rrInterval[i-1],rrInterval[i],rrInterval[i+1]) 
                for i in range(1, len(rrInterval)-1)] + [rrInterval[-1]]
        
    @staticmethod
    def estimationRRTrend(rrInterval, alpha=0.02):
        rrInterval = (rrInterval.tolist().copy() if rrInterval.__class__.__name__ == "ndarray" else rrInterval).copy()
        return f.exponentialAverager(rrInterval, alpha)
        
    @staticmethod
    def intervalIrregularity(rrInterval, N=8, gamma=(0.03 if f.SECONDS else 30)):
        rrInterval = (rrInterval.tolist() if rrInterval.__class__.__name__ == "ndarray" else rrInterval)
        
        M = [(2/(N*(N-1))) * sum([
                                sum([
                                    (1 if abs((AFDetector.IDEAL_RR_INTERVAL if i-j<0 else rrInterval[i-j]) -
                                                (AFDetector.IDEAL_RR_INTERVAL if i-k<0 else rrInterval[i-k]))-gamma > 0 else 0) 
                                        for k in range(j+1, N)]) # I USE N INSTEAD OF N+1 THAT WAS TAKING THE Nth+1 VALUE
                            for j in range(0, N)]) 
            for i in range(0, len(rrInterval))]       
        
        return [m/r for m,r in zip(f.exponentialAverager(M), AFDetector.estimationRRTrend(rrInterval))]
            
    @staticmethod
    def bigeminySuppression(rrInterval, N=8):
        rrInterval = (rrInterval.tolist() if rrInterval.__class__.__name__ == "ndarray" else rrInterval)
        rm = AFDetector.ectopicBeatsFiltering(rrInterval)

        return f.exponentialAverager([(sum([rm[n-j]for j in range(0, N)]) / sum([rrInterval[n-j]for j in range(0, N)]) -1)**2 for n in range(0, len(rrInterval))])

    @staticmethod
    def signalFusion(rrInterval, N=8, gamma=(0.03 if f.SECONDS else 30), delta=0.0002):
        It = AFDetector.intervalIrregularity(rrInterval, N, gamma)
        Bt = AFDetector.bigeminySuppression(rrInterval, N)
        return [It[i] if Bt[i]>=delta else Bt[i] for i in range(len(rrInterval))]
    
        
    @staticmethod
    def detectAF(rrInterval, eta=0.725):
        O = AFDetector.signalFusion(rrInterval)
        return [1 if x > eta else 0 for x in O]