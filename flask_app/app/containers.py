from dependency_injector import containers, providers

from app.repository.item.impl_item_repository import ImplItemRepository
from app.repository.item.item_repository import ItemRepository
from app.repository.price_history.impl_price_history_repository import ImplPriceHistoryRepository
from app.repository.price_history.price_history_repository import PriceHistoryRepository
from app.services.ceneo import ceneo_item_interface
import app.services.item.item_service
from app.services.ceneo.ceneo_item import CeneoItem


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.controllers.products.routes",
            "app.controllers.subscriptions.routes",
        ]
    )

    ceneo_item: ceneo_item_interface.CeneoItemInterface = providers.Singleton(
        CeneoItem,
    )

    item_repository: ItemRepository = providers.Singleton(
        ImplItemRepository
    )

    price_hist_repository: PriceHistoryRepository = providers.Singleton(
        ImplPriceHistoryRepository
    )

    item_service: app.services.item.item_service.ItemService = providers.Singleton(
        app.services.item.item_service.ItemService,
        ceneo_item_interface=ceneo_item,
        item_repository=item_repository,
        price_history_repository=price_hist_repository
    )

