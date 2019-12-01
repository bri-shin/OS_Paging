import os

def min_and_max(iterable):
    iterator = iter(iterable)

    # Assumes at least two items in iterator
    minim, maxim = sorted((next(iterator), next(iterator)))

    for item in iterator:
        if item < minim:
            minim = item
        elif item > maxim:
            maxim = item

    return (minim, maxim)

with open('random-numbers.txt', 'r') as f:
    values = (float(value_str) for line in f for value_str in line.split())
    minim, maxim = min_and_max(values)

print(maxim)

