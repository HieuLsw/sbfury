import os
from PySFML import sf

def load_image(filename):
    "Genera un objeto Image a partir de la ruta indicada."

    dirname = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(dirname, '..', 'data', filename)

    image = sf.Image()
    image.LoadFromFile(path)

    return image



