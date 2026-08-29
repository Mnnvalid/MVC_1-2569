
from __future__ import annotations

from .model import BusinessRuleViolationException, RequestStatus
from .service import ChangeRequestService
from .view import ChangeRequestView


class ChangeRequestController:
    def __init__(self, service: ChangeRequestService, view: ChangeRequestView):
        self._service = service
        self._view = view

    def run(self) -> None:
        actions = {
            "1": self.view_members_and_requests,
            "2": self.create_change_request,
            "3": self.cast_vote,
            "4": self.cancel_request,
            "5": self.view_summary,
        }
        while True:
            choice = self._view.show_main_menu()
            if choice == "0":
                print("ออกจากโปรแกรม")
                break
            action = actions.get(choice)
            if action is None:
                self._view.show_error("เมนูไม่ถูกต้อง กรุณาเลือกใหม่")
                continue
            try:
                action()
            except BusinessRuleViolationException as e:
                self._view.show_error(e.reason)
            except (ValueError, KeyError) as e:
                self._view.show_error(f"ข้อมูลไม่ถูกต้อง: {e}")

    def view_members_and_requests(self) -> None:
        members = self._service.get_members()
        requests = self._service.get_all_requests()
        self._view.render_members_and_requests(members, requests)

    def create_change_request(self) -> None:
        requester_id, target_id, new_role = self._view.prompt_create_request_input()
        request = self._service.create_request(requester_id, target_id, new_role)
        self._view.show_success(f"สร้างคำขอ {request.id} สำเร็จ อยู่ในสถานะ 'รอพิจารณา'")

    def cast_vote(self) -> None:
        request_id, member_id, choice = self._view.prompt_vote_input()
        request = self._service.cast_vote(request_id, member_id, choice)
        if request.status == RequestStatus.APPROVED:
            self._view.show_success(
                f"คำขอ {request.id} ได้รับอนุมัติแล้ว และเปลี่ยนบทบาทของสมาชิก "
                f"{request.target_id} เป็น {request.new_role.value}"
            )
        elif request.status == RequestStatus.REJECTED:
            self._view.show_success(
                f"คำขอ {request.id} ไม่ได้รับอนุมัติ บทบาทของสมาชิก {request.target_id} ไม่เปลี่ยนแปลง"
            )
        else:
            self._view.show_success(f"บันทึกความเห็นต่อคำขอ {request.id} สำเร็จ (ยังรอความเห็นเพิ่มเติม)")

    def cancel_request(self) -> None:
        request_id, requester_id = self._view.prompt_cancel_input()
        request = self._service.cancel_request(request_id, requester_id)
        self._view.show_success(f"ยกเลิกคำขอ {request.id} สำเร็จ")

    def view_summary(self) -> None:
        summary = self._service.get_summary()
        self._view.render_summary(summary)
