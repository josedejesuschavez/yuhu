from shared.domain.string_value_object import StringValueObject


class TaskDescription(StringValueObject):

    def __init__(self, value):
        super().__init__(value)
