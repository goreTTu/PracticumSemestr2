from model_api.model_api_manager import get_other_file_by_self, ModelWrapper
from PIL import Image, ImageFilter
from io import BytesIO

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
arr_i = res[0].orig_img
img_res = Image.fromarray(arr_i[...,::-1])
img_res.show()
# res[0].show()
# print(res[0].boxes)