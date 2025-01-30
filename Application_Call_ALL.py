


import subprocess

def allow_remote_port_windows(port):
    command = (
        f'netsh advfirewall firewall add rule name="Flask App {port}" '
        f'dir=in action=allow protocol=TCP localport={port} remoteip=any'
    )
    subprocess.run(command, shell=True, check=True)


# # Example: Allow ports 5001 and 5002
# allow_port_windows(5030)
# allow_port_windows(5031)

venv_path = r'C:\Users\Administrator\PycharmProjects\web\vn\Scripts'
project_path = r'C:\Users\Administrator\Desktop\SepehrSmart_services'


#--Booking Hotel (5002,5003)

script_name = 'Booking_Hotel_flask_OK.py'
ports = [5040,5041]
for port in ports:
    allow_remote_port_windows(port)
    subprocess.Popen(
                f'start cmd /k "cd /d {venv_path} && activate && cd /d {project_path} && python {script_name} {port}"',
                     shell=True)



#--- Jimboo Hotel (5020,5021)
script_name = 'Jimbo_Hotel_flask_OK.py'
ports = [5050,5051]
for port in ports:
    allow_remote_port_windows(port)
    subprocess.Popen(
        f'start cmd /k "cd /d {venv_path} && activate && cd /d {project_path} && python {script_name} {port}"',
        shell=True)




#---Booking Ready (5001,4010)

#----Jimboo ready (5030,5031)




#-- Alaedin


#--- Eghamat24
#--- Snapp

