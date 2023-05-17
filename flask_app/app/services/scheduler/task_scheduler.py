from typing import Callable

from apscheduler.schedulers.background import BackgroundScheduler


class TaskScheduler:
    def __init__(
            self,
            task: Callable,
            **trigger_args
    ):
        self.scheduler = BackgroundScheduler()
        self.task = task
        self.trigger_args = trigger_args

    def start_scheduler(self):
        self.scheduler.add_job(
            id='update_subscribers',
            func=self.task,
            trigger='cron',
            **self.trigger_args
            # day='*',
            # hour=12,
        )
        self.scheduler.start()
