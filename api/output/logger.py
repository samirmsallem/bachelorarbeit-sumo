
LOG = False


def printlog(string):
    '''
    Default logger function to log important messages to the console log
    Since sometimes its not necessary to print logs, this feature can be toggled of globally thorugh the above boolean flag
    '''
    if(LOG):
        print(string)