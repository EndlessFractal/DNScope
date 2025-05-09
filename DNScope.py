import concurrent.futures
import os
import socket
from time import sleep

import dns.resolver
from prettytable import PrettyTable
from tqdm import tqdm

# Change the working directory to the script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Function to check a given domain for subdomains.
def check_domain(domain, wordlist, workers=10):
    results = []
    resolver = dns.resolver.Resolver()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor, tqdm(total=len(wordlist), unit=" domains") as pbar:
        # Create a dictionary of futures to subdomains to be resolved
        future_to_domain = {executor.submit(check_subdomains, f"{subdomain}.{domain}", "", resolver): subdomain for subdomain in wordlist}
        for future in concurrent.futures.as_completed(future_to_domain):
            subdomain = future_to_domain[future]  # get the subdomain corresponding to this future
            try:
                results.extend(future.result())  # add the results of this future to the list of results
            # Handle keyboard interrupt
            except KeyboardInterrupt:
                print("\nKeyboard interrupt detected. Exiting...")
                exit()
            except:
                pass
            # Update progress bar
            pbar.update(1)
    return results

# Function to check subdomain for A and CNAME records.
def check_subdomains(domain, tld, resolver):
    full_domain = domain + "." + tld  # construct the full domain name
    results = set()  # set to store results (to remove duplicates)
    try:
        # Try to resolve A records
        a_records = resolver.resolve(full_domain, 'A')
        for a in a_records:
            # Add the domain name to the set of results
            results.add(full_domain)
        # Try to resolve CNAME records
        cname_records = resolver.resolve(full_domain, 'CNAME')
        for cname in cname_records:
            # Add the domain name to the set of results
            results.add(full_domain)
    except:
        # If resolution fails, do nothing
        pass
    # Return the set of results
    return results

# Function to check a domain for a specific subdomain
def perform_reverse_dns_lookup(subdomains_file_path, output_file_path, attempts=3):
    # Read the list of subdomains from a file
    with open(subdomains_file_path, 'r') as f:
        subdomains = [line.strip() for line in f]

    # Use concurrent.futures to perform reverse DNS lookups in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit each subdomain to the executor
        futures = [executor.submit(reverse_lookup, subdomain, attempts) for subdomain in subdomains]

        # Iterate over the completed futures and update the progress bar
        results = []
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            # Get the result of the future and append it to the list of results
            results.append(future.result())

    # Create an ASCII table with only vertical lines
    table = PrettyTable(["Subdomain", "IP Address"])
    table.hrules = 0
    table.vertical_char = "|"
    table.junction_char = "|"

    for subdomain, ip in results:
        if ip:
            table.add_row([subdomain, ip])
        else:
            table.add_row([subdomain, "not found"])

    # Save the ASCII table to a file
    with open(output_file_path, 'w') as f:
        f.write(str(table))

# Function to perform a reverse DNS lookup on a subdomain
def reverse_lookup(subdomain, attempts):
    for attempt in range(attempts):
        try:
            ip = socket.gethostbyname(subdomain)
            return subdomain, ip
        except socket.gaierror:
            # If the first attempt fails, try again up to 2 more times
            if attempt < attempts - 1:
                sleep(1)
                continue
            return subdomain, None

if __name__ == "__main__":
    print("""\
    ______ _   _  _____
    |  _  \ \ | |/  ___|
    | | | |  \| |\ `--.  ___ ___  _ __   ___
    | | | | . ` | `--. \/ __/ _ \| '_ \ / _ \\
    | |/ /| |\  |/\__/ / (_| (_) | |_) |  __/
    |___/ \_| \_/\____/ \___\___/| .__/ \___|
                                | |
    by NotoriusNeo              |_|          """)
    print("Wordlist Subdomain Finder & Reverse Lookup Tool")

    try:
        with open("wordlist.txt", "r") as f:
            # Read the list of subdomains from a file
            wordlist = f.read().splitlines()
    except FileNotFoundError:
        print("\n Wordlist not found!\n Please check if its in the same path as the Python file!")
        exit()

    try:
        domain = input("Enter domain to check: ")
    except KeyboardInterrupt:
            print("\n Exiting...")
            exit()
    
    # Call the check_domain function
    results = check_domain(domain, wordlist)
    if len(results) == 0:
        print("No subdomains found!")
    else:
        with open("subdomains.txt", "w") as f:
            # Remove duplicates and sort the list of subdomains
            for subdomain in sorted(set(results)):
                # Write each subdomain to a new line in the file
                f.write(f"{subdomain}\n")
        # Print the number of unique subdomains found and saved to the file
        print(f"{len(set(results))} unique subdomains found and saved to subdomains.txt!")

        valid_input = False
        while not valid_input:       
            answer = input("Would you like to perform a reverse lookup on the found subdomains [y]es/[n]o: ")
            if answer == "y":
                # Execute reverse DNS Lookup
                perform_reverse_dns_lookup('subdomains.txt', 'reverse_lookup.txt')
                print(f"\n Done!! Please check your files in {os.path.dirname(os.path.abspath(__file__))} !")
                valid_input = True
            elif answer == "n":
                # Exit code
                exit()
            else:
                # Error
                print("Invalid input.")

