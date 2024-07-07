import argparse
import socket

def parse_ports(port_arg):
    if port_arg == '-':
        return range(1, 65536)
    else:
        try:
            min_port, max_port = map(int, port_arg.split('-'))
            if 1 <= min_port <= 65535 and 1 <= max_port <= 65535 and min_port <= max_port:
                return range(min_port, max_port + 1)
            else:
                raise ValueError
        except ValueError:
            raise argparse.ArgumentTypeError("Port range must be in the format min-max with values between 1 and 65535")

parser = argparse.ArgumentParser(description="Port scanner")
parser.add_argument('-p', required=True, type=parse_ports, help="Specify port range as min-max or use -p- to scan all ports (1-65535)")
parser.add_argument('target', type=str, help="Target IP address or hostname")

args = parser.parse_args()

target = args.target
ports_to_scan = args.p  

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        sock.settimeout(1)  
        result = sock.connect_ex((target, port))  
        sock.close()  
        return result == 0  
    except socket.timeout:  
        return False
    except socket.error:
        return False

def get_service_name(port):
    try:
        return socket.getservbyport(port) 
    except OSError:  
        return None

print(f"Scanning target {target}")

for port in ports_to_scan:
    if scan_port(target, port):
        service = get_service_name(port) if port <= 100 else None
        if service:
            print(f"Port {port} is open (Service: {service})")
        else:
            print(f"Port {port} is open")
    else:
        print(f"Port {port} is closed")