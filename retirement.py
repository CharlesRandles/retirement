#!/usr/bin/env python3
import argparse
import random

TARGET_YEARS=35 #Numvber of years before cash runs out

class Retirement():
    def __init__(self,
                 initial_capital,
                 income,
                 flat_rate,
                 balance = 0.6):
        self.initial_capital = initial_capital
        self.income = income
        self.flat_rate = flat_rate
        self.balance = balance
        
def run_model(model, growth_fn):
    wealth=[]
    MAX_YEAR=50 # never run for more than this long
    capital = model.initial_capital
    year = 0
    while (capital > model.income) and year < MAX_YEAR:
        capital = capital - model.income
        capital = growth_fn(capital, year)
        wealth.append(capital)
        year += 1

    return wealth

def make_constant_rate_fn(rate, year=None):
    def constant_rate(capital):
        return capital * (1.0 + rate)
    return constant_rate

def make_balanced_asx_fn(asx_data, balance,flat_rate):
    #balance between ASX and flat rate
    def balanced_asx_rate(capital, year=0):
        asx_return = asx_data[year]
        #print(f"{year=}\t{asx_return=}\t{capital=}")
        return (capital * (1 + asx_return) * balance) + (capital * (1 + flat_rate) * (1-balance))
    return balanced_asx_rate    

def load_asx_data(filename):
    asx_data = {}
    with open(filename, 'r') as datafile:
        for line in datafile.readlines():
            try:
                year, rise = line.split(' ')
                asx_data[int(year)] = float(rise)/100
            except ValueError:
                print(f"{line} is not in the format '<year> <percentage>'")
    return list(asx_data.values())

def success(wealth):
    #Success means we had money remining after 30 years
    return len(wealth) >= TARGET_YEARS
    
def monte_carlo(asx_data, model, num_trials = 10000):
    trials = 0
    successes=0
    total_final_wealth = 0
    for trial in range(num_trials):
        trials += 1
        shuffled_data = make_random_data(asx_data)
        growth_fn = make_balanced_asx_fn(shuffled_data, model.balance, model.flat_rate)
        wealth = run_model(model, growth_fn)
        if success(wealth):
            successes +=1
            total_final_wealth += wealth[-1]
    print(f"{trials} runs complete. Average final wealth in successful runs was {(total_final_wealth / trials):.2f}")
    return successes/trials

def make_random_data(d):
    data=d.copy()
    random.shuffle(data)
    return data

def parse_args():
    parser = argparse.ArgumentParser(description="Monte Carlo analysis of retirement plans")
    parser.add_argument('--capital', '-c', default = 2500000, type=int)
    parser.add_argument('--income', '-i', default=120000, type=int)
    parser.add_argument('--interest', '-n', default=0.03, type=float)
    parser.add_argument('--balance', '-b', default=0.8, type=float)
    parser.add_argument('--filename', '-f', default='asx_history.txt', type=str)
    
    return parser.parse_args()

def display_parameters(args):
    print(f"Starting with ${args.capital} and spending ${args.income}")
    print(f"With a {(args.balance * 100):.0f}:{((1.0-args.balance)*100):.0f} stocks:cash split")
    print(f"and in interest rate of {args.interest}")
def main():
    args = parse_args()
    display_parameters(args)
    
    asx_file = args.filename
    asx_data = load_asx_data(asx_file)
    initial_capital = args.capital
    draw = args.income
    flat_rate = args.interest #Blended return on cash/bonds
    balance = args.balance #Split between ASX tracker and cash/bonds

    model = Retirement(initial_capital,
                       draw,
                       flat_rate,
                       balance)
    success_rate = monte_carlo(asx_data, model)
    print(f"Success rate is {success_rate * 100:.2f}")
        

if __name__=="__main__":
    main()
