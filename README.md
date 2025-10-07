# retirement
A Monte Carlo model for retirement planning.
This program takes historical stock market data - as much as you can find,
together with parameters to model retirement spending.

usage: retirement.py [-h] [--filename FILENAME] [--stockfile
STOCKFILE]

where <FILENAME? is the JSON config file structured as
{
    "capital": 2400000,
    "target_years": 35,
    "cpi": 3.5,
    "cash_rate":3.5,
    "balance": 0.7,
    "stock_history_file": "asx_history.txt",
    "num_runs" : 10000,
    "model" : [
	[120000, 10],
	[100000, 10],
	[80000, 5],
	[120000, 10]]
}

and <STOCKFILE> is historical market data in the format
<Year1> <%growth>
<Year2> <%growth>

The program runs a Monte Carlo simulation by shuffling
stock returns and increasing the income by CPI each year.

Sample output:
Initial Capital: 2400000
Cash Rate: 0.035
CPI: 0.035
Stock:Cash 70:30
Plan:
$120000 for 10 years
$100000 for 10 years
$80000 for 5 years
$120000 for 10 years
Shortest run: 24
10000 runs complete. Average final wealth in successful runs was $19201653.42
which is $5760051.73 in today's dollars
Success rate is 88.25
