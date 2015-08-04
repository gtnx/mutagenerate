# -*- coding: utf-8 -*-

# from __future__ import absolute_import, division, print_function

import os
import sys


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {
        "yes": True,
        "y": True,
        "ye": True,
        "no": False,
        "n": False
    }
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def list_directory(directory, extension):
    return [os.path.join(directory, fn) for fn in filter(lambda x: x.endswith('.' + extension), os.listdir(directory))]


def rget(data, *keys, **kwargs):
    try:
        value = data[keys[0]]
        for key in keys[1:]:
            value = value[key]
    except (KeyError, IndexError, TypeError):
        return kwargs.get('default', None)
    return value


def ignore_errors(errors, logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors as e:
                logger.error(e)
        return wrapper
    return decorator


def format_rows_output(rows):
    cols = zip(*rows)
    col_widths = [max(len(unicode(value)) for value in col) for col in cols]
    return '\n'.join([' | '.join([('%%%ds' % col_widths[i]) % unicode(value) for i, value in enumerate(row)]) for row in rows])
