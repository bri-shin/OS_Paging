# The program is invoked with 6 command line arguments:

M = 0   # Machine size in words
P = 0   # Page size in words.
S = 0   # Size of each process, i.e., the references are to virtual addresses 0..S-1.
J = 0   # Job mix, which determines A, B, and C, as described below.
N = 0   # Number of references for each process.
R = ""  # Replacement algorithm, LIFO (NOT FIFO), RANDOM, or LRU.