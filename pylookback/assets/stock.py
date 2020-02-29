from .asset import Asset


class Stock(Asset):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def revalue(self):
        pass
