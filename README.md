# SSH Honeypot Project

This SSH Honeypot emulates a vulnerable SSH server that attracts and monitors unauthorized access attempts, allowing for secure observation and analysis of malicious interactions. This tool uses `paramiko` for SSH protocol handling and provides a limited file system structure for intruders to interact with.

## Features

- **SSH Server Simulation:** Mimics a secure shell environment using the SSH protocol.
- **Authentication Simulation:** Valid credentials are `username: ironman` and `password: 12345`.
- **Basic Command Simulation:** Supports basic commands (`ls`, `cd`, etc.) and a virtual file structure.
- **Multi-threaded Connections:** Can handle multiple connections via threading.
- **Activity Logging:** Logs connection attempts, successful logins, and issued commands.

## File Structure

The honeypot has a minimal, simulated filesystem that allows users to interact with specific directories and files. Below is a summary of the root directory structure:
```plaintext
/                 # Root directory
├── bin           # Common command executables
├── home
│   └── ironmanabhi
│       ├── files 
│       └── directories (Desktop, Documents, Downloads, Music, Pictures, etc.)
├── lib32         
├── var           
└── other common system directories (etc, dev, tmp, usr, etc.)
```

## Setup Instructions

1. **Install Dependencies:**
   - This project requires `paramiko`. Install it with:
     ```bash
     pip install paramiko
     ```

2. **Generate or Provide an RSA Key:**
   - Place your RSA private key in the specified path or modify the `HOSTKEY` variable in the code to match your key location:
     ```python
     HOSTKEY = paramiko.RSAKey.from_private_key_file("/path/to/key")
     ```

3. **Run the Server:**
   - Start the SSH Honeypot by running:
     ```bash
     python honeypot.py
     ```
   - The server will listen on port `2222` for incoming SSH connections.

## Usage

- The SSH Honeypot accepts incoming SSH connections on the specified IP address and port (`0.0.0.0`, `2222` by default).
- Use SSH to connect and authenticate with the username and password (`ironman` and `12345`).
- Commands:
  - **`ls`**: Lists files in the `/home/ironmanabhi` directory.
  - **`cd <directory>`**: Allows navigation within `home/ironmanabhi` directories.
  - **Other commands**: Unsupported commands prompt a standard response.

## Project Structure

- **SSH Connection Handling**: The server listens for connections and sets up SSH channels using the `paramiko` library.
- **Authentication Management**: Credentials are validated, granting access upon successful authentication.
- **Command Emulation**: Common commands (`ls`, `cd`, etc.) are partially emulated to mimic a real shell environment.

## Example Output

```
{+} Listening for connection ...
{+} Got a connection! ('192.168.1.10', 23456)
{+} Authenticated!
$ ls
Desktop
Documents
Downloads

$ cd Desktop
Directory changed to Desktop

$ exit
Goodbye!
```

## Contributing

Feel free to contribute to this project by submitting issues or pull requests for new features, optimizations, or bug fixes.
