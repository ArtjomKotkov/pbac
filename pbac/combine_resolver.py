from typing import Iterable

from const import *


class CombineResolver:

    @staticmethod
    def combine(algorithm: Algorithm, items: Iterable[Effect]):
        match algorithm:
            case Algorithm.PERMIT_UNLESS_DENY:
                return CombineResolver._permit_unless_deny(items)
            case Algorithm.DENY_UNLESS_PERMIT:
                return CombineResolver._deny_unless_permit(items)
            case Algorithm.PERMIT_OVERRIDES:
                return CombineResolver._permit_overrides(items)
            case Algorithm.DENY_OVERRIDES:
                return CombineResolver._deny_overrides(items)

    @staticmethod
    def _permit_unless_deny(items: Iterable[Effect]) -> Effect:
        deny = next((item for item in items if item == Effect.DENY), None)

        return Effect.PERMIT if deny is None else Effect.DENY

    @staticmethod
    def _deny_unless_permit(items: Iterable[Effect]) -> Effect:
        permit = next((item for item in items if item == Effect.PERMIT), None)

        return Effect.DENY if permit is None else Effect.PERMIT

    @staticmethod
    def _permit_overrides(items: Iterable[Effect]) -> Effect:
        permit = next((item for item in items if item == Effect.PERMIT), None)
        if permit is not None:
            return Effect.PERMIT

        deny = next((item for item in items if item == Effect.DENY), None)
        if deny is not None:
            return Effect.DENY

        return Effect.NOT_APPLICABLE

    @staticmethod
    def _deny_overrides(items: Iterable[Effect]) -> Effect:
        deny = next((item for item in items if item == Effect.DENY), None)
        if deny is not None:
            return Effect.DENY

        permit = next((item for item in items if item == Effect.PERMIT), None)
        if permit is not None:
            return Effect.PERMIT

        return Effect.NOT_APPLICABLE
