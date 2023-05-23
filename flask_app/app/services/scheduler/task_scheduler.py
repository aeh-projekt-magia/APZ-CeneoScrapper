from apscheduler.schedulers.background import BackgroundScheduler

from app.services.scheduler.tasks import Tasks


class TaskScheduler:
    """
    Class responsible for scheduling the repetitive tasks
    """

    def __init__(self, tasks, **trigger_args):
        """
        Args:
            tasks: Class defining tasks to be scheduled
            **trigger_args: cron expressions for day, hour, minute
        """
        self.scheduler = BackgroundScheduler()
        self.tasks: Tasks = tasks
        self.trigger_args = trigger_args
        for task in self.tasks.get_tasks():
            self.scheduler.add_job(
                id=str(len(self.scheduler.get_jobs()) + 1),
                name=task.__name__,
                func=task,
                trigger="cron",
                **self.trigger_args,
            )

    def start_scheduler(self):
        self.scheduler.start()

    def stop_scheduler(self):
        self.scheduler.pause()

    def describe_tasks(self) -> str:
        tasks = "=" * 10 + "\n"
        for task in self.scheduler.get_jobs():
            tasks += (
                f"ID: {task.id}\t"
                f"NAME: {task.name}\t"
                f"NEXT RUN TIME: {task.next_run_time}\t"
                f"\n"
            )
        self.scheduler.print_jobs()
        return tasks
