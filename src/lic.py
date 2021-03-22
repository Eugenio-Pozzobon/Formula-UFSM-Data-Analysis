def checkLicense():
    '''
    check if licese file is saved with aplication folder to alow user run the app
    :return: boolean
    '''
    try:
        file = open('./LICENSE', 'r')
    except:
        return False

    return True
