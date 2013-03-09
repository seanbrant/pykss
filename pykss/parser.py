import os

from pykss.comment import CommentParser
from pykss.section import Section


class Parser(object):

    def __init__(self, *paths):
        self.paths = paths

    def parse(self):
        sections = {}

        filenames = [os.path.join(subpath, filename)
            for path in self.paths
            for subpath, dris, files in os.walk(path)
            for filename in files]

        for filename in filenames:
            parser = CommentParser(filename)
            for block in parser.blocks:
                section = Section(block, os.path.basename(filename))
                section.parse()
                if section.section:
                    sections[section.section] = section

        return sections

    @property
    def sections(self):
        if not hasattr(self, '_sections'):
            self._sections = self.parse()
        return self._sections

    def section(self, reference):
        return self.sections.get(reference, Section())
