from collections import OrderedDict


class Menu(OrderedDict):
    def __init__(self, data):
        super(Menu, self).__init__(data)
        self.current = None

    @property
    def width(self):
        return sum([max(50, len(v['title'])*10+15) for k, v in self.items()])

    def __str__(self):
        return 'menu'
