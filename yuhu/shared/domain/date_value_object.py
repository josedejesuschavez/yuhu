from datetime import datetime

from shared.domain.value_object import ValueObject, Primitives


class DateValueObject(ValueObject[int]):

    def __init__(self, value: int):
        super().__init__(value)

    def equals(self, other: 'ValueObject[Primitives]') -> bool:
        if not isinstance(other, DateValueObject):
            return False
        return self.value == other.value

    def from_timestamp(self) -> datetime:
        return datetime.fromtimestamp(self.value)
