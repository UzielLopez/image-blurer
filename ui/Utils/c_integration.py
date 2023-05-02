import re
import subprocess

# @parameter masks : int -> número de máscaras que el usuario dijo que quería hacer
# @returns int -> número de hosts disponibles
def check_cluster_status(masks: int) -> int:

    # 1. Get hosts from /etc/hosts
    try:
        with open("/etc/hosts", 'r') as f:
            
            registered_nodes = {}
            for line in f:
                if "ub" in line:
                    node_name = line.strip().split()[-1]
                    ip = re.search(r'\d+\.\d+\.\d+\.\d+', line).group(0)
                    registered_nodes[ip] = node_name

    except IOError:
        print("Could not read file /etc/hosts")

    if(len(registered_nodes) == 0):
        return 0
    # 2. Execute command fping -g {node_ip_1} {node_ip_2} {node_ip_...n}
    
    command_arguments = " ".join(registered_nodes.keys())
    nodes_check_command = f"fping " + command_arguments
    nodes_check_result = subprocess.run(nodes_check_command, shell=True, capture_output=True, text=True)

    # 3. Save all hosts that returned "is alive"
    available_nodes = set()
    status_per_node = nodes_check_result.stdout.split("\n")
    for status in status_per_node:
        if "is alive" in status:
            ip = re.search(r'\d+\.\d+\.\d+\.\d+', status).group(0)
            available_nodes.add(ip)
    
    # 4. Distribute load between nodes
    masks_per_node = masks // len(available_nodes)
    uneven = (masks % len(available_nodes) != 0)

    load_distribution = {}
    for n, node in enumerate(available_nodes):
        # TODO: en este paso se puede poner lógica extra para distribuir el trabajo conforme
        # las capacidades de cada sistema. Necesitamos un archivo extra que contenga esta info tho
        load_distribution[node] = masks_per_node
        if uneven and n == len(available_nodes) - 1:
            load_distribution[node] = load_distribution[node] + 1

    # 5. Update machinefile with all alive hosts
    with open("machinefile", "w") as f: #TODO: change depending on relative path
        for node in available_nodes:
            node_name = registered_nodes[node]
            number_of_masks = load_distribution[node]
            f.write(f"{node_name} slots={number_of_masks} max_slots={number_of_masks}\n")

    return len(available_nodes)