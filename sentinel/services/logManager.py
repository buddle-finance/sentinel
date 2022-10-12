import logging
import logging.handlers as handlers
import os

from sentinel.utils.constants import Constants
from sentinel.utils.fsUtils import FSUtils


class BuddleLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        self.errors = []
        self.warnings = []
        self.allErrors = []

        super(BuddleLogger, self).__init__(name, level)

    def debug(self, msg, *args, **kwargs):
        return super(BuddleLogger, self).debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        return super(BuddleLogger, self).info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        fmtmsg = str(msg)
        if args:
            fmtmsg = fmtmsg % args

        self.warnings.append(fmtmsg)
        self.allErrors.append("WARN: " + fmtmsg)

        return super(BuddleLogger, self).warning(msg, *args, **kwargs)

    warn = warning

    def error(self, msg, *args, **kwargs):
        fmtmsg = str(msg)
        if args:
            fmtmsg = fmtmsg % args

        self.errors.append(fmtmsg)
        self.allErrors.append("ERROR: " + fmtmsg)

        return super(BuddleLogger, self).error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        fmtmsg = str(msg)
        if args:
            fmtmsg = fmtmsg % args

        self.errors.append(fmtmsg)
        self.allErrors.append("ERROR: " + fmtmsg)

        kwargs["exc_info"] = 1
        return super(BuddleLogger, self).error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        fmtmsg = str(msg)
        if args:
            fmtmsg = fmtmsg % args

        self.errors.append(fmtmsg)
        self.allErrors.append("CRITICAL: " + fmtmsg)

        return super(BuddleLogger, self).critical(msg, *args, **kwargs)

    fatal = critical

    def log(self, level, msg, *args, **kwargs):
        return super(BuddleLogger, self).log(level, msg, *args, **kwargs)

    def findCaller(self, stack_info=False, stacklevel=3):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        We override this to get the caller 1 frame above the usual retrieved
        by logging.findCaller. Without this, caller information will always
        refer to the log functions implemented in this derived class.
        """
        return super(BuddleLogger, self).findCaller(stack_info, 3)

    @staticmethod
    def setupLogger(
        logLocation, logLevel="INFO"
    ):  # DEBUG, INFO, WARNING, ERROR, CRITICAL
        logging.setLoggerClass(BuddleLogger)
        logger = logging.getLogger(__name__)
        try:
            logger.setLevel(logLevel.upper())
        except Exception:
            logLevel = logging.INFO

        try:
            if logLocation is not None:
                logFileDir = logLocation
            else:
                logFileDir = os.path.join(FSUtils.getScriptPath(), "logs")

            logFilePath = os.path.join(logFileDir, Constants.LOG_FILE_NAME)
            FSUtils.createDirectory(logFileDir)
            fileLogFormat = logging.Formatter(
                "%(process)-5d %(asctime)s %(levelname)-7s %(module)-15s %(funcName)-20s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            fileLogHandler = handlers.RotatingFileHandler(
                logFilePath, maxBytes=2000000, backupCount=4
            )
            fileLogHandler.setLevel(logging.DEBUG)
            fileLogHandler.setFormatter(fileLogFormat)
            logger.addHandler(fileLogHandler)
        except Exception:
            logger.exception("Could not set up file logger")

        logger.debug("Logger setup done!")
        return logger
