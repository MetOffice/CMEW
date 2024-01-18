#!/usr/bin/env python
"""
Generates the request.json file from the ESMValTool recipe.

Generates the variables.txt file from the ESMValTool recipe.
"""
import os
from pathlib import Path

def extract_request() -> str:
    configure_standardise_path = Path(__file__).parent.parent
    with open(configure_standardise_path / "mock_data/request.json") as file:
        request = file.read()
    return request

def write_request(request: str):
    SHARE_DIR = os.environ["CYLC_WORKFLOW_SHARE_DIR"]
    with open(SHARE_DIR + "/etc/request.json", mode="w+") as file:
        file.write(request)
    return None

def main():
    request = extract_request()
    print(request)
    write_request(request=request)
    return None

if __name__ == "__main__":
    main()