import traceback

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def catch(func):
    return generalCatcher(func, fatal = False)

def catchFatal(func):
    return generalCatcher(func, fatal = True)

def generalCatcher(func, fatal = False):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            printError(traceback = traceback.format_exc(), fatal = fatal)
            if fatal:
                exitProgram(1)
    return wrapper

def exitProgram(status):
    exit(status)

def printError(traceback = "", fatal = False):
    print(f'{bcolors.BOLD}{"An error occured" if not fatal else "A fatal error occured"}: {bcolors.ENDC}{bcolors.FAIL}{traceback}{bcolors.ENDC}')