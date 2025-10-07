#!/usr/bin/env python3
import argparse
import random
import json

import spending

class Retirement():
    """
    Model a retirement portfolio over time.
    Assests are split between stocks and fixed-income
    """
    def __init__(self,
                 target_years : int,
                 initial_capital : int,
                 cash_rate: float,
                 cpi: float,
                 plan,
                 balance : int = 0.6):
        self.target_years = target_years
        self.initial_capital = initial_capital
        self.cash_rate = cash_rate
        self.cpi = cpi
        self.balance = balance
        self.spending = spending.VariableSpending(plan, cpi)
        
    def spending(self, year: int):
        #print(f"{year=}\tincome:{self.model.spend(year)}")
        return self.model.spend(year)

    def __str__(self):
        s=f"Initial Capital: {self.initial_capital}\n"
        s+=f"Cash Rate: {self.cash_rate}\n"
        s+=f"CPI: {self.cpi}\n"
        s+=f"Stock:Cash {(self.balance*100):.0f}:{(1-self.balance)*100:.0f}\n"
        s+=f"Plan:\n{self.spending}\n"
        return s.strip()
        
def run_model(model, growth_fn):
    """
    Use models for capital growth and income do determine the outcome of a retirement portfolio
    """
    wealth=[]
    capital = model.initial_capital
    year = 0
    while (capital > model.spending.spend(year)) and year < model.target_years:
        wealth.append(capital)
        capital = capital - model.spending.spend(year)
        capital = growth_fn(capital, year)
        year += 1
    return wealth
  
def monte_carlo(asx_data, model, trials = 10000):
    """
    Run many simulations of a retirement plan against various scenarios
    based on historic market and economic data
    """
    shortest_run = model.target_years
    successes=0
    total_final_wealth = 0
    for trial in range(trials):
        shuffled_data = make_random_data(asx_data)
        growth_fn = make_balanced_asx_fn(shuffled_data, model.balance, model.cash_rate)
        wealth = run_model(model, growth_fn)
        if success(wealth, model.target_years):
            successes +=1
            total_final_wealth += wealth[-1]
        else:
            shortest_run = len(wealth)
    cpi_growth = (1+model.cpi) ** model.target_years
    avg_wealth = total_final_wealth / trials
    print(f"Shortest run: {shortest_run}")
    print(f"{trials} runs complete. Average final wealth in successful runs was ${avg_wealth:.2f}")
    print(f"which is ${(avg_wealth/cpi_growth):.2f} in today's dollars")
    return successes/trials

def make_balanced_asx_fn(asx_data, balance, cash_rate):
    #balance between ASX and flat rate
    def balanced_asx_rate(capital, year=0):
        asx_return = asx_data[year]
        #print(f"{year=}\t{asx_return=}\t{capital=}")
        return (capital * (1 + asx_return) * balance) + (capital * (1 + cash_rate) * (1-balance))
    return balanced_asx_rate    

def load_asx_data(filename: str):
    asx_data = {}
    with open(filename, 'r') as datafile:
        for line in datafile.readlines():
            try:
                year, rise = line.split(' ')
                asx_data[int(year)] = float(rise)/100
            except ValueError:
                print(f"{line} is not in the format '<year> <percentage>'")
    return list(asx_data.values())

def success(wealth, years):
    #Success means we had money remining after 30 years
    return len(wealth) >= years

def make_random_data(d):
    data=d.copy()
    random.shuffle(data)
    return data

def parse_args():
    parser = argparse.ArgumentParser(description="Monte Carlo analysis of retirement plans")
    parser.add_argument('--filename', '-f', default='model.json', type=str)
    parser.add_argument('--stockfile', '-s', default='asx_history.txt', type=str)
    
    return parser.parse_args()

def display_parameters(args):
    print(f"Starting with ${args.capital} and spending ${args.income}")
    print(f"With a {(args.balance * 100):.0f}:{((1.0-args.balance)*100):.0f} stocks:cash split")
    print(f"and in interest rate of {args.interest}")

def read_config(filename: str):
    """
    Read the json file that defines the model and construct the model object we'll use to run the sim
    """
    with open(filename, 'r') as f:
        config = json.load(f)
    return config

def setup_model(config):
    plan=[]
    for elem in config['model']:
        plan.append((elem[0], elem[1]))
        
    retirement = Retirement(
        config['target_years'],
        config['capital'],
        float(config['cash_rate'])/100,
        float(config['cpi'])/100,
        plan,
        config['balance'])
    return retirement
    
def main():
    args = parse_args()
    config = read_config(args.filename)
    model = setup_model(config)
    print(model)
    asx_data = load_asx_data(args.stockfile)
    success_rate = monte_carlo(asx_data, model, config['num_runs'])
    print(f"Success rate is {success_rate * 100:.2f}")
        
if __name__=="__main__":
    main()
