import logging
logger = logging.getLogger(__name__)


def to_str(inp):
    logger.debug("Before casting")
    logger.debug(inp)
    logger.debug(type(inp))
    try:
        unicode # python2
        logger.debug("python2")
        inp = inp.decode('utf-8')
    except NameError:
        logger.debug("python3")
        try:
            inp = str(inp, 'utf-8')
        except TypeError:
            logger.debug("str in py3. cast was not executed.")
            pass

    logger.debug("After casting")
    logger.debug(inp)
    logger.debug(type(inp))

    return inp
