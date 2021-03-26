"""Dispatcher class to aid serializing and deserializing classes to JSON

Original code from: https://stackoverflow.com/a/51976115
"""
import abc
import logging
from typing import Dict

logger = logging.getLogger(__name__)


class JsonSerializable(abc.ABC):
    @abc.abstractmethod
    def as_dict(self) -> Dict:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, data):
        raise NotImplementedError


class _Dispatcher:
    def __init__(self, classname_key="__class__"):
        self._key = classname_key
        self._classes = {}

    def __call__(self, class_):  # Called when wrapped class is decorated
        if not issubclass(class_, JsonSerializable):
            raise TypeError("dispatched class must subclass JsonSerializable")
        self._classes[class_.__name__] = class_
        return class_

    def decoder_hook(self, d):
        """Decodes dictionary into original classes

        Args:
            d: JSON dictionary

        Returns: Remaining JSON
        """
        classname = d.pop(self._key, None)
        if classname:
            logger.debug("%s %s", classname, d)
            return self._classes[classname].from_dict(d)
        return d

    def encoder_default(self, obj):
        d = obj.as_dict()
        d[self._key] = type(obj).__name__
        return d


dispatcher = _Dispatcher()

if __name__ == "__main__":
    import json

    @dispatcher
    class Parent(JsonSerializable):
        def __init__(self, name):
            self.name = name

        def as_dict(self):
            return {"name": self.name}

        @classmethod
        def from_dict(cls, kwargs):
            return cls(name=kwargs["name"])

    s = json.dumps(Parent("test"), default=dispatcher.encoder_default)
    print(s)

    print(json.loads(s, object_hook=dispatcher.decoder_hook))
