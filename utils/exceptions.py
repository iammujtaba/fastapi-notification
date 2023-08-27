

class FilterKeyNotPresent(Exception):
    def __init__(self, message="Key provided does not exists."):
        super().__init__(message)


class ValidationError(Exception):
    def __init__(self, message="Something went wrong."):
        super().__init__(message)

class MultipleRecordFoundError(Exception):
    def __init__(self, message="Expecting 1 but queryset return multiple records"):
        super().__init__(message)

class DataNotProvidedException(Exception):
    def __init__(self, message="Data can not be empty."):
        super().__init__(message)

class FilterOperatorNotPresent(Exception):
    def __init__(self, message="Filter operator not provided."):
        super().__init__(message)
