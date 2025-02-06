import subprocess
import os


def allow_remote_port_linux(port):
    """Opens a port using firewall rules in Linux."""
    try:
        # Check if UFW is installed
        if subprocess.run(["which", "ufw"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
            subprocess.run(f"sudo ufw allow {port}/tcp", shell=True, check=True)
            print(f"Port {port} opened using UFW.")

        # Check if firewalld is installed
        elif subprocess.run(["which", "firewall-cmd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
            subprocess.run(f"sudo firewall-cmd --add-port={port}/tcp --permanent", shell=True, check=True)
            subprocess.run("sudo firewall-cmd --reload", shell=True, check=True)
            print(f"Port {port} opened using firewalld.")

        else:
            # Use iptables as fallback
            subprocess.run(f"sudo iptables -A INPUT -p tcp --dport {port} -j ACCEPT", shell=True, check=True)
            print(f"Port {port} opened using iptables.")

    except subprocess.CalledProcessError as e:
        print(f"Error opening port {port}: {e}")


# Define paths
# venv_path = "/home/user/project/venv/bin"  # Update with your actual virtual env path
# project_path = "/home/user/project"  # Update with your actual project path
script_name = "Server_Distribute_req.py"
ports = [6000, 6001, 6002, 6003, 6004, 6005]

for port in ports:
    allow_remote_port_linux(port)

    # Run the script in a new terminal window
    subprocess.Popen(
        f"gnome-terminal -- bash -c 'python {script_name} {port}; exec bash'",
        shell=True
    )


# ------------ for windoes

# import subprocess
#
# def allow_remote_port_windows(port):
#     command = (
#         f'netsh advfirewall firewall add rule name="Flask App {port}" '
#         f'dir=in action=allow protocol=TCP localport={port} remoteip=any'
#     )
#     subprocess.run(command, shell=True, check=True)
#
# # # #-- for server 130
# # venv_path = r'C:\Users\Administrator\SepehrSmart\SepehrSmart\.venv\Scripts'
# # project_path = r'C:\Users\Administrator\SepehrSmart\SepehrSmart'
#
#
# # # #-- for server 45
# venv_path = r'C:\Users\Administrator\PycharmProjects\web\vn\Scripts'
# project_path = r'C:\Users\Administrator\Desktop\SepehrSmart_services'
#
#
# #--Distribute_req (6000,6001,6002)
# script_name = 'Server_Distribute_req.py'
# ports = [6000, 6001, 6002,6003,6004,6005]
# for port in ports:
#     allow_remote_port_windows(port)
#     # subprocess.Popen(
#     #             f'start cmd /k "cd /d {venv_path} && activate && cd /d {project_path} && python {script_name} {port}"',
#     #                  shell=True)
#
#     #--- for server 185
#     subprocess.Popen(
#                 f'start cmd /k "python {script_name} {port}"',
#                      shell=True)
#
#
