# @author lmiguelmh
# @since 20161201

import os


def get_files(dir):
    return [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]


def get_content_file(file, encoding='utf8'):
    with open(file, 'r', encoding=encoding) as f:
        lines = f.readlines()
    return "\n".join(lines)
