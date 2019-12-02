# OS_Paging


*Operating System 2019 Fall*

*Author: Seung Heon Brian Shin*

## Program Background

Simulation of demand paging that determines number of page faults depending on page size, program size, replacement algorithm, and job mix.

#### This program is composed of:

- Process and Process Summary Class
- Frame and Frame Table Class
- Page Class
- Helper Components

## Program Specification

*Programming Language Used:* Python 3

## How to run this program

On the terminal, this program can be run by:

```bash
$ python3 run.py 10 10 20 1 10 lru 0
```

Refer below for sample inputs.

### Sample Inputs:

10 10 20 1 10 lru 0

10 10 10 1 100 lru 0
10 10 10 2 10 lru 0
20 10 10 2 10 lru 0
20 10 10 2 10 random 0
20 10 10 2 10 lifo 0
20 10 10 3 10 lru 0
20 10 10 3 10 lifo 0
20 10 10 4 10 lru 0
20 10 10 4 10 random 0
90 10 40 4 100 lru 0
40 10 90 1 100 lru 0
40 10 90 1 100 lifo 0
800 40 400 4 5000 lru 0
10 5 30 4 3 random 0
1000 40 400 4 5000 lifo 0
