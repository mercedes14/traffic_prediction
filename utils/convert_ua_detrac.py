import json
import os
import os.path as osp
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

images = []
annotations = []
categories = [{'id': 0, 'name': 'car'}]

src = "."
image_path = osp.join(src,'images')
label_path = osp.join(src,'labels')

def parse_labels(label_file):
    tree = ET.parse(label_file)
    root = tree.getroot()
    frames = root.getchildren()
    frames = frames[2:]
    bboxes = {}
    for frame in frames:
        frame_num = frame.attrib['num']
        regions = frame.getchildren()[0].getchildren()
        all_bboxes = []
        for bbox in regions:
            data = bbox.getchildren()
            coords = data[0].attrib
            bbox = [float(coords['left']),
                            float(coords['top']),
                            float(coords['width']),
                            float(coords['height'])]
            all_bboxes.append(bbox)
        bboxes[frame_num] = all_bboxes
    return bboxes
                    
def convert_data():
    image_id = 0
    bbox_id = 0
    images_list = {x:osp.join(image_path, x) for x in os.listdir(image_path)}
    labels_list = {x.split('.')[0]: parse_labels(osp.join(label_path, x)) for x in os.listdir(label_path)}
    for sequence_name in images_list:
        print(f"parsing {sequence_name}")
        image_folder_path = images_list[sequence_name]
        image_files = [x for x in os.listdir(image_folder_path) if (x.endswith('.jpg') or x.endswith('.jpeg') or x.endswith('.png'))]
        for image_file in image_files:
            image = Image.open(osp.join(image_folder_path,image_file))
            width, height = image.size
            image_info = {
                'file_name':f"{sequence_name}_{image_file}",
                'width' : width,
                'height' : height,
                'id' : image_id
            }
            images.append(image_info)
            image_seq = image_file.split('.')[0].replace("img","")
            image_seq = str(int(image_seq))
            for bboxes in labels_list[sequence_name].get(image_seq,[]):
                annotation_info = {
                    'image_id' : image_id,
                    'bbox' : bboxes,
                    'id' : bbox_id,
                    'category_id' : 0
                }
                annotations.append(annotation_info)
                bbox_id += 1
            image_id += 1

convert_data()
result = {
    'images':images,
    'annotations':annotations,
    'categories':categories
}

with open('annotation.json','w') as fh:
    json.dump(result, fh)


# import os
# import os.path as osp
# import shutil
# src = "."
# image_path = osp.join(src,'images')

# images_list = {x:osp.join(image_path, x) for x in os.listdir(image_path)}
# for sequence_name in images_list:
#     image_folder_path = images_list[sequence_name]
#     image_files = [x for x in os.listdir(image_folder_path) if (x.endswith('.jpg') or x.endswith('.jpeg') or x.endswith('.png'))]
#     for image_file in image_files:
#         src_file = osp.join(image_folder_path,image_file)
#         dst_file = osp.join(src,"new_image_path",f"{sequence_name}_{image_file}")
#         shutil.move(src_file,dst_file)

# import json

# with open('annotations.json') as fh:
#     line = fh.readline()
#     data = json.loads(line)
    
# anno = data['annotations']
# for ann in anno:
#     ann['area'] = ann['bbox'][2] * ann['bbox'][3]

# data['annotations'] = anno
# with open('annotations_bak.json','w') as fh:
#     line = json.dumps(data)
#     fh.write(line)
    