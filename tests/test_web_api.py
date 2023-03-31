import pytest
import json
import os
import shutil
import io
from datetime import datetime

from mongomock import MongoClient
from unittest.mock import patch

from backend.web_app import app as flask_app
from backend.file_handler import create_folders
import backend.database
from backend.database import mongo


dir_path = os.path.dirname(os.path.realpath(__file__))
temp_path = os.path.join(dir_path, "temp")


class PyMongoMock(MongoClient):
    def init_app(self, app):
        return super().__init__()


class TestWebApi:
    @pytest.fixture
    def setup_and_teardown(self):
        self._setup()
        yield
        self._teardown()

    def _setup(self):
        print("\nSetting up")
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
        create_folders()

    def _teardown(self):
        print("\nTearing down")

    @pytest.fixture
    def app(self):
        yield flask_app

    @pytest.fixture
    def client(self, app):
        return app.test_client()

    def test_hello(self, app, client, setup_and_teardown):
        res = client.get('/hello')
        assert res.status_code == 200
        expected = {'hello': 'from flask'}
        assert expected == json.loads(res.get_data(as_text=True))

    def test_models(self, app, client, setup_and_teardown):
        res = client.get('/models')
        assert res.status_code == 200
        expected = {
            'models': [
                "blazepose",
                "tflite_movenet_lightning_f16",
                "tflite_movenet_thunder_f16",
                "tflite_movenet_lightning_int8",
                "tflite_movenet_thunder_int8",
                "movenet_lightning",
                "movenet_thunder"
            ]
        }
        assert expected == json.loads(res.get_data(as_text=True))

    @patch.object(backend.database, "mongo", PyMongoMock())
    def test_predict(self, app, client, setup_and_teardown):
        mongo.init_app(app)

        def _predict(filename, expected_filename, renamed_filename=None):
            filepath = os.path.join(dir_path, "fixtures", filename)
            if renamed_filename:
                filename = renamed_filename
            data = {
                'file': (open(filepath, 'rb'), filename)
            }

            model_name = "tflite_movenet_lightning_f16"

            res = client.post(f"/predict?model_name={model_name}", data=data)
            assert res.status_code == 200
            assert res.headers['Content-Disposition'].startswith(
                f"attachment; filename={expected_filename}")
            assert 490000 < len(res.data) < 820000

        # Send same file 2 times to guarantee that the recursive file saving/naming function works.
        _predict("test_image.png", "test_image.png")
        _predict("test_image.png", "test_image.png")
        _predict("test_image_2.png", "test_image_1.png",
                 renamed_filename="test_image.png")

    @patch.object(backend.database, "mongo", PyMongoMock())
    def test_items(self, app, client, setup_and_teardown):
        mongo.init_app(app)

        item = {
            "filename": "filename.abc",
            "keypoints_with_scores": [[[1, 2, 3], [4, 5, 6]]],
            "model_name": "model_abc"
        }

        # Add data to db
        res = client.post("/items", data=json.dumps(item))
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["item"]["_id"]

        # Get all docs from DB
        res = client.get("/items")
        assert res.status_code == 200

        data = json.loads(res.data)

        for key in ["filename", "keypoints_with_scores", "model_name"]:
            assert data["items"][-1][key] == item[key]

    @patch.object(backend.database, "mongo", PyMongoMock())
    def test_post_get_delete_item(self, app, client, setup_and_teardown):
        mongo.init_app(app)

        item = {
            "filename": "filename.abc",
            "keypoints_with_scores": [[[4, 5, 6], [7, 8, 9]]],
            "model_name": "model_abc"
        }

        # 1. POST data to db
        res1 = client.post("/items", data=json.dumps(item))
        assert res1.status_code == 200
        data1 = json.loads(res1.data)

        assert data1["item"]["_id"]
        id = str(data1["item"]["_id"])

        # 2. GET single doc from DB
        res2 = client.get(f"/items/{id}")
        data2 = json.loads(res2.data)
        for key in ["filename", "keypoints_with_scores", "model_name"]:
            assert data2["item"][key] == item[key]

        # 3. PUT extra data to doc in DB
        item3 = {"extra": "abc"}
        res3 = client.put(f"/items/{id}", data=json.dumps(item3))

        # 3b Assert extra data is present
        res3b = client.get(f"/items/{id}")
        data3b = json.loads(res3b.data)
        assert data3b["item"]["extra"] == item3["extra"]

        # 4. DELETE earlier posted data
        res4 = client.delete(f"/items/{id}")
        data4 = json.loads(res4.data)
        assert data4["status"] == {
            "db_status": "deleted", "file_status": "not_found"}

        # 4b. Assert file is deleted
        res4b = client.get(f"/items/{id}")
        data4b = json.loads(res4b.data)
        assert data4b["item"] == None

    @patch.object(backend.database, "mongo", PyMongoMock())
    def test_get_file(self, app, client, setup_and_teardown):
        mongo.init_app(app)

        # Copy file to files folder
        filename = "test_image.png"
        filepath = os.path.join(dir_path, "fixtures", filename)
        dst_path = os.path.join(temp_path, "files", filename)
        shutil.copyfile(filepath, dst_path)

        item = {
            "filename": filename,
            "keypoints_with_scores": [[[
                [0.33217365, 0.5726658, 0.4494615],
                [0.31439158, 0.5772979, 0.6838645],
                [0.31208035, 0.5512204, 0.5983896],
                [0.31852993, 0.5547738, 0.38557354],
                [0.31637684, 0.4976929, 0.6155093],
                [0.41426465, 0.549188, 0.5268066],
                [0.4061126, 0.43749478, 0.67215455],
                [0.50775003, 0.6594318, 0.6601538],
                [0.5105499, 0.52640384, 0.81059706],
                [0.42197028, 0.64408493, 0.5783226],
                [0.4168474, 0.6145565, 0.6359308],
                [0.6082694, 0.40747428, 0.6510321],
                [0.60762316, 0.31438535, 0.7702483],
                [0.64879423, 0.5663375, 0.6455827],
                [0.6788212, 0.43183458, 0.61457497],
                [0.8356959, 0.515922, 0.533018],
                [0.8902436, 0.3593879, 0.77834857]
            ]]],
            "model_name": "model_abc"
        }

        # 1. POST data to db
        res1 = client.post("/items", data=json.dumps(item))
        assert res1.status_code == 200
        data1 = json.loads(res1.data)
        id = data1["item"]["_id"]

        # 2. GET file
        res2 = client.get(f"/files/{id}")
        assert res2.status_code == 200
        assert res2.headers['Content-Disposition'] == f"attachment; filename={filename}"
        assert 730000 < len(res2.data) < 740000

        # 3. GET file with keypoints drawn
        res3 = client.get(f"/files/{id}?prediction=true")
        assert res2.status_code == 200
        assert res2.headers['Content-Disposition'] == f"attachment; filename={filename}"
        assert 730000 < len(res2.data) < 740000

    @patch.object(backend.database, "mongo", PyMongoMock())
    def test_files(self, app, client, setup_and_teardown):
        mongo.init_app(app)

        # Copy file to files folder
        filename = "test_image.png"
        filepath = os.path.join(dir_path, "fixtures", filename)

        """
            response = self.client.post(
                url_for('adverts.save'), data=data, follow_redirects=True,
                content_type='multipart/form-data'
            )
        """
        item = {}
        item['file'] = (io.BytesIO(b"abcdef"), 'test.jpg')

        # 1. POST file
        res1 = client.post("/files", data=item)
        assert res1.status_code == 200
        data1 = json.loads(res1.data)
        assert data1["status"]["file_status"] == "ok"

        # 2. GET files
        res2 = client.get("/files")
        assert res1.status_code == 200
        data2 = json.loads(res2.data)
        assert data2["files"] == ["test.jpg"]

    @patch.object(backend.database, "mongo", PyMongoMock())
    def test_get_file_not_found(self, app, client, setup_and_teardown):
        mongo.init_app(app)

        filename = "not_found.jpg"

        item = {
            "filename": filename,
            "keypoints_with_scores": [[[4, 5, 6], [7, 8, 9]]],
            "model_name": "model_abc"
        }

        # 1. POST data to db
        res1 = client.post("/items", data=json.dumps(item))
        assert res1.status_code == 200
        data1 = json.loads(res1.data)
        id = data1["item"]["_id"]

        # 2. GET file
        res2 = client.get(f"/files/{id}")
        assert res2.status_code == 404
        data2 = json.loads(res2.data)
        assert data2 == {
            "error": "File not found in file system"}

    @patch.object(backend.database, "mongo", PyMongoMock())
    def test_stats(self, app, client, setup_and_teardown):
        mongo.init_app(app)

        def _predict(filename, expected_filename, renamed_filename=None, model_name="tflite_movenet_lightning_f16"):
            filepath = os.path.join(dir_path, "fixtures", filename)
            if renamed_filename:
                filename = renamed_filename
            data = {
                'file': (open(filepath, 'rb'), filename)
            }

            res = client.post(f"/predict?model_name={model_name}", data=data)
            assert res.status_code == 200

        _predict("test_image.png", "test_image.png")
        _predict("test_image.png", "test_image.png")
        _predict("test_image_2.png", "test_image_1.png",
                 renamed_filename="test_image.png")

        res = client.get("/stats")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data == {
            "image_amounts":
                {
                    "test_image.png": 2,
                    "test_image_1.png": 1
                },
            "model_amounts":
                {
                    "tflite_movenet_lightning_f16": 3
                },
            "prediction_dates":
                {
                    f"{datetime.now().strftime('%Y-%m-%d')}": 3
                },
            "status":
                {
                    "db_status": "found",
                    "file_status": ""
                },
            "total_results": 3
        }
