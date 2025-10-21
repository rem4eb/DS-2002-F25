#!/usr/bin/env python3

import pandas as pd
import json
import os
import sys


def _load_lookup_data(lookup_dir):
    """
    Load and process JSON price data from the lookup directory.
    Returns a DataFrame with card details and market values.
    """
    all_lookup_df = []
    
    # Iterate over all JSON files in the lookup directory
    for filename in os.listdir(lookup_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(lookup_dir, filename)
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Flatten JSON
            df = pd.json_normalize(data['data'])
            
            # Price calculation
            df['card_market_value'] = df.get('tcgplayer.prices.holofoil.market', 0.0).fillna(
                df.get('tcgplayer.prices.normal.market', 0.0)
            ).fillna(0.0)
            
            # Standardize names
            df = df.rename(columns={
                'id': 'card_id',
                'name': 'card_name',
                'number': 'card_number',
                'set.id': 'set_id',
                'set.name': 'set_name'
            })
            
            required_cols = ['card_id', 'card_name', 'card_number', 'set_id', 'set_name', 'card_market_value']
            all_lookup_df.append(df[required_cols].copy())
    
    # Concatenate all DataFrames
    lookup_df = pd.concat(all_lookup_df, ignore_index=True)
    
    # Sort by market value; remove duplicates; keep highest value
    lookup_df = lookup_df.sort_values('card_market_value', ascending=False)
    lookup_df = lookup_df.drop_duplicates(subset=['card_id'], keep='first')
    
    return lookup_df


def _load_inventory_data(inventory_dir):
    """
    Load and process CSV inventory data from the inventory directory.
    Returns a DataFrame with inventory details including a unified card_id.
    """
    inventory_data = []
    
    # Iterate over all CSV files 
    for filename in os.listdir(inventory_dir):
        if filename.endswith('.csv'):
            filepath = os.path.join(inventory_dir, filename)
            
            df = pd.read_csv(filepath)
            inventory_data.append(df)
    
    # Check if empty
    if not inventory_data:
        return pd.DataFrame()
    
    inventory_df = pd.concat(inventory_data, ignore_index=True)
    inventory_df['card_id'] = inventory_df['set_id'].astype(str) + '-' + inventory_df['card_number'].astype(str)
    
    return inventory_df


def update_portfolio(inventory_dir, lookup_dir, output_file):
    """
    Main ETL function that loads inventory and lookup data, merges them,
    and outputs the final portfolio CSV.
    """

    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)
    
    # Create CSV if empty inventory data
    if inventory_df.empty:
        print("Error: No inventory data found.", file=sys.stderr)
        # Create empty portfolio CSV with required headers
        empty_df = pd.DataFrame(columns=['card_name', 'set_name', 'card_market_value', 'index'])
        empty_df.to_csv(output_file, index=False)
        return
    
    # Merge inventory with lookup data
    inventory_cols = [col for col in inventory_df.columns if col != 'card_name']
    portfolio_df = pd.merge(
        inventory_df[inventory_cols],
        lookup_df[['card_id', 'card_name', 'set_name', 'card_market_value']],
        on='card_id',
        how='left'
    )
    
    # Final cleaning
    portfolio_df['card_market_value'] = portfolio_df['card_market_value'].fillna(0.0)
    portfolio_df['set_name'] = portfolio_df['set_name'].fillna('NOT_FOUND')
    
    # Location index column
    portfolio_df['index'] = (
        portfolio_df['binder_name'].astype(str) + '-' +
        portfolio_df['page_number'].astype(str) + '-' +
        portfolio_df['slot_number'].astype(str)
    )
    
    final_cols = ['card_id', 'card_name', 'set_name', 'card_market_value', 'index']
    portfolio_df[final_cols].to_csv(output_file, index=False)
    
    print(f"Success: Portfolio written to {output_file}")


def main():
    update_portfolio(
        inventory_dir='./card_inventory/',
        lookup_dir='./card_set_lookup/',
        output_file='card_portfolio.csv'
    )


def test():
    update_portfolio(
        inventory_dir='./card_inventory_test/',
        lookup_dir='./card_set_lookup_test/',
        output_file='test_card_portfolio.csv'
    )


if __name__ == "__main__":
    print("Starting in Test Mode:", file=sys.stderr)
    test()