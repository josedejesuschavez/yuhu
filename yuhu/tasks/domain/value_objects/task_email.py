import re

from shared.domain.invalid_argument_error import InvalidArgumentError
from shared.domain.string_value_object import StringValueObject


class TaskEmail(StringValueObject):

    def __init__(self, value: str):
        super().__init__(value)
        self.validate_is_email()

    def validate_is_email(self) -> None:
        if not self.is_valid_email(self.value):
            raise InvalidArgumentError(message=f"'{self.value}' is not a valid email address.")

    @staticmethod
    def is_valid_email(email: str) -> bool:
        email_regex = re.compile(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        )
        return re.match(email_regex, email) is not None