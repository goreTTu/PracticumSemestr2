from PIL import Image, ImageFilter
from io import BytesIO


def get_other_file_by_self(input_file, inp_name="resized_example.png", out_name="out_img.png"):
    img = input_file.read()

    image = Image.open(BytesIO(img))
    #resized_image = image.resize((300, 200))
    resized_image = image.rotate(180)#test
    inp_file_name = 'model_dir/input_img/' + inp_name
    with open(inp_file_name, 'wb') as f:
        resized_image.save(f, format='png')



    binary_data = None
    #out_file_name = 'model_dir/output_img/' + out_name#work variant
    out_file_name = inp_file_name#test
    with Image.open(out_file_name) as image_new:
        buffer_cont = BytesIO()
        image_new.save(buffer_cont, format='png')
        binary_data = buffer_cont.getvalue()
    #return (binary_data, out_file_name)
    return (BytesIO(binary_data), out_file_name)

