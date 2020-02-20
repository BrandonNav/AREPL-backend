from pickler import pickle_user_vars
from traceback import TracebackException, FrameSummary


class UserError(Exception):
    """
    user errors should be caught and re-thrown with this
    Be warned that this exception can throw an exception.  Yes, you read that right.  I apologize in advance.
    :raises: ValueError (varsSoFar gets pickled into JSON, which may result in any number of errors depending on what types are inside)
    """

    def __init__(self, exc_obj, exc_tb, varsSoFar={}, execTime=0):
        # skip arepl traceback - the user should just see their own error
        exc_tb = exc_tb.tb_next

        self.traceback_exception = TracebackException(type(exc_obj), exc_obj, exc_tb)
        self.friendly_message = "".join(self.traceback_exception.format())
        self.varsSoFar = pickle_user_vars(varsSoFar)
        self.execTime = execTime

        # stack is empty in event of a syntax error
        # This is problematic because frontend has to handle syntax/regular error differently
        # to make it easier populate stack so frontend can handle them the same way
        if self.traceback_exception.exc_type is SyntaxError:
            self.traceback_exception.stack.append(
                FrameSummary(self.traceback_exception.filename, int(self.traceback_exception.lineno), "")
            )
