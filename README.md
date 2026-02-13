# Splctl: Splunk Installation Automation Tool

## Overview
Splctl is a Python-based command-line utility designed to automate the installation and configuration of Splunk Universal Forwarder. It simplifies the process of downloading, extracting, and setting up Splunk, while ensuring best practices for user and directory management.

## Features
- **Automated Splunk Installation**: Supports online, local, and URL-based installation methods.
- **User and Group Management**: Creates and verifies Splunk-specific users and groups.
- **Environment Configuration**: Sets up environment variables for Splunk.
- **App Management**: Extracts and installs Splunk apps.
- **Service Management**: Enables Splunk to start at boot and manages its service lifecycle.
- **Logging**: Comprehensive logging for all operations.

## Requirements
- Python 3.8+
- Dependencies listed in `requirements.txt`:
  - BeautifulSoup4
  - Certifi
  - Charset-Normalizer
  - IDNA
  - Requests
  - Soupsieve
  - Types-Requests
  - Typing-Extensions
  - Urllib3

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/mromanode/splctl.git
   cd splctl
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the tool with the following options:

```bash
python splctl.py [OPTIONS]
```

### Options
- `-u, --user`: Specify the least privilege user (default: `splunkfwd`).
- `-g, --group`: Specify the user group (default: `splunkfwd`).
- `-a, --apps`: List of apps to import.
- `-m, --method`: Installation method (`online`, `local`, `url`).
- `-t, --tar`: Path to the Splunk tar archive (required for `local` method).
- `--url`: URL for Splunk tarball (required for `url` method).
- `-s, --start`: Start Splunk service after installation (`yes` or `no`, default: `yes`).
- `-d, --directory`: Target installation directory (default: `/opt`).

### Example Commands
1. **Online Installation**:
   ```bash
   python splctl.py -m online -a app1 app2
2. **Installation with local apps**:
   ```bash
   python splctl.py -m online -a app1 app2
   ```
3. **Local Installation**:
   ```bash
   python splctl.py -m local -t /path/to/splunk.tgz
   ```
4. **URL Installation**:
   ```bash
   python splctl.py -m url --url https://example.com/splunk.tgz
   ```

## File Structure
- `splctl.py`: Main entry point for the tool.
- `args_config.py`: Handles command-line argument parsing.
- `logging_config.py`: Configures logging for the application.
- `os_operations.py`: Provides OS-level operations (user, directory, and file management).
- `web_requests.py`: Handles HTTP requests and file downloads.
- `requirements.txt`: Lists Python dependencies.
- `LICENSE`: MIT License.

## Logging
Logs are stored in `splctl.log` and include detailed information about each operation, including errors and debug messages.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## Author
Marco Romano, 2026.

## Roadmap
- **Uninstall**: Add functionality to automate the uninstallation of Splunk Universal Forwarder, including user and directory cleanup.
- **Cross-Platform Support**: Extend compatibility to other operating systems like macOS and Windows.
- **Installation with apps from Splunkbase**: At the moment, the script support apps locally.