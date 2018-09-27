"""
Exceptions in COCS
"""


class COCSException(Exception):
    message = "An unknown exception occurred."

    def __init__(self, **kwargs):
        try:
            super(COCSException, self).__init__(self.message % kwargs)
            self.msg = self.message % kwargs
        except Exception:
            if not self.is_fatal_exception():
                super(COCSException, self).__init__(self.message)

    def __str__(self):
        return self.msg

    def is_fatal_exception(self):
        """
        When is fatal exception raise
        :return: return false
        """
        return False


class ResourceNotFound(COCSException):
    message = "Could not find %(resource_type)s: %(unique_key)s"

    def __init__(self, model, unique_key):
        resource_type = model.__name__.lower()
        super(ResourceNotFound, self).__init__(resource_type=resource_type,
                                               unique_key=unique_key)

class ResourceInUsing(COCSException):
    message = "Resource %(resource_type)s: %(unique_key)s is in using, " \
              "detail reason is %(reason)s"

    def __init__(self, model, unique_key, reason):
        resource_type = model.__name__.lower()
        super(ResourceInUsing, self).__init__(resource_type=resource_type,
                                              unique_key=unique_key,
                                              reason=reason)

class ResourceExist(COCSException):
    message = "Resource %(resource_type)s: %(unique_key)s exist"

    def __init__(self, model, unique_key):
        resource_type = model.__name__.lower()
        super(ResourceExist, self).__init__(resource_type=resource_type,
                                            unique_key=unique_key)


class ParamMissing(COCSException):
    message = "Param %(param_name)s is missing"

    def __init__(self, param_name):
        super(ParamMissing, self).__init__(param_name=param_name)


class RabbitMQClientDead(COCSException):
    message = "RabbitMQ client is not alive"
    def __init__(self):
        super(RabbitMQClientDead, self).__init__()


