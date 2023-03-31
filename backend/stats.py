import datetime
from bson.objectid import ObjectId


def calculate_stats(items):
    filename_count = {}
    model_count = {}
    date_count = {}

    for item in items:
        filename = item.get("filename")
        model_name = item.get("model_name")
        obj_id = ObjectId(item.get("_id"))

        if filename and model_name and obj_id:
            filename_count[filename] = filename_count.get(filename, 0) + 1
            model_count[model_name] = model_count.get(model_name, 0) + 1

            timestamp = obj_id.generation_time.timestamp()
            dt_object = datetime.datetime.fromtimestamp(timestamp)
            date = dt_object.strftime("%Y-%m-%d")
            date_count[date] = date_count.get(date, 0) + 1

    return model_count, filename_count, date_count
