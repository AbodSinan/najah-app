from enums import Enum

class PaymentType(Enum):
    CASH = 1

class PaymentStatus(Enum):
    INITIATED = 10
    PENDING = 20
    PAID = 30
    CANCELLED = -10