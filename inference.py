import os
from cv_helpers import image_to_elements
from gliffy_exporter import export_to_gliffy_json

OUTPUT_DIR = 'uploads'

def process_image_to_gliffy(image_path: str) -> str:
    elements = image_to_elements(image_path)
    if elements is None:
        return None
    filename = os.path.basename(image_path)
    name, _ = os.path.splitext(filename)
    out_path = os.path.join(OUTPUT_DIR, name + '_gliffy.json')
    export_to_gliffy_json(elements, out_path)
    return out_path