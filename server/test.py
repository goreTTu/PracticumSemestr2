from model_api.model_api_manager import get_other_file_by_self, ModelWrapper
from PIL import Image, ImageFilter
from io import BytesIO
import numpy as np
import cv2

def proccess_imgs():
    with Image.open('test_dir/inp_i.jpg') as test_i:
        test_i.load()
    
    resized_image = test_i.resize((416, 416))
    inp_file_name = 'test_dir/resiz_i.png'
    with open(inp_file_name, 'wb') as f:
        resized_image.save(f, format='png')

    return 'test_dir/resiz_i.png'


model = ModelWrapper()
# path_i = proccess_imgs()
# print(path_i)
res = model.get_answer_model_by_image('test_dir/resiz_i.png')
arr_i = res[0]
# print(arr_i)
results = arr_i
image = results.orig_img
# classes_names = results.names
# classes = results.boxes.cls.cpu().numpy()
boxes = results.boxes.xyxy.cpu().numpy().astype(np.int32)
# for class_id, box in zip(classes, boxes):
for box in boxes:
    color = (255, 0, 0)
    x1, y1, x2, y2 = box
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
cv2.imwrite("test_dir/test_img.png", image)
# cv2.imshow('Image with Bounding Boxes', image)
#img_res = Image.fromarray(arr_i[...,::-1])
#img_res.show()
# res[0].show()
# print(res[0].boxes)