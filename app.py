from flask import Flask, request, send_file, jsonify
import os
import os.path
import shutil
import re
from flask_sqlalchemy import SQLAlchemy




def addListFile(filename):
    
    try:
        
        filepathList = os.path.join(app.config['UPLOAD_FOLDER'], 'list_files.txt')
        if(filename!=''):
            with open(filepathList, 'a') as f:  # "a" означает режим "append" (добавление)
                f.write(filename + "\n") 
        
        else:
            with open(filepathList, 'w') as f:
                return
                
    except Exception as e:
        return jsonify({'error': 'Error add to list names'}), 500



app = Flask(__name__)
# Папка для хранения файлов (относительно корня проекта)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://filo:Pas4(sheduledb)@127.0.0.1:1201/shedule_db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://filo:Pas4(sheduledb)@192.168.1.165:1201/shedule_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Создаем папку uploads, если ее нет
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
addListFile('')



class Analytics(db.Model):
    __tablename__ = 'analytics'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10))
    event = db.Column(db.String(300))


@app.route('/analytics', methods=['POST'])
def add_analytics():
    data = request.get_data(as_text=True)

    if ':' in data:
        code, event = data.split(':', 1)
        record = Analytics(code=code.strip(), event=event.strip())
        db.session.add(record)
        db.session.commit()

    return ''



@app.route('/delete')
def query_delete():
    passFL = request.args.get('pass')
    if(passFL=='delallpas'):
        
        try:
            for filename in os.listdir(UPLOAD_FOLDER):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path) # Удаляет файл
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path) # Удаляет папку рекурсивно
            except Exception as e:
                return 0
                #print(f"Не удалось удалить {file_path}. Ошибка: {e}")
        except FileNotFoundError:
            return 0
        #print(f"Директория '{directory}' не найдена.")
        except OSError as e:
            return 0



        addListFile('')
        return '<h1> delited </h1>'
    else:
        return '<h1> wrong pass </h1>'


@app.route('/')
def query_start():
    return '<h1> hello </h1>'

@app.route('/list_files')
def query_list():
    filepathList = os.path.join(app.config['UPLOAD_FOLDER'], 'list_files.txt')
    return send_file(filepathList, as_attachment=True)

        

@app.route('/add_schedule/<filename>', methods=['GET', 'POST'])
def manage_file(filename):
    """
    Обрабатывает GET-запросы для скачивания файла и POST-запросы для загрузки файла.
    """
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename+'.txt')

    if request.method == 'GET':
        """
        Скачивание файла.
        """
        if os.path.exists(filepath):
            try:
                return send_file(filepath, as_attachment=True) # force download
            except Exception as e:
                return jsonify({'error': f"Error sending file: {str(e)}"}), 500
        else:
            return jsonify({'error': 'File not found'}), 404

    elif request.method == 'POST':
        """
        Загрузка файла.
        """
        try:
            data = request.get_data(as_text=True) # Получаем данные из тела запроса
            with open(filepath, 'w') as f:
                f.write(data)

            addListFile(filename)
            
                

            return jsonify({'message': 'File uploaded successfully '+filename}), 201

        except Exception as e:
            return jsonify({'error': f"Error uploading file: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

