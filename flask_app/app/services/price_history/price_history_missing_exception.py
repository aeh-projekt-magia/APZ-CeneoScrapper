from shared.basic_exception import BasicException


class PriceHistoryMissingException(BasicException):
    """Throw when requested price history record does not exist"""
    ...
