import wfdb
import wfdb.processing
import functions as f

class Signal:
    """
       Used to easily implement the algorithm and to organize the annotations. 
    """
    def __init__(self, filename):
        self.record = wfdb.rdrecord(filename)
        self.an = wfdb.rdann(filename, "atr")
        self.FS = self.an.fs

        rr = wfdb.processing.ann2rr(filename, "atr")
        meanrr = sum(rr)/len(rr)

        #I assume that if an rr is greather then 5*mean(rr) then it's an error.
        #The medianFilter would remove them in any case.
        #They are removed here manually to plot meaningfull graphs.
        self.rrIntervals = [(x if x<5*meanrr else meanrr)/self.FS * (1 if f.SECONDS else 1000) for x in rr] 

    def _showRecordValues(self):
        """
            wfdb.rdrecord returns an Any so it's difficult to see its values while developing.
        """
        for k, v in self.record.__dict__.items():
            print(k, v)

    def getBeats(self):
        return len(self.rrIntervals)

    def getDuration(self):
        return len(self.record.p_signal)/self.record.fs
    
    def getAFBeatsAnnotations(self):
        """
            Returns a list of AFAttacks one for each Atrial Fibrillation episode.
        """
        arrhythmias = [(b, t) for b, t in enumerate(self.an.aux_note) if t != '' and self.an.symbol[b]=='+']
        if arrhythmias[-1][1] != f.N: arrhythmias.append((self.an.ann_len, f.N)) #needed when the signal ends during an arrythmia
        return [AFAttack(arrhythmias[i][0], arrhythmias[i+1][0]) for i in range(len(arrhythmias)-1) if arrhythmias[i][1]==f.AF]
    
    def getAFLabels(self):
        labels = [0]*self.an.ann_len
        for attack in self.getAFBeatsAnnotations():
            labels[attack.start:attack.end] = [1]*(attack.duration())
        return labels

class AFAttack:
    """
        Rappresents an Atrial Fibrillation labeled episode.
    """
    def __init__(self, start, end):
        self.start=start
        self.end=end

    def duration(self):
        return self.end-self.start

    def __str__(self):
        return f"AF ({self.start},{self.end}) {self.duration()} beats"
    
    def __repr__(self):
        return self.__str__()