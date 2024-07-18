#!/usr/bin/env python
# coding: utf-8

# In[7]:


import argparse
import logging

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("--s", "--start", type=int, required=True, help="Start value", default = 0)
    parser.add_argument("--e", "--end", type=int, required=True, help="End value")
    parser.add_argument("--v", "--verbose", action="store_true", help="Increase output verbosity")
    return parser

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    start: int = args.start
    end: int = args.end
    verbose: bool = args.verbose

    print(start, end, verbose)

