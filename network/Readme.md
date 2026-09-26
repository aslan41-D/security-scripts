# Port Scanner

A fast, multi-threaded TCP port scanner written in Python. It uses `socket` for connection attempts and `ThreadPoolExecutor` for concurrent scanning, making it significantly faster than a single-threaded approach.

## Features

- **Multi-threaded scanning** — scan thousands of ports in seconds using a configurable thread pool
- **Flexible port range** — specify any range from 1 to 65535 (e.g., `1-1024`)
- **Configurable timeout** — control how long to wait for each connection attempt
- **Graceful interrupt handling** — press `Ctrl+C` at any time to stop and see partial results
- **Input validation** — clear error messages for invalid IPs, port ranges, or thread counts
- **Sorted output** — open ports are displayed in ascending order
- **No external dependencies** — uses only the Python standard library

## Requirements

- Python 3.9 or higher (for `cancel_futures` support in `ThreadPoolExecutor`)

## Usage

```bash
python3 port_scanner.py -i <IP> -p <PORT_RANGE> [OPTIONS]
```

Examples
Scan the first 1024 ports on a local machine
```bash
python3 port_scanner.py -i 127.0.0.1 -p 1-1024
```
Scan a wider range with a shorter timeout and more threads
```bash
python3 port_scanner.py -i 192.168.1.1 -p 1-65535 -t 0.5 -w 200
```
Scan a domain name
```bash
python3 port_scanner.py -i scanme.nmap.org -p 20-100
```
Example Output
----------------------------------------
[+] Açık portlar: 22, 80, 443
Toplam 1024 port tarandı, 3 açık port bulundu.

## Disclaimer
### This tool is intended for educational purposes and authorized security testing only. Scanning systems without explicit permission is illegal and unethical. The author is not responsible for any misuse.

## License
### This project is provided as-is for learning and authorized testing purposes.
