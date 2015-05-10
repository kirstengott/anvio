# -*- coding: utf-8

"""Exceptions"""

import textwrap

from anvio.ttycolors import color_text

__author__ = "A. Murat Eren"
__copyright__ = "Copyright 2015, The anvio Project"
__credits__ = []
__license__ = "GPL 3.0"
__maintainer__ = "A. Murat Eren"
__email__ = "a.murat.eren@gmail.com"
__status__ = "Development"


def remove_spaces(text):
    while 1:
        if text.find("  ") > -1:
            text = text.replace("  ", " ")
        else:
            break

    return text


class AnvioError(Exception, object):
    def __init__(self, e = None):
        Exception.__init__(self)
        return

    def __str__(self):
        max_len = max([len(l) for l in textwrap.fill(self.e, 80).split('\n')])
        error_lines = ['%s%s' % (l, ' ' * (max_len - len(l))) for l in textwrap.fill(self.e, 80).split('\n')]

        error_message = ['%s: %s' % (color_text(self.error_type, 'red'), error_lines[0])]
        for error_line in error_lines[1:]:
            error_message.append('%s%s' % (' ' * (len(self.error_type) + 2), error_line))

        return '\n\n' + '\n'.join(error_message) + '\n\n'


class ConfigError(AnvioError):
    def __init__(self, e = None):
        self.e = remove_spaces(e)
        self.error_type = 'Config Error'
        AnvioError.__init__(self)


class TerminalError(AnvioError):
    def __init__(self, e = None):
        self.e = remove_spaces(e)
        self.error_type = 'Terminal Error'
        AnvioError.__init__(self)


class FilesNPathsError(AnvioError):
    def __init__(self, e = None):
        self.e = remove_spaces(e)
        self.error_type = 'File/Path Error'
        AnvioError.__init__(self)


