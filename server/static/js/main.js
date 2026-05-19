
let help_is_main_page = document.querySelectorAll('.main_container_button');
var is_main_page = false;
if (help_is_main_page.length > 0) {
    is_main_page = true;
}

let help_is_reg_page = document.querySelectorAll('.auth_reg_form_send_reg');
var is_reg_page = false;
if (help_is_reg_page.length > 0) {
    is_reg_page = true;
}

let help_is_authoriz_page = document.querySelectorAll('.auth_reg_form_send_auth');
var is_authoriz_page = false;
if (help_is_authoriz_page.length > 0) {
    is_authoriz_page = true;
}

let help_is_find_of_models_page = document.querySelectorAll('.find_of_models_page_tag');
var is_find_of_models_page = false;
if (help_is_find_of_models_page.length > 0) {
    is_find_of_models_page = true;
}


let help_is_view_model_page = document.querySelectorAll('.main_container_input_sector_send');
var is_view_model_page = false;
if (help_is_view_model_page.length > 0) {
    is_view_model_page = true;
}

let help_is_profile_page = document.querySelectorAll('.profile_clear_history');
var is_profile_page = false;
if (help_is_profile_page.length > 0) {
    is_profile_page = true;
}



function clear_menu(){
    const auth_elems = document.querySelectorAll('.auth_no');
    const profile_elems = document.querySelectorAll('.auth_accept');

    for (let i = 0; i < profile_elems.length; i++)
    {
        profile_elems[i].classList.remove('hide');
    }
    for (let i = 0; i < auth_elems.length; i++)
    {
        auth_elems[i].classList.remove('hide');
    }
}





async function init_menu_fetch(){
    return fetch('http://127.0.0.1:5000/get_is_authorized_user')
    .then(response => {
        if (!response.ok) {
            throw new Error('Http error');
        }
        return response.json();
    })
    .then(data => {
        const data_normal_obj = data;
        if(data_normal_obj.is_auth){
            return true
        }
        else{
            return false
        }
    })
    .catch(error => {console.error('Error with execute request', error);  return false});
}



async function init_menu(){
    const auth_elems = document.querySelectorAll('.auth_no');
    const profile_elems = document.querySelectorAll('.auth_accept');

    const a_bool = await init_menu_fetch();


    console.log(a_bool);

    if(a_bool)
    {
        for (let i = 0; i < auth_elems.length; i++)
        {
            auth_elems[i].classList.add('hide');
        }
        for (let i = 0; i < profile_elems.length; i++)
        {
            profile_elems[i].classList.remove('hide');
        }
    }
    else
    {
        for (let i = 0; i < profile_elems.length; i++)
        {
            profile_elems[i].classList.add('hide');
        }
        for (let i = 0; i < auth_elems.length; i++)
        {
            auth_elems[i].classList.remove('hide');
        }
    }

};


window.onload = function(){
    clear_menu();
    init_menu();
    builder_handlers();
}




//authorized and registration

function hide_auth_reg_error_field(){
    const error_field_el = document.querySelectorAll('.error_field_auth_reg');
    const error_field = error_field_el[0];
    error_field.classList.add('hide');
}

function show_auth_reg_field_error(type_error)
{
    const error_field_el = document.querySelectorAll('.error_field_auth_reg');
    const error_field = error_field_el[0];

    if(type_error === 'empty'){
        error_field.textContent = 'Empty fields';
        error_field.classList.remove('hide');

    }
    else if(type_error === 'not_exist_user')
    {
        error_field.textContent = 'This user not exist';
        error_field.classList.remove('hide');
    }
    else if(type_error === 'diff_pass'){
        error_field.textContent = 'Passwords are not equal';
        error_field.classList.remove('hide');
    }
    else if(type_error === 'this_user_already_exist'){
        error_field.textContent = 'This user already exist';
        error_field.classList.remove('hide');
    }
}

//authorized

function get_auth_form_data(){

    const name_input_el = document.querySelectorAll('.auth_reg_form_user_name_input_auth');
    const pass_input_el = document.querySelectorAll('.auth_reg_form_password_input_auth');


    const name_input_value = name_input_el[0].value;
    const pass_input_value = pass_input_el[0].value;

    if(name_input_value.length === 0 || pass_input_value.length === 0){
        show_auth_reg_field_error('empty');
        return null;
    }

    const data_obj = {
        name_u: name_input_value,
        password_u: pass_input_value,
    };

    return data_obj;
}

function send_auth_form(user_data){

    return fetch('http://127.0.0.1:5000/execute_auth', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(user_data),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Httpe error');
        }

        let data_js = null;

        if (response.headers.get('Content-Type') === "application/json"){
            data_js = null;
            show_auth_reg_field_error("not_exist_user");
        }
        else{
            hide_auth_reg_error_field();
            data_js = "http://127.0.0.1:5000/profile";
            window.location.href = data_js;
        }

        return data_js;

    })
    .then(data => {
        console.log('User created:', data);
        return data;

    })
    .catch(error => {
        console.error('Fetch error:', error);

    });
}

