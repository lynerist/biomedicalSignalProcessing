from matplotlib import pyplot as plt 
from parameters import *

AF = "(AFIB"
N = "(N"

def plotSerie(names, rrIntervals):
    """
        To plot multiple signals with a single function.
    """
    for i, (name,r) in enumerate(zip(names, rrIntervals)):
        plt.subplot(len(rrIntervals), 1, i+1)
        if name == "Bt":
            plt.axhline(y=DELTA, color="red", linestyle=":", linewidth=0.5)
        if name == "O":
            plt.axhline(y=ETA, color="red", linestyle=":", linewidth=0.5)
        plt.title(name, x=-0.13, y=0.2)
        plt.plot(r, linewidth=0.3)
    plt.show()
    
def median3(a, b, c):
    if a>b: b,a=a,b
    return (b if c>b else (c if a<c else a))

def exponentialAverager(data, alpha=ALPHA):
    """
        Modifies also inplace, be carefull
    """
    for i in range(1, len(data)):
        data[i] = alpha*data[i]+ (1-alpha)*data[i-1]
    return data

def FBExponentialAverager(data, alpha=ALPHA):
    return exponentialAverager(exponentialAverager(data, alpha)[::-1],alpha)[::-1]

def checkTypeList(l):
    return l if isinstance(l, list) else list(l)
