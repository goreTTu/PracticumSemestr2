from flask import Flask, render_template, jsonify, request, make_response, redirect, send_file
from db_tools.db_manager_tools import DBManager
from model_api.model_api_manager import get_other_file_by_self
import json
from io import BytesIO


app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/', methods=['GET'])
def get_main_page():
    return render_template('main_index.html')


@app.route('/get_is_authorized_user', methods=['GET'])
def get_is_authorized():
    answer = {"is_auth" : False}
    if not request.cookies.get('logged'):
        return jsonify(answer)

    cookies_user = request.cookies.get('logged')

    if cookies_user == "yes":
        answer = {"is_auth" : True}
        return jsonify(answer)

    return jsonify(answer)



@app.route('/view_models', methods=['POST', 'GET'])
def get_all_models_page():

    if not request.cookies.get('logged'):
        return render_template('authorization.html')

    cookies_user = request.cookies.get('logged')

    if cookies_user == "no":
        return render_template('authorization.html')

    return render_template('find_of_models.html')

@app.route('/get_all_models', methods=['GET'])
def get_all_models_handler():
    all_models = ['WheatDetection', 'Example1', 'Example2']
    answer = {}

    my_db = DBManager()
    counter_mdl = 0
    for item in all_models:
        mdl_tmp = my_db.get_model_by_name(item)
        mdl_tmp = mdl_tmp[0]
        answer[counter_mdl] = {'name': mdl_tmp['modeltitle'], 'description': mdl_tmp['modeldescription']}
        counter_mdl += 1

    return jsonify(answer)

@app.route('/get_model_with_name', methods=['GET'])
def get_model_with_name_handler():
    name_m = request.args.get('name')

    if name_m != 'WheatDetection':
        return render_template('error_site.html')

    my_db = DBManager()
    mdl_tmp = my_db.get_model_by_name(name_m)
    mdl_tmp = mdl_tmp[0]

    resp = make_response(redirect('/target_model'))
    resp.set_cookie('model', mdl_tmp['modeltitle'])
    return resp

@app.route('/target_model', methods=['GET'])
def get_view_handler():
    return render_template('view_model.html')


@app.route('/info_by_self', methods=['GET'])
def get_info_by_self_handler():
    name_model_cookies = request.cookies.get('model')

    my_db = DBManager()
    mdl_tmp = my_db.get_model_by_name(name_model_cookies)
    mdl_tmp = mdl_tmp[0]

    model_desc = mdl_tmp['modeldescription']

    answer = {'name': name_model_cookies, 'description': model_desc}
    return jsonify(answer)

@app.route('/run_model', methods=['POST'])
def run_model_handler():
    name_user_cookies = request.cookies.get('user')
    name_model_cookies = request.cookies.get('model')
    my_db = DBManager()
    answer={"server_response":"error_model_execute"}

    file_img = request.files.get('imagedata')
    new_img = get_other_file_by_self(file_img)
    new_path = new_img[1]
    new_img = new_img[0]
    if new_img:
        cookies_user = request.cookies.get('user')
        cookies_model = request.cookies.get('model')
        meta_data = 'meta_data'
        result = my_db.insert_history_item(cookies_user, cookies_model, new_path, meta_data)
        if not result:
            answer["server_response"]="bad_sql"
            return jsonify(answer)
        att_name = cookies_user + cookies_model + "_result_img.png"
        return send_file(
            new_img,
            download_name=att_name,
            mimetype='image/png'
        )

    return jsonify(answer)


@app.route('/get_output_model_by_id_history', methods=['GET'])
def get_detail_output_history_handler():
    id_his = request.args.get('id_record')
    my_db = DBManager()
    mdl_tmp = my_db.get_history_item_by_item_id(id_his)

    new_img = mdl_tmp['imagebin']
    new_img = BytesIO(new_img)
    att_name = "_result_img.png"
    return send_file(
            new_img,
            download_name=att_name,
            mimetype='image/png'
        )


@app.route('/info_name_profile_self', methods=['GET'])
def get_info_name_handler():
    answer = {"name":"unknown"}
    cookies_name = request.cookies.get('user')
    answer["name"] = cookies_name
    return jsonify(answer)

@app.route('/get_all_history', methods=['GET'])
def get_all_history_handler():
    name_user_cookies = request.cookies.get('user')
    my_db = DBManager()
    mdl_tmp = my_db.get_user_by_name(name_user_cookies)
    mdl_tmp = mdl_tmp[0]
    user_id = mdl_tmp['userid']

    answer={}

    all_history_items = my_db.get_all_history_items_by_user_id(user_id)
    if len(all_history_items) == 0:
        return jsonify(answer)


    counter_mdl = 0
    for item in all_history_items:
        model_id = item['outermodelid']
        mdl_tmp = my_db.get_model_by_id(model_id)
        mdl_tmp = mdl_tmp[0]
        answer[str(counter_mdl)] = {'name': mdl_tmp['modeltitle'], 'id': item['hid']}
        counter_mdl += 1

    return jsonify(answer)


@app.route('/auth_page', methods=['GET'])
def get_auth_page():
    if request.cookies.get('logged'):
        cookies_user = request.cookies.get('logged')
        if cookies_user == "yes":
            return render_template('main_index.html')

    return render_template('authorization.html')


@app.route('/reg_page', methods=['GET'])
def get_reg_page():
    if request.cookies.get('logged'):
        cookies_user = request.cookies.get('logged')
        if cookies_user == "yes":
            return render_template('main_index.html')

    return render_template('registration.html')


@app.route('/profile', methods=['POST', 'GET'])
def get_profile_page():
    return render_template('profile.html')



@app.route('/execute_auth', methods=['POST'])
def execute_auth_handler():
    data = request.json
    u_name = data['name_u']
    u_pass = data['password_u']

    my_db = DBManager()
    usr_count = len(my_db.get_user_by_name_and_password(u_name, u_pass))

    if usr_count != 0:
        resp = make_response(redirect('/profile'))
        resp.set_cookie('logged', 'yes')
        resp.set_cookie('user', u_name)
        return resp

    answer = {"server_response" : 'not_exist_user'}
    return jsonify(answer)

@app.route('/execute_reg', methods=['POST'])
def execute_reg_handler():
    data = request.json
    u_name = data['name_u']
    u_pass = data['password_u']

    my_db = DBManager()
    usr_count = my_db.insert_user_if_not_exist(u_name, u_pass)

    if usr_count:
        resp = make_response(redirect('/profile'))
        resp.set_cookie('logged', 'yes')
        resp.set_cookie('user', u_name)
        return resp

    answer = {"server_response" : 'this_user_already_exist'}
    return jsonify(answer)


@app.route('/logout', methods=['GET'])
def logout_exec():

    cookies_user = request.cookies.get('logged')

    if cookies_user == "no":
        return render_template('main_index.html')

    resp = make_response(redirect('/'))
    resp.set_cookie('logged', 'no')
    return resp

if __name__ == '__main__':
    #'new_user', 'qwerty'
    my_db = DBManager()

    # my_db.create_db()
    # my_db.insert_model_by_name('WheatDetection', 'Model for recognizing wheat ears from an image', 'iti')
    # my_db.insert_model_by_name('Example1', 'Example1 description', 'iti')
    # my_db.insert_model_by_name('Example2', 'Example2 description', 'iti')
    app.run(debug=True)