//registration


function get_reg_form_data(){

    const name_input_el = document.querySelectorAll('.auth_reg_form_user_name_input_reg');
    const pass_input_el = document.querySelectorAll('.auth_reg_form_password_input_reg');
    const sec_pass_input_el = document.querySelectorAll('.auth_reg_form_second_password_input_reg');


    const name_input_value = name_input_el[0].value;
    const pass_input_value = pass_input_el[0].value;
    const sec_pass_input_value = sec_pass_input_el[0].value;

    if(name_input_value.length === 0 || pass_input_value.length === 0 || sec_pass_input_value.length === 0){
        show_auth_reg_field_error('empty');
        return null;
    }


    if(pass_input_value !== sec_pass_input_value){
        show_auth_reg_field_error('diff_pass');
        return null;
    }

    const data_obj = {
        name_u: name_input_value,
        password_u: pass_input_value,
    };

    return data_obj;
}

function send_reg_form(user_data){

    return fetch('http://127.0.0.1:5000/execute_reg', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(user_data),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Httpe error');
        }

        let data_js = null;

        if (response.headers.get('Content-Type') === "application/json"){
            data_js = null;
            show_auth_reg_field_error("this_user_already_exist");
        }
        else{
            hide_auth_reg_error_field();
            data_js = "http://127.0.0.1:5000/profile";
            window.location.href = data_js;
        }

        return data_js;

    })
    .then(data => {
        console.log('User created:', data);
        return data;

    })
    .catch(error => {
        console.error('Fetch error:', error);

    });
}

// find of models page

function create_model_items(json_data, lng)
{
    for(let i = 0; i < lng; i++)
    {
        let item = json_data[i];
        const div_item= document.createElement("div");
        div_item.classList.add("main_container_models_box_item");

        const div_block_info = document.createElement("div");
        div_block_info.classList.add("main_container_models_box_item_block_info");


        const title_div = document.createElement("div");
        title_div.classList.add("main_container_models_box_item_title");
        title_div.textContent = item.name;

        const desc_div = document.createElement("div");
        desc_div.classList.add("main_container_models_box_item_description");
        desc_div.textContent = item.description;

        const a_get_model = document.createElement("a");
        a_get_model.classList.add("main_container_models_box_item_button");
        a_get_model.textContent = "go to the page of model";
        const lk = "http://127.0.0.1:5000/get_model_with_name?name=" + item.name;
        a_get_model.href = lk;

        div_block_info.appendChild(title_div);
        div_block_info.appendChild(desc_div);

        div_item.appendChild(div_block_info);
        div_item.appendChild(a_get_model);

        document.querySelector('.main_container_models_box').appendChild(div_item);
    }

}

function get_all_models(){
    return fetch('http://127.0.0.1:5000/get_all_models')
    .then(response => {
        if (!response.ok) {
            throw new Error('Http error');
        }
        return response.json();
    })
    .then(data => {
        const leng_data = Object.keys(data).length;
        create_model_items(data, leng_data);

    })
    .catch(error => {console.error('Error with execute request', error); });
}

// model_page

function set_info_to_view_model(name, desc)
{
    const title_model_el = document.querySelectorAll('.main_container_title');
    const desc_model_el = document.querySelectorAll('.main_container_description_model');

    const title_model_val = title_model_el[0];
    const desc_model_val = desc_model_el[0];

    title_model_val.textContent = name;
    desc_model_val.textContent = desc;

}

function get_info_model_by_self(){
    return fetch('http://127.0.0.1:5000/info_by_self')
    .then(response => {
        if (!response.ok) {
            throw new Error('Http error');
        }
        return response.json();
    })
    .then(data => {
        set_info_to_view_model(data.name, data.description);

    })
    .catch(error => {console.error('Error with execute request', error); });
}

function set_file_name_on_loading()
{
    const loader_file_el = document.querySelectorAll('.main_container_input_sector_send_input');
    const div_filename_el = document.querySelectorAll('.main_container_text_file_name');

    const loader_file_val = loader_file_el[0];
    const div_filename_val = div_filename_el[0];

    loader_file_val.addEventListener('change', (e) => {
        const fileInfo = e.target.files[0];
        div_filename_val.textContent = "Loaded file: " + fileInfo.name;
    });
}

function set_value_in_file_name_div(file_value){
    const div_filename_el = document.querySelectorAll('.main_container_text_file_name');
    const div_filename_val = div_filename_el[0];
    div_filename_val.textContent = file_value;
}

function get_file_name_from_loading()
{
    const div_filename_el = document.querySelectorAll('.main_container_text_file_name');
    const div_filename_val = div_filename_el[0];
    const name_file = div_filename_val.textContent;
    return name_file;
}

