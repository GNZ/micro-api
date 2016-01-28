from abc import ABCMeta, abstractmethod


class AnalysisType:
    __metaclass__ = ABCMeta

    @abstractmethod
    def analyse(self, **kwargs): pass
