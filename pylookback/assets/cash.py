from .asset import Asset


class Cash(Asset):

    def revalue(self):
        self.local_value = 1.0
