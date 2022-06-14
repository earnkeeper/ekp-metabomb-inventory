from decouple import AutoConfig
from ekp_sdk import BaseContainer

from app.features.inventory.player.inventory_controller import InventoryController
from app.features.inventory.player.inventory_service import InventoryService
from app.features.inventory.players.players_controller import InventoryPlayersController
from app.features.inventory.players.players_service import InventoryPlayersService

from shared.mapper_service import MapperService
from shared.metabomb_api_service import MetabombApiService
from shared.metabomb_coingecko_service import MetabombCoingeckoService
from shared.metabomb_moralis_service import MetabombMoralisService

class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig(".env")

        super().__init__(config)

        self.metabomb_coingecko_service = MetabombCoingeckoService(
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service
        )

        self.metabomb_api_service = MetabombApiService(
            cache_service=self.cache_service
        )
        #
        self.mapper_service = MapperService(
            cache_service=self.cache_service,
            metabomb_coingecko_service=self.metabomb_coingecko_service,
        )

        self.metabomb_moralis_service = MetabombMoralisService(
            cache_service=self.cache_service,
            moralis_api_service=self.moralis_api_service
        )

        # FEATURES - INVENTORY - PLAYERS

        self.inventory_players_service = InventoryPlayersService(
            metabomb_api_service=self.metabomb_api_service,
            metabomb_coingecko_service=self.metabomb_coingecko_service,
            metabomb_moralis_service=self.metabomb_moralis_service,
            mapper_service=self.mapper_service
        )

        self.inventory_players_controller = InventoryPlayersController(
            client_service=self.client_service,
            inventory_players_service=self.inventory_players_service
        )

        # FEATURES - INVENTORY

        self.inventory_service = InventoryService(
            metabomb_api_service=self.metabomb_api_service,
            metabomb_coingecko_service=self.metabomb_coingecko_service,
            metabomb_moralis_service=self.metabomb_moralis_service,
            mapper_service=self.mapper_service
        )

        self.inventory_controller = InventoryController(
            client_service=self.client_service,
            inventory_service=self.inventory_service
        )


if __name__ == '__main__':
    container = AppContainer()


    container.client_service.add_controller(
        container.inventory_players_controller
    )
    container.client_service.add_controller(
        container.inventory_controller
    )
    
    container.client_service.listen()
