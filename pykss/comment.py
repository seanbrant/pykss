SINGLE_LINE = '//'
MULTI_LINE = '*'
MULTI_LINE_START = '/*'
MULTI_LINE_END = '*/'


def is_single_line_comment(line):
    return line.startswith(SINGLE_LINE)


def is_multi_line_comment_start(line):
    return line.startswith(MULTI_LINE_START)


def is_multi_line_comment_end(line):
    if is_single_line_comment(line):
        return False
    return line.endswith(MULTI_LINE_END)


def parse_single_line(line):
    return line[len(SINGLE_LINE):].strip()


def parse_multi_line(line):
    if is_multi_line_comment_start(line):
        line = line[len(MULTI_LINE_START):]

    if is_multi_line_comment_end(line):
        line = line[:-len(MULTI_LINE_END)]

    if line.startswith(MULTI_LINE):
        line = line[len(MULTI_LINE):]

    return line.strip()


def normalize(lines):
    return '\n'.join(lines).strip()


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
                line = line.strip()

                if is_single_line_comment(line):
                    parsed = parse_single_line(line)

                    if inside_single_line_block:
                        current_block.append(parsed)
                    else:
                        current_block = [parsed]
                        inside_single_line_block = True

                if is_multi_line_comment_start(line) or inside_multi_line_block:
                    parsed = parse_multi_line(line)

                    if inside_multi_line_block:
                        current_block.append(parsed)
                    else:
                        current_block = [parsed]
                        inside_multi_line_block = True

                if is_multi_line_comment_end(line):
                    inside_multi_line_block = False

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
