from dataclasses import dataclass


@dataclass(frozen=True)
class CommentsValidationRule:
    TEXT_MAX_LENGTH = 255
    TEXT_MIN_LENGTH = 1
