import re


single_line_re = re.compile(r'^\s*\/\/')
single_line_strip_re = re.compile(r'\s*\/\/')

multi_line_start_re = re.compile(r'^\s*\/\*')
multi_line_end_re = re.compile(r'.*\*\/')
multi_line_start_strip_re = re.compile(r'\s*\/\*')
multi_line_end_strip_re = re.compile(r'\*\/')
multi_line_middle_strip_re = re.compile(r'^(\s*\*+)')

preceding_white_space_re = re.compile(r'^\s*')


def is_single_line_comment(line):
    return single_line_re.match(line) is not None


def is_multi_line_comment_start(line):
    return multi_line_start_re.match(line) is not None


def is_multi_line_comment_end(line):
    if is_single_line_comment(line):
        return False
    return multi_line_end_re.match(line) is not None


def parse_single_line(line):
    return single_line_strip_re.sub('', line).rstrip()


def parse_multi_line(line):
    cleaned = multi_line_start_strip_re.sub('', line)
    return multi_line_end_strip_re.sub('', cleaned).rstrip()


def normalize(lines):
    cleaned = []
    indents = []

    for line in lines:
        line = multi_line_middle_strip_re.sub('', line)
        cleaned.append(line)
        match = preceding_white_space_re.match(line)
        if line:
            indents.append(len(match.group()))

    indent = min(indents) if indents else 0

    return '\n'.join([line[indent:] for line in cleaned]).strip()


class CommentParser(object):

    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        blocks = []
        current_block = []
        inside_single_line_block = False
        inside_multi_line_block = False

        with open(self.filename) as fileobj:
            for line in fileobj:
                # Parse single-line style
                if is_single_line_comment(line):
                    parsed = parse_single_line(line)

                    if inside_single_line_block:
                        current_block.append(parsed)
                    else:
                        current_block = [parsed]
                        inside_single_line_block = True

                # Prase multi-line style
                if is_multi_line_comment_start(line) or inside_multi_line_block:
                    parsed = parse_multi_line(line)

                    if inside_multi_line_block:
                        current_block.append(parsed)
                    else:
                        current_block = [parsed]
                        inside_multi_line_block = True

                # End a multi-line block if detected
                if is_multi_line_comment_end(line):
                    inside_multi_line_block = False

                # Store the current block if we're done
                if is_single_line_comment(line) is False and inside_multi_line_block is False:
                    if current_block:
                        blocks.append(normalize(current_block))

                    inside_single_line_block = False
                    current_block = []

        return blocks

    @property
    def blocks(self):
        if not hasattr(self, '_blocks'):
            self._blocks = self.parse()
        return self._blocks
