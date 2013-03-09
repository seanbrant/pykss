import re

from pykss.modifier import Modifier


CLASS_MODIFIER = '.'
PSEUDO_CLASS_MODIFIER = ':'
MODIFIER_DESCRIPTION_SEPARATOR = ' - '
REFERENCE_START = 'Styleguide'

reference_re = re.compile('%s ([\d\.]+)' % REFERENCE_START)


class Section(object):

    def __init__(self, comment=None, filename=None):
        self.comment = comment
        self.filename = filename

    def parse(self):
        self._description_lines = []
        self._modifiers = []
        self._reference = None

        for line in self.comment.splitlines():
            if line.startswith(CLASS_MODIFIER) or line.startswith(PSEUDO_CLASS_MODIFIER):
                try:
                    modifier, description = line.split(MODIFIER_DESCRIPTION_SEPARATOR)
                except ValueError:
                    pass
                else:
                    self._modifiers.append(Modifier(modifier.strip(), description.strip()))

            elif line.startswith(REFERENCE_START):
                self._reference = reference_re.match(line).groups()[0].rstrip('.')
            else:
                self._description_lines.append(line)

        self._description = '\n'.join(self._description_lines).strip()

    @property
    def description(self):
        if not hasattr(self, '_description'):
            self.parse()
        return self._description

    @property
    def modifiers(self):
        if not hasattr(self, '_modifiers'):
            self.parse()
        return self._modifiers

    @property
    def section(self):
        if not hasattr(self, '_reference'):
            self.parse()
        return self._reference
