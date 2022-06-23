import logging
import os

from naff import Client, listen, logger_name


class CustomClient(Client):
    """Subclass of naff.Client with our own logger and on_startup event"""

    # you can use that logger in all your extensions
    logger = logging.getLogger(logger_name)

    @listen()
    async def on_startup(self):
        """Gets triggered on startup"""

        self.logger.info(f"{os.getenv('PROJECT_NAME')} - Startup Finished!")
        self.logger.info(
            "Note: Discord needs up to an hour to load your global commands / context menus. They may not appear immediately\n"
        )
