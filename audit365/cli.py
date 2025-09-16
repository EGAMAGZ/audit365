import click
import rich_click

from audit365.commands.message_trace import message_trace


@click.group(cls=rich_click.RichGroup)
def cli() -> None:
    pass

cli.add_command(message_trace)

if __name__ == "__main__":
    cli()
