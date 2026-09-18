# Log Reader

A simple Python CLI tool that parses web server access logs and counts requests per IP address. Useful for quick traffic analysis and identifying suspicious or high-frequency IPs during incident response.

## Features

- Parses any log file where the **first column is the IP address**
- Counts total requests per IP
- Filters results with a minimum request threshold (`--threshold`)
- Sorts output in descending order (most active IPs first)
- Lightweight — no external dependencies, uses only the Python standard library

## Requirements

- Python 3.x

## Usage

```bash
python3 log_reader.py <log_file> [--threshold <number>]
```

Example
Given a sample access.log file:


10.0.0.5 12/Jan/2026:13:45:12 GET /index.html 200 1024


10.0.0.5 12/Jan/2026:13:45:13 GET /about.html 200 2048


192.168.1.10 12/Jan/2026:13:46:01 GET / 200 1024


8.8.8.8  12/Jan/2026:13:49:00 GET / 200 1024


Run:

```bash
python3 log_reader.py access.log --threshold 2
Output:
```

IP : 10.0.0.5 => 2 requests

## License


## This project is for educational and authorized security testing purposes only.
