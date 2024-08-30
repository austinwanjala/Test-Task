# Test-Task
# TCP String Search Server

A multithreaded TCP server that listens for incoming connections, receives a string, and checks if it exists as a standalone line in a specified file. The server supports SSL authentication and can be configured to re-read the file on each query.

## Features

- Handles unlimited concurrent connections using multithreading.
- Searches for exact matches of a string in a file.
- Configurable to re-read the file on each query.
- Supports SSL for secure communication.
- Detailed logging of queries and execution times.

## Requirements

- Python 3.x
- OpenSSL (for SSL support)

## Installation

### Step 1: Clone the Repository

git clone <repository-url>
cd <repository-directory>__


Step 2: Install Dependencies
Ensure you have Python 3 and the required libraries installed. You can install any missing dependencies using:
_sudo apt-get install python3 python3-ssl_

Step 3: Create Configuration File
Create a config.txt file in the same directory as the server script with the following format:

linuxpath=/path/to/your/file.txt
REREAD_ON_QUERY=True  # Set to False if the file does not change
SSL_ENABLED=True       # Set to False to disable SSL

Step 4: Generate SSL Certificates
To enable SSL, generate a self-signed certificate:
_openssl req -new -x509 -days 365 -keyout server.key -out server.crt_

Step 5: Run the Server
Start the server as a background process:
_nohup python3 server.py &_

The server will listen on port 9999 for incoming connections.
Usage
Once the server is running, you can connect to it using a TCP client. The client should send a string, and the server will respond with either:
STRING EXISTS\n if the string is found as a standalone line in the file.
STRING NOT FOUND\n if the string is not found.
