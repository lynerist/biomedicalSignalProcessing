import functions as f
import numpy as np
import scipy as sc

class AFDetector:
    IDEAL_RR_INTERVAL = 0.8 if f.SECONDS else 800

    @staticmethod
    def ectopicBeatsFiltering(rrInterval):
        if not isinstance(rrInterval, np.ndarray): rrInterval = np.array(rrInterval)
        return sc.signal.medfilt(rrInterval)
        
    @staticmethod
    def estimationRRTrend(rrInterval, alpha=0.02):
        if not isinstance(rrInterval, np.ndarray): rrInterval = np.array(rrInterval)
        return f.exponentialAverager(np.copy(rrInterval), alpha)
        
    @staticmethod
    def intervalIrregularity(rrInterval, N=8, gamma=(0.03 if f.SECONDS else 30)):
        if not isinstance(rrInterval, np.ndarray): rrInterval = np.array(rrInterval)

        M = [(2/(N*(N-1))) * sum([
                                sum([
                                    (1 if abs((AFDetector.IDEAL_RR_INTERVAL if i-j<0 else rrInterval[i-j]) -
                                                (AFDetector.IDEAL_RR_INTERVAL if i-k<0 else rrInterval[i-k]))-gamma > 0 else 0) 
                                        for k in range(j+1, N)]) # I USE N INSTEAD OF N+1 THAT WAS TAKING THE Nth+1 VALUE
                            for j in range(0, N)]) 
            for i in range(0, len(rrInterval))]       
        
        return np.array(f.exponentialAverager(M))/np.array(AFDetector.estimationRRTrend(rrInterval))
            
    @staticmethod
    def bigeminySuppression(rrInterval, N=8):
        if not isinstance(rrInterval, np.ndarray): rrInterval = np.array(rrInterval)
        rm = AFDetector.ectopicBeatsFiltering(rrInterval)
        return f.exponentialAverager([(rm[i-N+1:i+1].sum() / sum([rrInterval[i-j]for j in range(0, N)]) -1)**2 for i in range(0, len(rrInterval))])


    @staticmethod
    def signalFusion(rrInterval, N=8, gamma=(0.03 if f.SECONDS else 30), delta=0.0004):
        It = AFDetector.intervalIrregularity(rrInterval, N, gamma)
        Bt = AFDetector.bigeminySuppression(rrInterval, N)
        return [It[i] if Bt[i]>=delta else Bt[i] for i in range(len(rrInterval))]
    
        
    @staticmethod
    def detectAF(rrInterval, eta=0.725):
        O = AFDetector.signalFusion(rrInterval)
        return [1 if x > eta else 0 for x in O]