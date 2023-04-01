from typing import Any


class Executable:
    def execute(self, subject: Any, target: Any, action: str, context: Any):
        ...