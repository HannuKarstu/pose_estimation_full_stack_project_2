import os
import io
import json

from flask import Flask, request, send_file, abort

from backend.config import config
from backend.file_handler import save_file, create_folders, delete_file, open_file, get_filepath, get_files
from backend.pose_estimation_process import estimate_pose
from backend.model_utils import SUPPORTED_MODELS
from backend.visualisation_utils import visualize_image_with_keypoints, numpy_array_to_img
from backend.database_connection import DBConnection
from backend.database import mongo
from backend.tensor_utils import convert_image_to_tensor
from backend.stats import calculate_stats

dir_path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

if os.environ.get("MONGO_URI"):
    # Using for example Azure's MongoDB
    app.config["MONGO_URI"] = os.environ["MONGO_URI"]
else:
    # local
    app.config["MONGO_URI"] = 'mongodb://'  \
        + os.environ['MONGODB_USERNAME']  \
        + ':' + os.environ['MONGODB_PASSWORD']  \
        + '@' + os.environ['MONGODB_HOSTNAME']  \
        + ':' + os.environ['MONGODB_PORT']  \
        + '/' + os.environ['MONGODB_DATABASE']

db_connection = DBConnection("predictions")

create_folders()
mongo.init_app(app)


@app.errorhandler(400)
def bad_request(error):
    print(error.description)
    return {"error": error.description}, error.code


@app.errorhandler(404)
def file_not_found(error):
    print(error.description)
    return {"error": error.description}, error.code


@app.errorhandler(500)
def internal_server_error(error):
    print(error.description)
    return {"error": error.description}, error.code


@app.route('/hello', methods=['GET'])
def hello():
    print("Hello from Flask!")
    return {"hello": "from flask"}


@app.route('/environment', methods=['GET'])
def environment():
    return {"environment": os.environ.get('RUN_ENV')}


@app.route('/items', methods=['GET', 'POST'])
def items():
    db_status = ''
    file_status = ''
    item = {}
    items = []

    if request.method == "GET":
        items, db_status = db_connection.get_all_items()

    elif request.method == "POST":
        data = json.loads(request.data)
        item, db_status = db_connection.insert_item(data)

    return {
        "status": {
            "db_status": db_status,
            "file_status": file_status
        },
        "item": item,
        "items": items
    }


@app.route('/stats', methods=['GET'])
def stats():
    db_status = ''
    file_status = ''
    item = {}
    items = []

    if request.method == "GET":
        items, db_status = db_connection.get_all_items()
        model_amounts, image_amounts, prediction_dates = calculate_stats(items)

    return {
        "status": {
            "db_status": db_status,
            "file_status": file_status
        },
        "total_results": len(items),
        "model_amounts": model_amounts,
        "image_amounts": image_amounts,
        "prediction_dates": prediction_dates
    }


@app.route('/models', methods=['GET'])
def models():
    models = SUPPORTED_MODELS
    return {
        "models": models
    }


@app.route('/items/<id>', methods=['GET', 'PUT', 'DELETE'])
def item(id):
    db_status = ''
    file_status = ''
    item = {}

    if request.method == "GET":
        item, db_status = db_connection.find_item_by_id(id)

    elif request.method == "PUT":
        update = json.loads(request.data)
        item, db_status = db_connection.update_item(id, update)

    elif request.method == "DELETE":
        item, db_status = db_connection.delete_item(id)
        file_status = delete_file(item.get("filename"))

    return {
        "status": {
            "db_status": db_status,
            "file_status": file_status
        },
        "item": item
    }


@app.route('/files/<id>', methods=['GET'])
def get_file(id):
    if request.method == "GET":
        print(f"Requesting file from db id ({id})")
        item, db_status = db_connection.find_item_by_id(id)

        filename = item.get("filename")
        filepath = get_filepath(filename)

        if not filepath:
            abort(404, 'File not found in file system')

        prediction = request.args.get('prediction')

        if prediction:
            print(f"- Drawing prediction on image")
            keypoints_with_scores = item["keypoints_with_scores"]
            image_tensor = convert_image_to_tensor(filepath)

            np_array = visualize_image_with_keypoints(
                image_tensor, keypoints_with_scores)

            image_binary = numpy_array_to_img(np_array)

            filepath = io.BytesIO(image_binary)

        return send_file(
            filepath,
            mimetype='image/png',
            as_attachment=True,
            download_name=filename
        )


@app.route('/files', methods=['GET', 'POST'])
def files():
    if request.method == "POST":
        file = request.files['file']

        print(
            f"\nReceived {request.method} request to save a file")

        filename, filepath = save_file(file)

        file_status = "ok" if filename else "not_saved"

        return {
            "status": {
                "db_status": '',
                "file_status": file_status
            },
        }

    elif request.method == "GET":
        print(f"Received {request.method} request to fetch all files")

        files_list = get_files()

        return {
            "files": files_list
        }


@app.route('/predict', methods=['POST'])
def predict():
    model_name = request.args['model_name']
    file = request.files['file']

    print(
        f"\nReceived {request.method} request to estimate the pose using '{model_name}'")

    filename, filepath = save_file(file)

    keypoints_with_scores, image_tensor = estimate_pose(
        filepath, model_name)

    item = {
        "filename": filename,
        "keypoints_with_scores": keypoints_with_scores.tolist(),
        "model_name": model_name
    }

    db_id = db_connection.insert_item(item)

    np_array = visualize_image_with_keypoints(
        image_tensor, keypoints_with_scores)

    image_binary = numpy_array_to_img(np_array)

    return send_file(
        io.BytesIO(image_binary),
        mimetype='image/png',
        as_attachment=True,
        download_name=filename)


@app.route('/config', methods=['GET'])
def get_dict_config():
    return config.dict()


@app.after_request
def add_headers(response):
    response.headers.add('Content-Type', 'application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods',
                         'PUT, GET, POST, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Expose-Headers',
                         'Content-Type,Content-Length,Authorization,X-Pagination')
    return response


def _is_true(string):
    return False if string in ["false", "False"] else True


if __name__ == "__main__":
    print(f"\nStarting application\n\n")
    app.run(
        debug=_is_true(os.environ.get('APP_DEBUG', "True")),
        host='0.0.0.0',
        port=8000)
