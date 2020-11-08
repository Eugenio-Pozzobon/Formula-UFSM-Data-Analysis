def checkLicense():
    try:
        file = open('./LICENSE', 'r')
    except:
        return False

    return True
