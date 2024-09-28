from shared.domain.invalid_argument_error import InvalidArgumentError
from shared.domain.string_value_object import StringValueObject


class TaskTitle(StringValueObject):

    def __init__(self, value: str):
        super().__init__(value)
        self.validate_title_length()

    def validate_title_length(self) -> None:
        if len(self.value) > 100:
            raise InvalidArgumentError(
                message='The title cannot exceed 100 characters.',
                params={'value': self.value},
            )
