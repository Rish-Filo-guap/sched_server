from flask import Flask, request, send_file, jsonify
import os

app = Flask(__name__)

# Папка для хранения файлов (относительно корня проекта)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Создаем папку uploads, если ее нет
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/file/<filename>', methods=['GET', 'POST'])
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
