# DNScope

DNScope is a Python script designed to simplify DNS subdomain enumeration and reverse lookup. It provides the following features:

- Parallel subdomain checking using a supplied wordlist.
- Progress bars to track the progress of the enumeration process.
- Output of results to files.

## Installation

1. Clone the repository using the following command:

   ```shell
   git clone https://github.com/NotoriusNeo/DNScope
   ```

2. Navigate to the cloned directory:

   ```shell
   cd DNScope
   ```

3. Install the required dependencies by running:

   ```shell
   pip install -r requirements.txt
   ```

## Usage

Run the script using the following command:

```
python3 DNScope.py
```

**Note:** The script was built with Python 3.11 in mind, but it may work with other Python versions as well.

## Workflow

1. The script will prompt you to provide a domain to perform DNS subdomain enumeration on.

2. You need to have a wordlist file containing a list of subdomains to check. The file should be named `wordlist.txt` and placed in the same directory as the script.

3. The script will initiate the parallel subdomain checking process using the provided wordlist. Progress bars will be displayed to track the progress of the enumeration.

4. Once the subdomain enumeration is complete, the script will save the results to a file named `<timestamp>_subdomains_<domain>.txt`, where `<timestamp>` represents the current date and time, and `<domain>` represents the domain name.

5. The script will then prompt you if you want to perform a reverse DNS lookup on the found subdomains.

6. If you choose to proceed with the reverse DNS lookup, the script will initiate the process and display progress bars.

7. The results of the reverse DNS lookup will be saved to a file named `<timestamp>_reverselookup_<domain>.txt`.

8. The script will display a message indicating the completion of the process and provide the path to the generated files.

## Note

DNScope simplifies the DNS subdomain enumeration and reverse lookup process by providing parallel checking and progress tracking. It relies on a wordlist for subdomain enumeration and utilizes external libraries to facilitate the process.

**Disclaimer:**
Please use DNScope responsibly and in compliance with ethical hacking guidelines. The script is provided as-is without any warranty. The developer is not responsible for any misuse or damage caused by the script.
