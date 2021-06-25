# -*- coding: utf-8 -*-

from abc import abstractmethod


class BaseWorker:

    @abstractmethod
    def start(self, *args, **kwargs):
        ...

    @abstractmethod
    def stop(self, *args, **kwargs):
        ...
