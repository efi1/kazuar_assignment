import json


class obj(object):
    def __init__(self, dict_):
        self.__dict__.update(dict_)


def dict_to_obj(d):
    return json.loads(json.dumps(d), object_hook=obj)

