import os

from pykss.comment import CommentParser
from pykss.exceptions import SectionDoesNotExist
from pykss.section import Section


class Parser(object):

    def __init__(self, *paths, **kwargs):
        self.paths = paths
        extensions = kwargs.pop('extensions', None)
        if extensions is None:
            extensions = ['.less', '.css', '.sass', '.scss']
        self.extensions = extensions

    def parse(self):
        sections = {}

        for filename in self.find_files():
            parser = CommentParser(filename)
            for block in parser.blocks:
                section = Section(block, os.path.basename(filename))
                if section.section:
                    sections[section.section] = section

        return sections

    def find_files(self):
        '''Find files in `paths` which match valid extensions'''
        for path in self.paths:
            for subpath, dirs, files in os.walk(path):
                for filename in files:
                    (name, ext) = os.path.splitext(filename)
                    if ext in self.extensions:
                        yield os.path.join(subpath, filename)

    @property
    def sections(self):
        if not hasattr(self, '_sections'):
            self._sections = self.parse()
        return self._sections

    def section(self, reference):
        try:
            return self.sections[reference]
        except KeyError:
            raise SectionDoesNotExist('Section "%s" does not exist.' % reference)
