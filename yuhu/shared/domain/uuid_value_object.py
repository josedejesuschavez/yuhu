import uuid

from shared.domain.invalid_argument_error import InvalidArgumentError
from shared.domain.value_object import ValueObject, Primitives


class UuidValueObject(ValueObject[str]):

    def __init__(self, value):
        super().__init__(value)
        self.validate_is_uuid()

    def validate_is_uuid(self):
        try:
            uuid_obj = uuid.UUID(self.value)
        except ValueError:
            raise InvalidArgumentError(message=f"'{self.value}' is not a valid UUID.")

    def equals(self, other: 'ValueObject[Primitives]') -> bool:
        if not isinstance(other, UuidValueObject):
            return False
        return self.value == other.value