import os
import logging

logger = logging.getLogger(__name__)


class FSUtils:
    @staticmethod
    def getScriptPath():
        scriptPath = ""
        try:
            scriptPath = os.path.dirname(os.path.realpath(__file__))
            scriptPath = os.path.dirname(scriptPath)
        except OSError:
            logger.exception(
                "Could not retrieve script path, using current working directory"
            )
            try:
                scriptPath = os.getcwd()
            except OSError:
                logger.exception(
                    "Could not retrieve current working directory either :("
                )

        return scriptPath

    @staticmethod
    def createDirectory(path):
        try:
            path = os.path.abspath(path)
            if os.path.exists(path):
                return True
            else:
                logger.debug("Creating directory [%s]", path)

            os.makedirs(path)
        except Exception:
            logger.exception("Could not create directory [%s]", path)
            return False
        return True
