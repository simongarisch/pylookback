from weakref import WeakSet


OBSERVER_METHOD = "msg_from_observable"


class Observable:
    def __init__(self):
        self._observers = WeakSet()

    def add_observer(self, observer):
        self._observers.add(observer)
        if not hasattr(observer, OBSERVER_METHOD):
            raise AttributeError(
                "observer requires method %s" % OBSERVER_METHOD
            )

    def remove_observer(self, observer):
        self._observers.discard(observer)

    def notify_observers(self):
        for observer in self._observers:
            method = getattr(observer, OBSERVER_METHOD)
            method(self)
