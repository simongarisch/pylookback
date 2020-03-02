from .asset import Asset


class Stock(Asset):
    def _revalue(self):
        self._local_value = self._price
