#!/usr/bin/env python3

"""
A model of spending in retirement
"""

import abc

class NoSpendingData(Exception):
    pass

#Abstract base
class Spending(abc.ABC):

    @abc.abstractmethod
    def spend(self, year):
        return 0

#Same every year
class LinearSpending(Spending):
    def __init__(self, annual_spend):
        self.annual_spend = annual_spend
    def spend(self, year):
        return self.annual_spend

"""
Models variable spending over time. 'plan' is a list of tuples of (<income>, <number_of_years>)
"""
class VariableSpending(Spending):
    def __init__(self, plan, cpi, extend_final = True):
        self.plan = plan
        self.extend_final = extend_final
        self.cpi = cpi

    def spend(self, year):
        remaining_year = year
        for entry in self.plan:
            if remaining_year < entry[1]:
                spending = entry[0]
                break
            else:
                remaining_year -= entry[1]
        else:
            if self.extend_final:
                spending = self.plan[-1][0]
            else:
                raise NoSpendingData(f"Model does not have data for spending in year {year}")

        # Apply CPI correctly based on absolute year
        spending = spending * ((1 + self.cpi) ** year)
        return spending
    
    def __str__(self):
        result = ""
        for entry in self.plan:
            result += f"${entry[0]} for {entry[1]} years\n"
        return result.strip()
        
import unittest

class LinearSpendingTestCase(unittest.TestCase):
    def testLinearSpending(self):
        spend = 100_000
        ls = LinearSpending(spend)
        self.assertEqual(ls.spend(0), spend)
        self.assertEqual(ls.spend(1), spend)
        self.assertEqual(ls.spend(2), spend)

    def testVariable(self):
        
        model = VariableSpending([(100_000, 1),
                                  (90_000, 2),
                                  (80_000, 3),
                                  (70_000, 1)])
        cases = [
            (0, 100_000),
            (1, 90_000),
            (2, 90_000),
            (3, 80_000),
            (6, 70_000),
            (100, 70_000),
            ]
        for year, expected in cases:
            self.assertEqual(model.spend(year), expected)

        non_extending_model = VariableSpending([(100_000,1), (150_000, 1)])
        self.assertEqual(non_extending_model.spend(1), 150_000)
        #self.assertRaises(NoSpendingData, non_extending_model.spend(2))
            
if __name__ == "__main__":
    unittest.main()
        
