#!/usr/bin/env python3

import sys
import update_portfolio
import generate_summary

def run_production_pipeline():
    """
    Execute the combined production pipeline:
    1. Run ETL to update portfolio from update_portfolio.py
    2. Generate & display summary report from generate_summary.py
    """
    print("-"*50, file=sys.stderr)
    print("Starting Production Pipeline", file=sys.stderr)
    print("-"*50, file=sys.stderr)
    
    print("Step 1: Running ETL & Updating Portfolio", file=sys.stderr)
    update_portfolio.main()
    
    print("\nStep 2: Generating Summary Report", file=sys.stderr)
    generate_summary.main()
    
    #print("\n" + "-"*50, file=sys.stderr)
    print("Production Pipeline Complete", file=sys.stderr)
    #print("-"*50, file=sys.stderr)


if __name__ == "__main__":
    run_production_pipeline()