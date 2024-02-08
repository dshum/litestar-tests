from click import Group
from litestar import Litestar
from litestar.plugins import CLIPluginProtocol


class DemoCLIPlugin(CLIPluginProtocol):
    def on_cli_init(self, cli: Group) -> None:
        @cli.command()
        def debug(app: Litestar):
            print(app.debug)
