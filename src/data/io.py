import os


def json_serialize_default(obj):
    """for objects that have members that cant be serialized and implement toJson() method"""
    try:
        return obj.toJson()
    except Exception:
        return obj.__dict__


def create_if_not_exist(path):
    if path is not None and not os.path.exists(path):
        os.makedirs(path)
