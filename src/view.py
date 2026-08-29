from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Tuple

from .model import ChangeRequest, Member, Role, VoteChoice
from .service import SummaryReport


class ChangeRequestView(ABC):
    @abstractmethod
    def show_main_menu(self) -> str: ...

    @abstractmethod
    def render_members_and_requests(
        self, members: List[Member], requests: List[ChangeRequest]
    ) -> None: ...

    @abstractmethod
    def render_summary(self, summary: SummaryReport) -> None: ...

    @abstractmethod
    def show_success(self, message: str) -> None: ...

    @abstractmethod
    def show_error(self, reason: str) -> None: ...

    @abstractmethod
    def prompt_create_request_input(self) -> Tuple[str, str, Role]: ...

    @abstractmethod
    def prompt_vote_input(self) -> Tuple[str, str, VoteChoice]: ...

    @abstractmethod
    def prompt_cancel_input(self) -> Tuple[str, str]: ...


class ConsoleChangeRequestView(ChangeRequestView):
    MENU = """
 Friends Forever Change Request
=================================
 1) ดูสมาชิกและคำขอทั้งหมด
 2) สร้างคำขอเปลี่ยนบทบาท
 3) ลงความเห็นต่อคำขอ
 4) ยกเลิกคำขอ
 5) ดูสรุปผล
 0) ออกจากโปรแกรม
=================================
"""

    def show_main_menu(self) -> str:
        print(self.MENU)
        return input("เลือกเมนู: ").strip()

    def render_members_and_requests(self, members, requests) -> None:
        print("\n-- รายชื่อสมาชิก --")
        print(f"{'ID':<6}{'ชื่อ':<20}{'บทบาทปัจจุบัน':<15}{'Active':<8}")
        for m in members:
            print(f"{m.id:<6}{m.name:<20}{m.role.value:<15}{str(m.active):<8}")

        print("\n-- คำขอเปลี่ยนบทบาททั้งหมด --")
        print(
            f"{'ID':<6}{'ผู้เสนอ':<10}{'เป้าหมาย':<10}{'บทบาทใหม่':<12}"
            f"{'สถานะ':<12}{'อนุมัติ':<8}{'ไม่อนุมัติ':<10}"
        )
        for r in requests:
            print(
                f"{r.id:<6}{r.requester_id:<10}{r.target_id:<10}{r.new_role.value:<12}"
                f"{r.status.value:<12}{r.count_approve():<8}{r.count_reject():<10}"
            )
        print()

    def render_summary(self, summary: SummaryReport) -> None:
        def _print_group(title, items):
            print(f"\n-- {title} ({len(items)}) --")
            for r in items:
                print(
                    f"  {r.id}: {r.requester_id} -> {r.target_id} เป็น {r.new_role.value} "
                    f"(อนุมัติ {r.count_approve()} / ไม่อนุมัติ {r.count_reject()})"
                )

        print("\n===== สรุปผลคำขอ =====")
        _print_group("รอพิจารณา", summary.pending)
        _print_group("อนุมัติแล้ว", summary.approved)
        _print_group("ไม่อนุมัติ", summary.rejected)
        _print_group("ยกเลิก", summary.cancelled)

        print("\n-- บทบาทปัจจุบันของสมาชิก --")
        for m in summary.members:
            print(f"  {m.id} {m.name}: {m.role.value}")
        print()

    def show_success(self, message: str) -> None:
        print(f"[สำเร็จ] {message}")

    def show_error(self, reason: str) -> None:
        print(f"[ปฏิเสธ] {reason}")

    def prompt_create_request_input(self):
        requester_id = input("ผู้เสนอ (memberId เช่น M01): ").strip().upper()
        target_id = input("สมาชิกเป้าหมาย (memberId เช่น M02): ").strip().upper()
        role_choices = ", ".join(r.value for r in Role)
        role_str = input(f"บทบาทใหม่ ({role_choices}): ").strip().upper()
        new_role = Role(role_str)
        return requester_id, target_id, new_role

    def prompt_vote_input(self):
        request_id = input("รหัสคำขอ (เช่น C01): ").strip().upper()
        member_id = input("รหัสสมาชิกผู้ลงความเห็น (เช่น M04): ").strip().upper()
        choice_str = input("ความเห็น (APPROVE/REJECT): ").strip().upper()
        choice = VoteChoice(choice_str)
        return request_id, member_id, choice

    def prompt_cancel_input(self):
        request_id = input("รหัสคำขอที่ต้องการยกเลิก: ").strip().upper()
        requester_id = input("รหัสสมาชิกผู้เสนอ (เพื่อยืนยันสิทธิ์): ").strip().upper()
        return request_id, requester_id
