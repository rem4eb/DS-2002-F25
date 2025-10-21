#!/usr/bin/env python3

import pandas as pd
import os
import sys


def generate_summary(portfolio_file):
    """
    Read the portfolio CSV and output a summary report with the
    most valuable card information.
    """
    # Check if portfolio file exists
    if not os.path.exists(portfolio_file):
        print(f"Error: Portfolio file '{portfolio_file}' not found.", file=sys.stderr)
        sys.exit(1)
    
    df = pd.read_csv(portfolio_file)
    
    # Check if DataFrame is empty
    if df.empty:
        print("Portfolio is empty. No data to summarize.")
        return
    
    # Calculate total portfolio value
    total_portfolio_value = df['card_market_value'].sum()
    
    # Find most valuable card
    most_valuable_idx = df['card_market_value'].idxmax()
    most_valuable_card = df.loc[most_valuable_idx]
    
    # Summary report
    print("\n" + "-"*50)
    print("PORTFOLIO SUMMARY")
    print("-"*50)
    print(f"Total Portfolio Value: ${total_portfolio_value:,.2f}")
    print(f"\nMost Valuable Card Attributes")
    print(f"Name: {most_valuable_card['card_name']}")
    print(f"ID: {most_valuable_card['index']}")
    print(f"Value: ${most_valuable_card['card_market_value']:,.2f}")
    print("-"*50 + "\n")


def main():
    generate_summary('card_portfolio.csv')


def test():
    generate_summary('test_card_portfolio.csv')


if __name__ == "__main__":
    test()