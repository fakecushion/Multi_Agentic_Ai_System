import os
import json
from datetime import datetime

def test_logging():
    """Test that logging works correctly"""
    # Check if log file exists
    log_file = "logs/system_logs.json"
    
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            logs = json.load(f)
            print(f"Found {len(logs)} log entries")
            
            # Print the first log entry if it exists
            if logs:
                first_log = logs[0]
                print("First log entry:")
                print(json.dumps(first_log, indent=2))
    else:
        print("No log file found")

if __name__ == "__main__":
    test_logging()