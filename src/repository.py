from __future__ import annotations

from typing import List, Optional

from .model import ChangeRequest, Member, RequestStatus

class MemberRepository:
    def __init__(self, members: List[Member]):
        self._members = members

    def find_all(self) -> List[Member]:
        return list(self._members)

    def find_by_id(self, member_id: str) -> Optional[Member]:
        for m in self._members:
            if m.id == member_id:
                return m
        return None

class ChangeRequestRepository:
    def __init__(self, requests: List[ChangeRequest]):
        self._requests = requests

    def find_all(self) -> List[ChangeRequest]:
        return list(self._requests)

    def find_by_id(self, request_id: str) -> Optional[ChangeRequest]:
        for r in self._requests:
            if r.id == request_id:
                return r
        return None

    def has_pending_for_target(self, target_id: str) -> bool:
        return any(
            r.target_id == target_id and r.status == RequestStatus.PENDING
            for r in self._requests
        )

    def add(self, request: ChangeRequest) -> None:
        self._requests.append(request)

    def next_id(self) -> str:
        max_num = 0
        for r in self._requests:
            if r.id.startswith("C") and r.id[1:].isdigit():
                max_num = max(max_num, int(r.id[1:]))
        return f"C{max_num + 1:02d}"
