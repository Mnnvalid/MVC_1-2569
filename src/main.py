from __future__ import annotations

import os

from .controller import ChangeRequestController
from .seed_loader import SeedDataLoader
from .service import ChangeRequestService
from .view import ConsoleChangeRequestView


def main() -> None:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    seed_path = os.path.join(project_root, "seed_data.json")

    member_repo, request_repo = SeedDataLoader.load(seed_path)
    service = ChangeRequestService(member_repo, request_repo)
    view = ConsoleChangeRequestView()
    controller = ChangeRequestController(service, view)
    controller.run()


if __name__ == "__main__":
    main()
