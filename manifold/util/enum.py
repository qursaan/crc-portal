class Enum(object):
    def __init__(self, *keys):
        self.__dict__.update(zip(keys, range(len(keys))))
        self.invmap = {v:k for k, v in self.__dict__.items()}
    
    def get_str(self, value):
        return self.invmap[value]
