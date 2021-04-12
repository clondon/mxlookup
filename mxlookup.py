#!python3.9
import logging
import dns.resolver # From DNS Pyhton module
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from dns.exception import DNSException
from logging import exception, raiseExceptions
from dns.exception import DNSException
from flanker.addresslib import address
import os
import sys



''' Set up path to site packages '''
sys.path.append("/Users/charles/myvenv/lib/python3.9/site-packages")
"""
Colours
"""
RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

"""
WAKE UP THIS IS EXCITING!!!!
1) Read a file of emails address
2) Pirnt the number of email addresses in the  file
2) Loop through the
"""


def email_check(mxitem):
    email_results = []
    # Split out host and domain name
  
    email_item = mxitem.strip()
    # print("Email name {}".format(email_item))
    # Check domain MX record
    # Lazily extract doamin name from the email items
    domain_name = email_item.split('@')[1]
    email_name = email_item.split('@')[0]

    
    try:
        # Test the email address
        for rdata in dns.resolver.resolve(domain_name, 'MX'): # rdata is false if mx record is not present.
            email_exist = True
    except DNSException:
        email_exist  = False 
    
    if email_exist:
        sys.stdout.write(GREEN)
        print("{} has MX record at {}".format(email_name, domain_name))
    else:
        sys.stdout.write(RED)
        print("Email {} does not have an MX record at {}".format(email_name, domain_name))
        
# Main code loop   
if __name__ == "__main__":
    # print("MX Lookup by Charles London")
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
  
    
    # Name of file containing delimited list of email addresses
    FILENAME = "domains.txt"
    # Full or relative path
    DIRNAME = "/Users/charles/python_proj/mxlookup/bin/"
    
    # Open files
    # Check if the path and file name are correct
    if os.path.exists(os.path.join(DIRNAME, FILENAME)):
        # print(os.path.join(DIRNAME, FILENAME))  Works!!!!
        # If the directory file and exits we can open the file and start reading lines
        items = open(os.path.join(DIRNAME, FILENAME))

        for item in items:
            
            # Add one emil address to the thread functions
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:  # controls threading
                executor.map(email_check(item))

    # File open failed - Check file, file name and location
    else:
        print("\nError\nFile \u0332{}\u0332 not found. Quitting...\n".format(FILENAME))
        exit()
    
    # Close the file
    items.close
    
    print("Finishing...")    
  

