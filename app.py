import os
from DB import DB

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify

app = Flask(__name__)	# Initialize the Flask application

app.config['UPLOAD_FOLDER'] = 'uploads/'	# This is the path to the upload directory
app.config['TEST_FOLDER'] = 'test/'    # This is the path to the upload directory

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test/<filename>')
def tst_images(filename):
    return send_from_directory('test/', filename)

@app.route('/test', methods=['POST'])
def test():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        image_url = os.path.join(app.config['TEST_FOLDER'], filename)
        file.save(image_url)    # save the file
        image_url = 'https://fls-shoe-app.herokuapp.com/' + image_url
        json_result =  API().compare(image_url)
        # print json_result
        return jsonify(json_result)

@app.route('/getAll')
def getAll():
    data = DB().get_all()
    return jsonify(data)

# Route that will process the file upload
@app.route('/add', methods=['POST'])
def add_from_api():
    request.is_json
    content = request.get_json()
    data = {
            'title': content['title'],
            'date': content['date']
    }
    DB().add_data(data)
    return jsonify(DB().get_all())

# Route that will process the file upload
@app.route('/addForm', methods=['POST'])
def add_from_form():
    title = request.form.get('title')
    date = request.form.get('date')
    data = {
            'title': title,
            'date': date
    }
    print(data)
    DB().add_data(data)
    return jsonify(DB().get_all())

@app.route('/delete', methods=['POST'])
def delete_api():
    cid = request.get_json()['id']
    DB().delete(cid)
    return jsonify(DB().get_all())

@app.route('/deleteForm', methods=['POST'])
def delete_form():
    cid = request.form.get('id')
    DB().delete(cid)
    return jsonify(DB().get_all())
    
#     # Check if the file is one of the allowed types/extensions
#     if file and allowed_file(file.filename):
#         # Make the filename safe, remove unsupported chars
#         filename = secure_filename(file.filename)
#         # Move the file form the temporal folder to
#         # the upload folder we setup
#         image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(image_url)	# save the file
#         image_url = 'https://fls-shoe-app.herokuapp.com/' + image_url
#         # print image_url
#         json_result =  API().get_json(image_url)
#         # print json_result
#         DB().add_data_table(image_url, json_result)
#         # return jsonify(json_result)
#         return DB().print_all_data()

if __name__ == '__main__':
    app.run(
        debug=True
    )