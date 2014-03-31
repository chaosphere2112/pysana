from asynclist import AsyncItem, AsyncList


class AsyncModel(object):
    """
        Map to a remote object, load attributes as needed
    """

    def __init__(self, id):
        self.id = id
        self.__async_attributes__ = {}

    def loader_for_attribute(self, attribute):
        """
            Subclasses should replace this function to implement
            actual object loading; this just returns the ID passed in.
        """
        return lambda x: x

    def map_attributes(self, attrs):
        for key in attrs:
            value = attrs[key]
            loader = self.loader_for_attribute(key)
            if hasattr(value, "__iter__"):
                #Iterable (non-string) value
                mapped = AsyncList(value, loader)
            else:
                #Plain value
                mapped = AsyncItem(value, loader)

            self.__async_attributes__[key] = mapped

    def __getattr__(self, name):
        if name in self.__async_attributes__:
            try:
                #Plain value
                return self.__async_attributes__[name].get()
            except AttributeError:
                #Iterable
                return self.__async_attributes__[name]
        else:
            raise AttributeError("'%s' object has no attribute '%s'" %
                                 (type(self), name))
