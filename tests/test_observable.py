from pylookback.observable import Observable


class Observer:
    is_updated = False

    def observable_update(self, observable):
        self.is_updated = True


def test_observable_add_remove():
    observable = Observable()
    assert len(observable._observers) == 0
    observer1 = Observer()
    observer2 = Observer()

    observable.add_observer(observer1)
    assert len(observable._observers) == 1

    observable.add_observer(observer2)
    assert len(observable._observers) == 2

    observable.remove_observer(observer1)
    assert len(observable._observers) == 1
    assert list(observable._observers) == [observer2]

    del observer2
    assert len(observable._observers) == 0  # should be weak set


def test_observable_messaging():
    observer = Observer()

    observable = Observable()
    observable.add_observer(observer)
    assert observer.is_updated is False
    observable.notify_observers()
    assert observer.is_updated is True
