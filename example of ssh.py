ssh smartland@mqtt.angizehco.com -p 2858

ssh root@185.252.28.42 -p 22
qwaszx!!11


udo netstat -tulnp | grep 6000
sudo kill -9 <PID>

#
# #----
#  # install all libraries
#
#
# Define servers and ports
# servers = [
#     ("mqtt.angizehco.com", [6000, 6001, 6002, 6003, 6004, 6005]),
#     ("45.149.76.168", [6000, 6001, 6002, 6003, 6004, 6005]),
#     ("130.185.77.24", [6000, 6001, 6002, 6003, 6004, 6005]),
# ]


# # Create a dictionary where each port is associated with its server:port combinations
# server_port_by_port = {
#     port: [f"{server}:{port}" for server, ports in servers if port in ports]
#     for port in set(port for _, ports in servers for port in ports)
# }
#
# # Print the result
# for port, server_ports in server_port_by_port.items():
#     print(f"Port {port}: {', '.join(server_ports)}")
# #
#
#
# # Create a list of server:port combinations for each port
# server_port_list = [
#     f"{server}:{port}"
#     for port in set(port for _, ports in servers for port in ports)
#     for server, ports in servers if port in ports
# ]
#
# # Print the result
# print(server_port_list)
#
# from itertools import cycle
#
# # Create a round-robin cycle from the list
# server_cycle = cycle(server_port_list)
#
# # Function to get the next item in a round-robin manner
# def next_server():
#     return next(server_cycle)
#
# for i in range(0,100):
#     # print(next_server())
#     server_ip, server_port=next_server().split(':')
#     print(f'{server_ip}:{server_port}')
#
#
#
#



#
# # # Swap the keys and values
# # swapped_servers = [
# #     (port, server)
# #     for server, ports in servers
# #     for port in ports
# # ]
# from itertools import cycle
#
# # Create a round-robin cycle for all server:port combinations
# server_cycle = cycle(
#     (server, port)
#     for server, ports in servers
#     for port in ports
# )
#
# # Function to get the next IP:port
# def next_IPport():
#     server_ip, server_port = next(server_cycle)
#     return server_ip, server_port
#
# for i in range(0,100):
#     server_ip, server_port=next_IPport()
#     print(f'{server_ip}:{server_port}')
# Create the round-robin iterator for all the servers and ports
#
# # Create a round-robin cycle for each port
# server_cycle_by_port = {
#     port: cycle(
#         (server, port) for server, ports in servers if port in ports
#     )
#     for port in set(port for _, ports in servers for port in ports)
# }
#
# # Function to get the next IP:port
# def next_IPport():
#     for port in server_cycle_by_port:
#         # Get the next combination for this port and return it
#         server_ip, server_port = next(server_cycle_by_port[port])
#         return server_ip, server_port
#
#
# for i in range(0,100):
#     server_ip, server_port=next_IPport()
#     print(f'{server_ip}:{server_port}')