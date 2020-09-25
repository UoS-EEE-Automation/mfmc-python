class RequiredDatafieldError(KeyError):
    """A required datafield_name was not found.

    Args:
        name: The key name which was attempted to be accessed.
    """

    def __init__(self, name: str) -> None:
        msg = f"Required datafield_name not found: {name}"
        super().__init__(msg)


class OptionalDatafieldError(KeyError):
    """An optional datafield_name was not found.

    Args:
        name: The key name which was attempted to be accessed.
    """

    def __init__(self, name: str) -> None:
        msg = f"Optional datafield_name not found: {name}"
        super().__init__(msg)


class UnknownDatafieldError(KeyError):
    """A user-defined datafield_name was accessed incorrectly.

    User attributes should be accessed using the ``user_attributes`` property,
    and user datasets should be accessed using the ``user_datasets`` property.

    Args:
        name: The key name which was attempted to be accessed.
    """

    def __init__(self, name: str) -> None:
        msg = f"Unknown datafield_name not found: {name}"
        super().__init__(self, msg)
