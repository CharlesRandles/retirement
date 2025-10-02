# retirement
A Monte Carlo model for retirement planning.
This program takes historical stock market data - as much as you can find,
together with parameters to model retirement spending.

usage: retirement.py [-h] [--capital CAPITAL] [--income INCOME]
                     [--interest INTEREST] [--balance BALANCE]
                     [--filename FILENAME]

It takes your retirement capital, your desired flat income, 
the interest you will get on your non-stock portfolio, a balance between 0 and 1
indicating your stock: fixed income asset balance
and the name of the file containing historical market data in tho format
<Year1> <%growth>
<Year2> <%growth>

The program performs 10,000 Monte Carlo simulations and reports what percentage of them lasted 35 years.

Sample output:
./retirement.py -c 2300000 -b 0.75 -i 120000 -n 0.03
Starting with $2300000 and spending $120000
With a 75:25 stocks:cash split
and in interest rate of 0.03
10000 runs complete. Average final wealth in successful runs was 126787787.37
Success rate is 98.18
