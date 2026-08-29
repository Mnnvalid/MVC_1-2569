# SUBMISSION - Exit Exam MVC 1/2569 (เสาร์บ่าย)

## 1. วิธีเปิดโปรแกรม
- ภาษา/เฟรมเวิร์ก: python
- Entry point / คำสั่งเปิดโปรแกรม: python run.py
- หมายเหตุที่จำเป็น (ถ้ามี): 

## 2. ตารางเชื่อมโยง Requirements

| Requirement | Model / Domain | Controller / Action | View / Screen |
|---|---|---|---|
| R1 | Role, RequestStatus, VoteChoice (enum); Member, ChangeRequest, Decision (entity); MemberRepository, ChangeRequestRepository; SeedDataLoader| main.py, run.py, ChangeRequestController| ChangeRequestView (interface), ConsoleChangeRequestView (เมนูหลัก + ทุกหน้าจอ)|
| R2 | Member, MemberRepository.findAll(); ChangeRequest, ChangeRequestRepository.hasPendingForTarget(); ChangeRequestService.getMembers(), getAllRequests(), createRequest()| ChangeRequestController.viewMembersAndRequests(), createChangeRequest()| ConsoleChangeRequestView.renderMembersAndRequests(), promptCreateRequestInput()|
| R3 | Member.isActive(); ChangeRequest.hasVoted(), isPending(); Decision, VoteChoice; ChangeRequestService.castVote()| ChangeRequestController.castVote()| ConsoleChangeRequestView.promptVoteInput(), showSuccess() / showError()|
| R4 | ChangeRequest.countApprove(), countReject(), markApproved(), markRejected(); Member.changeRole(); ChangeRequestService.resolveIfDecided() (เรียกอัตโนมัติต่อจาก castVote() ทันทีที่ครบ 2 เสียง ไม่รอเสียงที่ 3)| ChangeRequestController.castVote()| ConsoleChangeRequestView.showSuccess() (แจ้งสถานะคำขอใหม่และบทบาทที่เปลี่ยน)|
| R5 | ChangeRequestService.cancelRequest() (ตรวจ PENDING และที่ยังไม่มีผู้ลงความเห็น), ChangeRequest.markCancelled(); ChangeRequestService.getSummary(), SummaryReport; BusinessRuleViolationException (ใช้ร่วมกันกับการปฏิเสธทุกกรณีใน R2-R5)| ChangeRequestController.cancelRequest(), viewSummary()| ConsoleChangeRequestView.renderSummary(), showError()|

## 3. ผลการทดสอบ

| กรณี | ผ่าน/ไม่ผ่าน | หมายเหตุ (เฉพาะที่จำเป็น) |
|---|---|---|
| T1 | ผ่าน| |
| T2 | ผ่าน| |
| T3 | ผ่าน| |
| T4 | ผ่าน| |
| T5 | ผ่าน| |
| T6 | ผ่าน| |

## 4. ความแตกต่างระหว่างแบบที่ออกกับโปรแกรมจริง (ถ้ามี)
ระบุไม่เกิน 3 ข้อ
1. 
2. 
3. 

## 5. บันทึกการใช้ Generative AI
หากไม่ได้ใช้ ให้ระบุ **ไม่ได้ใช้ Generative AI**

| เวลาโดยประมาณ | เครื่องมือ | ใช้เพื่ออะไร | นำคำแนะนำไปใช้อย่างไร |
|---|---|---|---|
| 13.42 น.| Gemini| รวบรวมข้อมูลเงื่อนไขที่กระจายอยู่แต่ละจุดของโจทย์ให้มารวมกันจะอ่านง่ายๆ เห็นได้ชัดเจน| เอามาใช้สร้างโปรแกรมและdiagramให้ครอบคลุมกับ req และเงื่อนไขที่โจทย์กำหนด|
| | | | |
| | | | |