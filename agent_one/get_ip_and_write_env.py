import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

with open('.env', 'w') as f:
    f.write(f"AGENT_HOST={get_ip()}\n")
    f.write("AGENT_PORT=8080\n")