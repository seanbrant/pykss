class Modifier(object):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.example = ''

    @property
    def class_name(self):
        return self.name.replace('.', ' ').replace(':', ' pseudo-class-').strip()

    def add_example(self, example):
        self.example = example.replace('$modifier_class', ' %s' % self.class_name)
