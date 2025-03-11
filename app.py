from flask import Flask, request, send_file, jsonify
import os
import os.path
import shutil

app = Flask(__name__)

# Папка для хранения файлов (относительно корня проекта)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Создаем папку uploads, если ее нет
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/delete')
def query_delete():
    passFL = request.args.get('pass')
    if(passFL=='1234'):
        



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




        return '<h1> delited </h1>'
    else:
        return '<h1> wrong pass </h1>'


@app.route('/')
def query_start():
    return '<h1> hello 123 </h1>'



@app.route('/add_schedule/<filename>', methods=['GET', 'POST'])
def manage_file(filename):
    """
    Обрабатывает GET-запросы для скачивания файла и POST-запросы для загрузки файла.
    """
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

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
            return jsonify({'message': 'File uploaded successfully'}), 201
        except Exception as e:
            return jsonify({'error': f"Error uploading file: {str(e)}"}), 500


def delete_all_files_in_directory(directory):
    """Удаляет все файлы (и подпапки!) из указанной директории."""
    
        #print(f"Ошибка при работе с директорией '{directory}': {e}")



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')