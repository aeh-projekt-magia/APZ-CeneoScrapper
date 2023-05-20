from dependency_injector import containers, providers

from app.repository.item.impl_item_repository import ImplItemRepository
from app.repository.item.item_repository import ItemRepository
from app.repository.price_history.impl_price_history_repository import ImplPriceHistoryRepository
from app.repository.price_history.price_history_repository import PriceHistoryRepository
from app.services.ceneo import ceneo_item_interface
import app.services.item.item_service
from app.services.ceneo.ceneo_item import CeneoItem
from app.services.emails.email_sender import EmailSender
from app.services.scheduler.tasks import Tasks
from app.services.scheduler.task_scheduler import TaskScheduler
from app.services.subscription.subscription_service import SubscriptionService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.controllers.products.routes",
            "app.controllers.scheduler.routes",
        ]
    )

    config = providers.Configuration(ini_files=["config.ini"])

    ceneo_item: ceneo_item_interface.CeneoItemInterface = providers.Singleton(
        CeneoItem,
    )

    item_repository: ItemRepository = providers.Singleton(
        ImplItemRepository
    )

    price_hist_repository: PriceHistoryRepository = providers.Singleton(
        ImplPriceHistoryRepository
    )

    email_service: EmailSender = providers.Singleton(
        EmailSender
    )

    item_service: app.services.item.item_service.ItemService = providers.Singleton(
        app.services.item.item_service.ItemService,
        ceneo_item_interface=ceneo_item,
        item_repository=item_repository,
        price_history_repository=price_hist_repository
    )

    subscription_service: SubscriptionService = providers.Singleton(
        SubscriptionService,
    )

    tasks = providers.Singleton(
        Tasks,
        item_service=item_service,
        subscription_service=subscription_service,
        email_service=email_service,
    )

    task_scheduler: TaskScheduler = providers.Singleton(
        TaskScheduler,
        tasks=tasks,
        day=config.task_scheduler.day,
        hour=config.task_scheduler.hour,
        minute=config.task_scheduler.minute,
    )
