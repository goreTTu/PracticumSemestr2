import sqlite3
import json


class DBManager:
    def __init__(self):
        with open('db_tools/config_db.json', 'r', encoding='utf-8') as mfp:
            params = json.load(mfp)
            self.path_to_db = params['path_to_db']
            self.is_created = params['is_created']
            self.sql_creation_script = params['sql_creation_script']

    def print_data(self):
        print(self.path_to_db, self.is_created, self.sql_creation_script)


    def connect_to_db(self):
        conn = sqlite3.connect(self.path_to_db)
        conn.row_factory = sqlite3.Row
        return conn

    def create_db(self):
        if self.is_created:
            return
        db = self.connect_to_db()
        sql_script = None
        with open(self.sql_creation_script, 'r') as sql_file:
            sql_script = sql_file.read()

        cursor = db.cursor()
        cursor.executescript(sql_script)
        db.commit()
        db.close()

        params = None

        with open('db_tools/config_db.json', 'r', encoding='utf-8') as f:
            params = json.load(f)

        with open('db_tools/config_db.json', 'w', encoding='utf-8') as mfp:
            self.is_created = True
            params['is_created'] = self.is_created
            json.dump(params, mfp)

        print("DataBase was created")

    def insert_user_if_not_exist(self, user_name, user_password):
        users = self.get_user_by_name(user_name)
        if len(users) != 0:
            return False
        db = self.connect_to_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO users (username, upassword) VALUES (?, ?)', (user_name, user_password))
        db.commit()
        db.close()
        return True


    def get_user_by_name(self, user_name):
        db = self.connect_to_db()
        cursor = db.cursor()
        cursor.execute('SELECT userid, username, upassword FROM users WHERE username = ?', (user_name,))
        results = cursor.fetchall()
        db.commit()
        db.close()
        return results

    def get_user_by_name_and_password(self, user_name, password):
        db = self.connect_to_db()
        cursor = db.cursor()
        cursor.execute('SELECT userid, username, upassword FROM users WHERE username = ? AND upassword = ?', (user_name, password))
        results = cursor.fetchall()
        db.commit()
        db.close()
        return results

    def delete_user_by_name(self, user_name):
        users = self.get_user_by_name(user_name)
        if len(users) == 0:
            return True
        db = self.connect_to_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM users WHERE username = ?', (user_name,))
        db.commit()
        db.close()
        return True

    def insert_model_by_name(self, model_name, model_descr, model_type):
        models = self.get_model_by_name(model_name)
        if len(models) != 0:
            return False
        db = self.connect_to_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO aimodels (modeltitle, modeldescription, modeltype) VALUES (?, ?, ?)', (model_name, model_descr, model_type))
        db.commit()
        db.close()
        return True

    def get_model_by_name(self, model_name):
        db = self.connect_to_db()
        cursor = db.cursor()
        cursor.execute('SELECT modelid, modeltitle, modeldescription, modeltype FROM aimodels WHERE modeltitle = ?', (model_name,))
        results = cursor.fetchall()
        db.commit()
        db.close()
        return results

    def get_model_by_id(self, model_id):
        db = self.connect_to_db()
        cursor = db.cursor()
        cursor.execute('SELECT modelid, modeltitle, modeldescription, modeltype FROM aimodels WHERE modelid = ?', (model_id,))
        results = cursor.fetchall()
        db.commit()
        db.close()
        return results

    def delete_model_by_name(self, model_name):
        models = self.get_model_by_name(model_name)
        if len(models) == 0:
            return True
        db = self.connect_to_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM aimodels WHERE modeltitle = ?', (model_name,))
        db.commit()
        db.close()
        return True

    def insert_history_item(self, user_name, model_name, path_to_img, text_out):
        user_id = self.get_user_by_name(user_name)
        user_id = user_id[0]['userid']

        model_id = self.get_model_by_name(model_name)
        model_id = model_id[0]['modelid']

        with open(path_to_img, 'rb') as f:
            img_data = f.read()
            db = self.connect_to_db()
            cursor = db.cursor()
            cursor.execute('INSERT INTO historyitems (outeruserid, outermodelid, imagebin, textout) VALUES (?, ?, ?, ?)', (user_id, model_id, img_data, text_out))
            db.commit()
            db.close()
        return True


    def get_all_history_items_by_user_id(self, user_id):
        db = self.connect_to_db()
        cursor = db.cursor()
        cursor.execute('SELECT hid, outermodelid, outeruserid FROM historyitems WHERE outeruserid = ?', (user_id,))
        results = cursor.fetchall()
        db.commit()
        db.close()
        return results

    def get_history_item_by_item_id(self, item_id):
        db = self.connect_to_db()
        cursor = db.cursor()
        cursor.execute('SELECT hid, outeruserid, outermodelid, imagebin, textout FROM historyitems WHERE hid = ?', (item_id,))
        result = cursor.fetchone()
        db.commit()
        db.close()
        return result

    def delete_history_items_all_by_user_name(self, user_name):
        user_id = self.get_user_by_name(user_name)
        if len(user_id) == 0:
            return True
        user_id = user_id[0]['userid']
        all_items = self.get_all_history_items_by_user_id(user_id)
        if len(all_items) == 0:
            return True

        id_list = []
        for item in all_items:
            tmp_s = item[0]['hid']
            id_list.append((tmp_s,))

        db = self.connect_to_db()
        cursor = db.cursor()
        sql_q = "DELETE FROM historyitems WHERE hid = ?"
        cursor.executemany(sql_q, id_list)
        db.commit()
        db.close()
        return True



