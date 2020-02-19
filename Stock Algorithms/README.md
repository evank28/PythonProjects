# Read Me for _STOCK ALGORITHMS_ directory
##### Author: Evan Kanter
### Purpose
This repository was created in an effort to make algorithmic stock picking 
decisions.
The algorithms in this repo are used by an investment group to 
trade _> $50 000 CAD_ in securities. 
### Repo Contents
This folder contains:
- `Momentumlist.py` &rarr; A Python script using Yahoo Finance to get a list of 
Quantiative Momentum stocks. This uses the _Quantitative Momentum_ strategy from the University of Chicago, as modified by Evan Kanter.
- `Momentumlist.md` &rarr; A markdown file with an explanation of the _Quantitative Momentum_ algorithm used in
 `Momentumlist.py`
- `Momentumlist_withTiemSeriesEOD.py` &rarr; A n attempt in Python attempt 
at `Momentumlist.py`, but using the quandl library
    - Without a paid license, this failed
- `Russell1k.py` &rarr; A script that ownloads a list of Russel1k stocks from 
Wikipedia
- `SandP.py` &rarr; A script that downloads a list of S&P 500 stocks. 
Not written by Evan Kanter.





\
\
&copy; Evan Kanter 2020
