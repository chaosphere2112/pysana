class AsyncIter(object):
    """
        Iterator that works on a list of async items,
        returning the fetched value of each item.
    """
    def __init__(self, asyncitems):
        self.items = asyncitems
        self.index = 0

    def next(self):
        if self.index == len(self.items):
            raise StopIteration
        item = self.items[self.index].get()
        self.index += 1
        return item

    def __iter__(self):
        return self


class AsyncItem(object):
    """
        Wrapper that will take an ID, and load the desired
        object when requested.
    """
    def __init__(self, item_id, loader):
        self.item = None
        self.item_id = item_id
        self.loader = loader

    def get(self):
        if self.item is None:
            self.item = self.loader(self.item_id)
        return self.item


class AsyncList(object):
    """
        List-like object that loads items as they are accessed
    """
    def __init__(self, ids, loader):
        """
            loader callable should take an id and return a fully-loaded
            version of whatever object.
        """
        self.__loader__ = loader
        self.__items__ = [AsyncItem(item_id, self.__loader__)
                          for item_id in ids]

    def __len__(self):
        return len(self.__items__)

    def __getitem__(self, key):
        item = self.__items__[key]
        return item.get()

    def __setitem__(self, key, item):
        self.__items__[key] = AsyncItem(item, self.__loader__)

    def __delitem__(self, key):
        del self.__items__[key]

    def __iter__(self):
        return AsyncIter(self.__items__)

    def __reversed__(self):
        new_list = []
        for item in self.__items__:
                new_list.insert(0, item.get())

        return new_list
