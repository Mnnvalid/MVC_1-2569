from __future__ import annotations

import json
from typing import Tuple

from .model import ChangeRequest, Member, Role, RequestStatus, VoteChoice
from .repository import ChangeRequestRepository, MemberRepository

class SeedDataLoader:
    @staticmethod
    def load(path: str) -> Tuple[MemberRepository, ChangeRequestRepository]:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        members = [
            Member(id=m["id"], name=m["name"], role=Role(m["role"]), active=m["active"])
            for m in data["members"]
        ]
        member_repo = MemberRepository(members)

        requests = [
            ChangeRequest(
                id=r["id"],
                requester_id=r["requester_id"],
                target_id=r["target_id"],
                new_role=Role(r["new_role"]),
                status=RequestStatus(r["status"]),
            )
            for r in data["role_change_requests"]
        ]
        request_repo = ChangeRequestRepository(requests)

        for d in data.get("decisions", []):
            request = request_repo.find_by_id(d["request_id"])
            if request is not None:
                request.add_decision(d["member_id"], VoteChoice(d["result"]))

        return member_repo, request_repo
