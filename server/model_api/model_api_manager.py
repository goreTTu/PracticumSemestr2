from PIL import Image, ImageFilter
from io import BytesIO
from ultralytics import YOLO
import numpy as np
import cv2

class ModelWrapper:
    def __init__(self):
        pth_const = "model_api/last.pt"
        self.path_to_model = pth_const
        self.model_worker = YOLO(pth_const)

    def reload_model(self):
        self.model_worker = YOLO(self.path_to_model)

    def get_answer_model_by_image(self, img_path):
        results_model = self.model_worker(img_path)
        return results_model


def get_other_file_by_self(input_file, model_tmp, inp_ext, out_ext, inp_name="resized_example", out_name="out_img"):
    img = input_file.read()

    image = Image.open(BytesIO(img))
    input_file.close()
    resized_image = image.resize((416, 416))
    image.close()
    inp_file_name = 'model_dir/input_img/' + inp_name + inp_ext
    with open(inp_file_name, 'wb') as f:
        resized_image.save(f, format='png')
    
    out_file_name = 'model_dir/output_img/' + out_name + out_ext

    res_mod = model_tmp.get_answer_model_by_image(inp_file_name)
    res_mod = res_mod[0]
    results = res_mod

    arr_img_mod = results.orig_img
    boxes = results.boxes.xyxy.cpu().numpy().astype(np.int32)
    for box in boxes:
        color = (255, 0, 0)
        x1, y1, x2, y2 = box
        cv2.rectangle(arr_img_mod, (x1, y1), (x2, y2), color, 2)

    cv2.imwrite(out_file_name, arr_img_mod)

    binary_data = None
    with Image.open(out_file_name) as image_new:
        buffer_cont = BytesIO()
        image_new.save(buffer_cont, format='png')
        binary_data = buffer_cont.getvalue()
    return (BytesIO(binary_data), out_file_name)

