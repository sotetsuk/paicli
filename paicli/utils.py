import logging
logger = logging.getLogger(__name__)


def to_str(inp):
    _type = type(inp)
    try:
        unicode # python2
        inp = inp.decode('utf-8')
    except NameError:
        try:
            inp = str(inp, 'utf-8')
        except TypeError:
            pass

    logger.debug("Casted \"{}\" from {} to {}".format(inp, _type, type(inp)))

    return inp
