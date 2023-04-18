import toml

config = None

class Config:
    def __init__(self, d=None):
        self.d = d
        if d is not None:
            for key, value in d.items():
                if type(value) is dict:
                    setattr(self, key, Config(value))
                else:
                    setattr(self, key, value)

    def __str__(self):
        return str(self.d)

    def get(self, attr):
        return getattr(self, attr)

    def reload(self):
        tmp = toml.load('config.toml')
        self.d = tmp
        for key, value in tmp.items():
            if type(value) is dict:
                setattr(self, key, Config(value))
            else:
                setattr(self, key, value)


with open('config.toml', 'r'):
    d = toml.load('config.toml')
    config = Config(d)


def reload():
    config.reload()

reload()
