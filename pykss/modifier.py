class Modifier(object):

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @property
    def class_name(self):
        return self.name.replace('.', ' ').replace(':', ' pseudo-class-').strip()
