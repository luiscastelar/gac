settings = None

def printError(msg, err=None):
    """
    Docstring para printError
    
    :param msg: texto
    :param err: código de salida
    """
    if err == None:
        err = -1
    settings.logging.error(msg)
    print(msg)
    exit(err)

def printInfo(msg):
    """
    Docstring para printInfo
    
    :param msg: texto
    """
    settings.logging.info(msg)
    print(msg)