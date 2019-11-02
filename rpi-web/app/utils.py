class JsonClass(object):

    def to_json_string(self):
        return json.dumps(self, default=lambda obj: obj.__dict__)

    def from_json_string(self, json_string):
        data = json.loads(json_string)

        for key in self.__dict__.keys():
            setattr(self, key, data[key])