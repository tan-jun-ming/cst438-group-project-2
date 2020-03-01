import traceback

def get_traceback(e):
    return "".join(traceback.TracebackException.from_exception(e).format())