import json

def export_to_gliffy_json(elements: dict, out_path: str):
    nodes = elements.get('nodes', [])
    edges = elements.get('edges', [])
    w,h = elements.get('image_size', (1024,768))

    doc = {
        'version': '1.0',
        'page': {
            'width': w,
            'height': h,
            'shapes': [],
            'connectors': []
        }
    }

    for n in nodes:
        x,y,w0,h0 = n['bbox']
        shape = {
            'id': n['id'],
            'type': 'rectangle',
            'x': x,
            'y': y,
            'width': w0,
            'height': h0,
            'text': n.get('label','')
        }
        doc['page']['shapes'].append(shape)

    for e in edges:
        src = e.get('source')
        tgt = e.get('target')
        conn = {
            'id': e['id'],
            'type': 'connector',
            'source': src,
            'target': tgt,
            'points': e.get('points', [])
        }
        doc['page']['connectors'].append(conn)

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(doc, f, indent=2)

    return out_path