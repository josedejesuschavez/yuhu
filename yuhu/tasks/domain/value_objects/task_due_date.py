from datetime import datetime
from typing import Optional

from shared.domain.date_value_object import DateValueObject
from shared.domain.invalid_argument_error import InvalidArgumentError
from shared.domain.value_object import Primitives


class TaskDueDate(DateValueObject):

    def __init__(self, value: int):
        super().__init__(value)
        self.validate_due_date()

    def validate_due_date(self) -> None:
        if self.value is None:
            return

        current_timestamp = int(datetime.now().timestamp())
        if self.value < current_timestamp:
            raise InvalidArgumentError(message=f"The due date '{self.value}' cannot be in the past.")

    def _ensure_value_is_defined(self, value: Optional[Primitives]) -> None:
        return None

    def from_timestamp(self) -> Optional[datetime]:
        if self.value is None:
            return None

        return datetime.fromtimestamp(self.value)
