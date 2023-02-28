import uuid


class Journey(object):
    def __init__(self, size: int):
        self.id = uuid.uuid4().__str__()
        self.size = size

    def __str__(self):
        return f'<<<Journey id:{self.id}, size:{self.size}>>>'
