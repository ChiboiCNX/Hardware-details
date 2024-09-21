import socket
import platform
import psutil


def get_local_ip():
    """Get the local IP address of the machine."""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except Exception as e:
        return f"Unable to get IP address: {e}"
    
# print(get_local_ip())

def get_system_info():
    """Gather system hardware information."""
    sys_info = {
        "Platform": platform.system(),
        "Platform Version": platform.version(),
        "Platform Release": platform.release(),
        "Architecture": platform.machine(),
        "Processor": platform.processor(),
        "CPU Cores": psutil.cpu_count(logical=False),
        "Logical CPUs": psutil.cpu_count(logical=True),
        "Memory": f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB",
        "Disk Usage": {}
    }
    
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            sys_info["Disk Usage"][partition.mountpoint] = {
                "Total": f"{round(usage.total / (1024 ** 3), 2)} GB",
                "Used": f"{round(usage.used / (1024 ** 3), 2)} GB",
                "Free": f"{round(usage.free / (1024 ** 3), 2)} GB"
            }
        except PermissionError:
            # Handle partitions where we may not have access
            sys_info["Disk Usage"][partition.mountpoint] = "Access denied"
    
    return sys_info

# print(get_system_info())


def display_system_info():
    """Display the gathered system information."""
    print("Gathering system information...\n")
    
    # Display IP address
    local_ip = get_local_ip()
    print(f"Local IP Address: {local_ip}\n")

    # Display system information
    sys_info = get_system_info()
    
    print("System Information:")
    for key, value in sys_info.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for subkey, subvalue in value.items():
                print(f"    {subkey}: {subvalue}")
        else:
            print(f"  {key}: {value}")

if __name__ == "__main__":
    display_system_info()