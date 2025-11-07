import cv2
import pytesseract
import uuid


def ocr_text(image):
config = '--psm 6'
text = pytesseract.image_to_string(image, config=config)
return text.strip()


def detect_contours(gray):
blur = cv2.GaussianBlur(gray, (5,5), 0)
th = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
close = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel, iterations=1)
contours, _ = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
return contours, close


def bbox_from_cnt(cnt):
x,y,w,h = cv2.boundingRect(cnt)
return (x,y,w,h)


def approx_shape(cnt):
peri = cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
return len(approx)


def is_arrow(cnt, img):
x,y,w,h = cv2.boundingRect(cnt)
aspect = max(w/h, h/w)
area = cv2.contourArea(cnt)
if area < 50:
return False
if aspect > 3.0 and min(w,h) < 40:
return True
if approx_shape(cnt) <= 4 and area < 2000:
return True
return False


def image_to_elements(img_path):
img_orig = cv2.imread(img_path)
if img_orig is None:
return None
h0, w0 = img_orig.shape[:2]
gray = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY)


contours, binary = detect_contours(gray)


nodes = []
edges = []


for cnt in contours:
x,y,w,h = bbox_from_cnt(cnt)
if w*h < 200:
continue
roi = img_orig[y:y+h, x:x+w]
if is_arrow(cnt, img_orig):
cx = x + w//2
cy = y + h//2
edges.append({
'id': 'e_'+str(uuid.uuid4())[:8],
'bbox': (x,y,w,h),
'points': [(cx,cy)]
})
else:
label = ocr_text(roi)
nodes.append({
'id': 'n_'+str(uuid.uuid4())[:8],
'bbox': (x,y,w,h),
'label': label
})


def center(b):
x,y,w,h = b
return (x + w//2, y + h//2)


node_centers = {n['id']: center(n['bbox']) for n in nodes}
for e in edges:
if 'points' not in e or len(e['points'])==0:
continue
px,py = e['points'][0]
dists = []
for nid, (nx,ny) in node_centers.items():
d = (nx-px)**2 + (ny-py)**2
dists.append((d,nid))
dists.sort()
if len(dists)>=2:
src = dists[0][1]
tgt = dists[1][1]
elif len(dists)==1:
src = tgt = dists[0][1]
else:
continue
e['source'] = src
e['target'] = tgt


return {'nodes': nodes, 'edges': edges, 'image_size': (w0,h0)}