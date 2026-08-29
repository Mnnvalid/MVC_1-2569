from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List

class Role(Enum):
    PRODUCER = "PRODUCER"
    FINANCE = "FINANCE"
    EDITOR = "EDITOR"
    CREATOR = "CREATOR"

class RequestStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"

class VoteChoice(Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"

class BusinessRuleViolationException(Exception):
    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason

@dataclass
class Member:
    id: str
    name: str
    role: Role
    active: bool = True

    def is_active(self) -> bool:
        return self.active

    def change_role(self, new_role: Role) -> None:
        self.role = new_role

@dataclass
class Decision:
    member_id: str
    choice: VoteChoice

@dataclass
class ChangeRequest:
    id: str
    requester_id: str
    target_id: str
    new_role: Role
    status: RequestStatus = RequestStatus.PENDING
    decisions: List[Decision] = field(default_factory=list)

    def is_pending(self) -> bool:
        return self.status == RequestStatus.PENDING

    def has_voted(self, member_id: str) -> bool:
        return any(d.member_id == member_id for d in self.decisions)

    def add_decision(self, member_id: str, choice: VoteChoice) -> None:
        self.decisions.append(Decision(member_id, choice))

    def count_approve(self) -> int:
        return sum(1 for d in self.decisions if d.choice == VoteChoice.APPROVE)

    def count_reject(self) -> int:
        return sum(1 for d in self.decisions if d.choice == VoteChoice.REJECT)

    def mark_approved(self) -> None:
        self.status = RequestStatus.APPROVED

    def mark_rejected(self) -> None:
        self.status = RequestStatus.REJECTED

    def mark_cancelled(self) -> None:
        self.status = RequestStatus.CANCELLED
