import os
import re

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
