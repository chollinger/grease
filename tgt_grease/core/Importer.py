import importlib
from tgt_grease.core import Logging


class ImportTool(object):
    """Import Tooling for getting instances of classes automatically

    Attributes:
        _log (Logging): Logger for the class

    """

    _log = None

    def __init__(self, logger):
        if not isinstance(logger, Logging):
            raise Exception("Invalid Constructor, logger element not of type Logging class")
        else:
            self._log = logger

    def load(self, className):
        """Dynamic loading of classes for the system

        Args:
            className (str): Class name to search for

        Returns:
            object: If an object is found it is returned
            None: If an object is not found and error occurs None is returned

        """
        self._log.trace("Attempting to load class [{0}]".format(className), trace=True)
        for path in self._log.getConfig().get('Import', 'searchPath'):
            self._log.trace("Searching path [{0}]".format(path), trace=True)
            try:
                SearchModule = importlib.import_module(str(path))
            except ImportError as e:
                self._log.error("Failed to import module [{0}]".format(path), verbose=True)
                continue
            if className in dir(SearchModule):
                req = getattr(SearchModule, str(className))
                try:
                    instance = req()
                    return instance
                except AttributeError as e:
                    self._log.error(
                        "Failed to create instance of class [{0}] from module [{1}]".format(className, path)
                    )
                    continue
        return None
