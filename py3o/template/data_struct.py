class Py3oDataError(Exception):
    pass


class Py3oObject(dict):
    """ Mother class to be inherited.
    """
    def __repr__(self):  # pragma: no cover
        res = super(Py3oObject, self).__repr__()
        return self.__class__.__name__ + "(" + res + ")"


class Py3oModule(Py3oObject):
    def jsonify(self, data):
        """ This function will render the datastruct according
         to the user's data
        :param data: User data to use for jsonification
        :return: dict
        """
        res = {}
        for key, value in self.items():
            subdata = data.get(key, None)
            if subdata is None:
                raise Py3oDataError(
                    "The key '%s' must be present"
                    " in your data dictionary" % key
                )
            # Spread only the appropriate data to its children
            val = value.jsonify(data.get(key))
            if val:
                res[key] = val
        return res


class Py3oArray(Py3oObject):
    """ A class representing an array.
    The attribute direct_access will tell if this class should be considered
     as a list of dict or a list of values.
    """
    def __init__(self):
        super(Py3oArray, self).__init__()
        self.direct_access = False

    def jsonify(self, data):
        """ This function will render the datastruct according
        to the user's data
        :return: a list of values or a list of Py3oObject
        """
        if self.direct_access:
            return data
        if not self:
            return None
        res = []
        for d in data:
            tmp_dict = {}
            for key, value in self.items():
                # Spread only the appropriate data to its children
                tmp_dict[key] = value.jsonify(getattr(d, key))
            res.append(tmp_dict)
        return res


class Py3oBuiltin(Py3oObject):
    """ This class holds information about builtins
    """
    pass


class Py3oName(Py3oObject):
    """ This class holds information of variables.
    Keys are attributes and values the type of this attribute
     (another Py3o class or a simple value)
    i.e.: i.egg -> Py3oName({'i': Py3oName({'egg': Py3oName({})})})
    """
    def jsonify(self, data):
        """ This function will render the datastruct according
        to the user's data
        :param data: the value to apply on the instance
        :return:
        """
        if not self:
            return data
        res = {}

        for key, value in self.items():
            # Spread only the appropriate data to its children
            res[key] = value.jsonify(getattr(data, key))
        return res


class Py3oDummy(Py3oObject):
    """ This class holds unused defined attribute,
     such as counters from enumerate()
    """
    pass
