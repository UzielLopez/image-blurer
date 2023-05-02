import os
import re
import subprocess

from PIL import Image



def getAllImages(imagesPath: str, app):
    if len(app.images) >= 40:
        print("Ya se han cargado todas las imagenes")
        return

    # Almacenamos el path de las imágenes nuevas que hemos reconocido.
    images = []
    for file in os.listdir(imagesPath):
        # Checamos que el file tenga la extensión de las imágenes que buscamos.
        if file.endswith(".bmp"):
            try:
                imagePath = imagesPath + "/" + file

                # Intentamos abrir la imagen; si no se abre es porque no posee ningún dato en el archivo.
                # Ante ello, entraremos en el except y omitiremos esta imagen porque sigue en construcción.
                Image.open(imagePath)

                # Evaluamos que la imagen reconocida no se encuentre en el arreglo existente de imágenes.
                if imagesPath not in app.images:
                    images.append(imagePath)
                    print("Añadiendo: " + imagePath)
                else:
                    print("La imagen ya se ha añadido a la app")
            except:
                print(file + " la imagen aun se encuentra en construcción")

    images.sort(key=lambda f: int(re.sub('\D', '', f)))
    app.images.extend(images)
    app.evaluateButtonsEnable()
    print("--------------------")

# @parameter masks : int -> número de máscaras que el usuario dijo que quería hacer
def check_cluster_status(masks: int):

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
    with open("machinefile", "w") as f:
        for node in available_nodes:
            node_name = registered_nodes[node]
            number_of_masks = load_distribution[node]
            f.write(f"{node_name} slots={number_of_masks} max_slots={number_of_masks}\n")