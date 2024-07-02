#rr length

SECONDS = True
IDEAL_RR_INTERVAL = 0.8 if SECONDS else 800

#detector parameters

ALPHA = 0.02
GAMMA = (0.03 if SECONDS else 30)
DELTA = 0.0002
WINDOWLEN = 8
ETA = 0.725