from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .model import (
    BusinessRuleViolationException,
    ChangeRequest,
    Member,
    Role,
    RequestStatus,
    VoteChoice,
)
from .repository import ChangeRequestRepository, MemberRepository


@dataclass
class SummaryReport:
    pending: List[ChangeRequest] = field(default_factory=list)
    approved: List[ChangeRequest] = field(default_factory=list)
    rejected: List[ChangeRequest] = field(default_factory=list)
    cancelled: List[ChangeRequest] = field(default_factory=list)
    members: List[Member] = field(default_factory=list)


class ChangeRequestService:
    def __init__(self, member_repo: MemberRepository, request_repo: ChangeRequestRepository):
        self._member_repo = member_repo
        self._request_repo = request_repo

    def get_members(self) -> List[Member]:
        return self._member_repo.find_all()

    def get_all_requests(self) -> List[ChangeRequest]:
        return self._request_repo.find_all()

    def create_request(self, requester_id: str, target_id: str, new_role: Role) -> ChangeRequest:
        requester = self._member_repo.find_by_id(requester_id)
        target = self._member_repo.find_by_id(target_id)
        if requester is None:
            raise BusinessRuleViolationException(f"ไม่พบสมาชิกที่เสนอ '{requester_id}'")
        if target is None:
            raise BusinessRuleViolationException(f"ไม่พบสมาชิกเป้าหมาย '{target_id}'")
        if requester_id == target_id:
            raise BusinessRuleViolationException("ผู้เสนอไม่สามารถเป็นสมาชิกเป้าหมายของคำขอตนเองได้")
        if self._request_repo.has_pending_for_target(target_id):
            raise BusinessRuleViolationException(
                f"สมาชิกเป้าหมาย '{target_id}' มีคำขอที่ยัง 'รอพิจารณา' อยู่แล้ว 1 คำขอ"
            )

        new_request = ChangeRequest(
            id=self._request_repo.next_id(),
            requester_id=requester_id,
            target_id=target_id,
            new_role=new_role,
        )
        self._request_repo.add(new_request)
        return new_request

    def cast_vote(self, request_id: str, member_id: str, choice: VoteChoice) -> ChangeRequest:
        request = self._request_repo.find_by_id(request_id)
        if request is None:
            raise BusinessRuleViolationException(f"ไม่พบคำขอ '{request_id}'")
        if not request.is_pending():
            raise BusinessRuleViolationException(
                f"คำขอ '{request_id}' สิ้นสุดแล้ว ({request.status.value}) ไม่สามารถลงความเห็นเพิ่มได้"
            )

        member = self._member_repo.find_by_id(member_id)
        if member is None:
            raise BusinessRuleViolationException(f"ไม่พบสมาชิก '{member_id}'")
        if not member.is_active():
            raise BusinessRuleViolationException(f"สมาชิก '{member_id}' ไม่ได้อยู่ในสถานะ Active")
        if member_id == request.requester_id:
            raise BusinessRuleViolationException("ผู้เสนอคำขอไม่มีสิทธิ์ลงความเห็นต่อคำขอของตนเอง")
        if member_id == request.target_id:
            raise BusinessRuleViolationException("สมาชิกเป้าหมายไม่มีสิทธิ์ลงความเห็นต่อคำขอของตนเอง")
        if request.has_voted(member_id):
            raise BusinessRuleViolationException(f"สมาชิก '{member_id}' เคยลงความเห็นต่อคำขอนี้ไปแล้ว")

        request.add_decision(member_id, choice)
        self._resolve_if_decided(request)
        return request

    def _resolve_if_decided(self, request: ChangeRequest) -> None:
        if request.count_approve() >= 2:
            request.mark_approved()
            target = self._member_repo.find_by_id(request.target_id)
            target.change_role(request.new_role)
        elif request.count_reject() >= 2:
            request.mark_rejected()

    def cancel_request(self, request_id: str, requester_id: str) -> ChangeRequest:
        request = self._request_repo.find_by_id(request_id)
        if request is None:
            raise BusinessRuleViolationException(f"ไม่พบคำขอ '{request_id}'")
        if request.requester_id != requester_id:
            raise BusinessRuleViolationException("เฉพาะผู้เสนอคำขอเท่านั้นที่ยกเลิกคำขอนี้ได้")
        if not request.is_pending():
            raise BusinessRuleViolationException(
                f"คำขอ '{request_id}' สิ้นสุดแล้ว ({request.status.value}) ไม่สามารถยกเลิกได้"
            )
        if len(request.decisions) > 0:
            raise BusinessRuleViolationException("มีสมาชิกลงความเห็นต่อคำขอนี้แล้ว ไม่สามารถยกเลิกได้")

        request.mark_cancelled()
        return request

    def get_summary(self) -> SummaryReport:
        summary = SummaryReport(members=self._member_repo.find_all())
        for r in self._request_repo.find_all():
            if r.status == RequestStatus.PENDING:
                summary.pending.append(r)
            elif r.status == RequestStatus.APPROVED:
                summary.approved.append(r)
            elif r.status == RequestStatus.REJECTED:
                summary.rejected.append(r)
            elif r.status == RequestStatus.CANCELLED:
                summary.cancelled.append(r)
        return summary
