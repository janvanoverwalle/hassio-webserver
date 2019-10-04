""" HTTP Methods module """


class HttpMethods(object):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'

    @classmethod
    def equals(cls, method1, method2):
        return method1.upper() == method2.upper()

    @classmethod
    def is_get(cls, method):
        return cls.equals(method, cls.GET)

    @classmethod
    def is_post(cls, method):
        return cls.equals(method, cls.POST)

    @classmethod
    def is_put(cls, method):
        return cls.equals(method, cls.PUT)

    @classmethod
    def is_delete(cls, method):
        return cls.equals(method, cls.DELETE)
