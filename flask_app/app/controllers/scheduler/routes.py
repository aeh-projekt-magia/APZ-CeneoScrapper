from dependency_injector.wiring import inject, Provide
from flask_login import login_required
from app.services.scheduler.task_scheduler import TaskScheduler
from app.containers import Container
from app.controllers.scheduler import bp

import traceback
import sys

from app.services.decorators import (
    admin_user_required,
    confirmed_user_required,
)


@bp.route("/start", methods=["POST"])
@login_required
@admin_user_required
@confirmed_user_required
@inject
def start_scheduler(scheduler: TaskScheduler = Provide[Container.task_scheduler]):
    try:
        scheduler.start_scheduler()
        return "SCHEDULER STARTED\n\n" + scheduler.describe_tasks()
    except Exception:
        return (
            f"SCHEDULER NOT STARTED\n\n"
            f"{traceback.format_exc()}\n\n"
            f"{sys.exc_info()[2]}"
        )


@bp.route("/stop", methods=["POST"])
@login_required
@admin_user_required
@confirmed_user_required
@inject
def stop_scheduler(scheduler: TaskScheduler = Provide[Container.task_scheduler]):
    try:
        scheduler.stop_scheduler()
        return "SCHEDULER STOPPED\n\n" + scheduler.describe_tasks()
    except Exception:
        return (
            f"SCHEDULER NOT STOPPED\n\n"
            f"{traceback.format_exc()}\n\n"
            f"{sys.exc_info()[2]}"
        )
