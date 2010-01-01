import os
from PySFML import sf
import sheet

def load_image(filename):
    "Genera un objeto Image a partir de la ruta indicada."

    dirname = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(dirname, '..', 'data', filename)

    image = sf.Image()
    image.LoadFromFile(path)

    return image



def load_sheet(filename, cols=1, rows=1):
    image = load_image(filename)
    image_sheet = sheet.ImageSheet(image, cols, rows)
    return image_sheet