function set_value_proccess_model_run(proccess_value){
    const div_proccess_el = document.querySelectorAll('.main_container_model_procces_text');
    const div_proccess_val = div_proccess_el[0];
    div_proccess_val.textContent = proccess_value;
}

function get_extension_str(file_name_to_ext)
{
    if(file_name_to_ext.includes(".png")){
        return ".png";
    }else if(file_name_to_ext.includes(".jpg")){
        return ".jpg"
    }else{
        return null;
    }
}

function send_img_file_data(frm_data){

    return fetch('http://127.0.0.1:5000/run_model', {
        method: 'POST',
        body: frm_data,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Httpe error');
        }

        if (response.headers.get('Content-Type') === "application/json"){
            // response.json()
            set_value_proccess_model_run("Error of server");

        }else{
            return response.blob();
        }

        let data_js = null;
        return data_js;

    })
    .then(data => {
        console.log('User created:', data);
        if(data !== null){
            const imageUrl = URL.createObjectURL(data);
            const imgElement = document.getElementById("main_container_mdl_res_image");
            imgElement.src = imageUrl;
            set_value_proccess_model_run("Model end work");
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);

    });
}

//profile page

function set_info_to_profile_name(name)
{
    const profile_name_el = document.querySelectorAll('.profile_name_user');
    const profile_name_val = profile_name_el[0];
    profile_name_val.textContent = name;
}

function get_info_name_by_self(){
    return fetch('http://127.0.0.1:5000/info_name_profile_self')
    .then(response => {
        if (!response.ok) {
            throw new Error('Http error');
        }
        return response.json();
    })
    .then(data => {
        set_info_to_profile_name(data.name);

    })
    .catch(error => {console.error('Error with execute request', error); });
}


function create_history_items(json_data, lng)
{
    for(let i = 0; i < lng; i++)
    {
        let item = json_data[i];
        const div_item= document.createElement("div");
        div_item.classList.add("history_list_item_block");

        const title_div = document.createElement("div");
        title_div.classList.add("history_list_name_model_record");
        title_div.textContent = item.name;

        const div_get_model = document.createElement("a");
        div_get_model.classList.add("history_list_full_information");
        div_get_model.textContent = "information";
        const lk = "http://127.0.0.1:5000/get_output_model_by_id_history?id_record=" + item.id;

        div_get_model.addEventListener('click', function (event) {
            send_out_history_req(lk);
        });

        div_item.appendChild(title_div);
        div_item.appendChild(div_get_model);

        document.querySelector('.history_history_list').appendChild(div_item);
    }

}

function send_out_history_req(req_addrr){
    return fetch(req_addrr)
    .then(response => {
        if (!response.ok) {
            throw new Error('Http error');
        }
        return response.blob();
    })
    .then(data => {
        const imageUrl = URL.createObjectURL(data);
        const imgElement = document.getElementById("history_view_item_image");
        imgElement.src = imageUrl;


    })
    .catch(error => {console.error('Error with execute request', error); });
}

function get_all_histories(){
    return fetch('http://127.0.0.1:5000/get_all_history')
    .then(response => {
        if (!response.ok) {
            throw new Error('Http error');
        }
        return response.json();
    })
    .then(data => {
        const leng_data = Object.keys(data).length;
        create_history_items(data, leng_data);

    })
    .catch(error => {console.error('Error with execute request', error); });
}


function builder_handlers()
{
    if(is_authoriz_page){

        console.log('is_authoriz_page');
        hide_auth_reg_error_field();
        const button_obj = help_is_authoriz_page[0];
        button_obj.addEventListener('click', () => {

            const data_obj = get_auth_form_data();
            if(data_obj === null){
                return;
            }
            send_auth_form(data_obj);
        });

    }
    else if(is_reg_page)
    {
        console.log('is_reg_page');
        hide_auth_reg_error_field();
        const button_obj = help_is_reg_page[0];
        button_obj.addEventListener('click', () => {

            const data_obj = get_reg_form_data();
            if(data_obj === null){
                return;
            }
            send_reg_form(data_obj);
        });
    }
    else if(is_find_of_models_page)
    {
        console.log('is_find_of_models_page');
        get_all_models();
    }
    else if(is_view_model_page){
        console.log('is_view_model_page');
        get_info_model_by_self();
        set_file_name_on_loading();

        const button_obj = help_is_view_model_page[0];
        button_obj.addEventListener('click', () => {

            const file_name = get_file_name_from_loading();
            if(file_name === "File no choose"){
                set_value_in_file_name_div("You need choose file");
                return;
            }else if(file_name === "You need choose file"){
                return;
            }
            const imageData = document.querySelectorAll('.main_container_input_sector_send_input')[0].files[0];
            const formData = new FormData();
            formData.append('imagedata', imageData, file_name);
            set_value_proccess_model_run("Model begin work");
            send_img_file_data(formData);

        });
        // console.log(get_file_name_from_loading());

    }
    else if(is_profile_page){
        console.log('is_profile_page');
        get_info_name_by_self();
        get_all_histories();
    }
}



