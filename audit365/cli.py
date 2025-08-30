import click

from audit365.commands.personal_emails import personal_emails


@click.group()
def cli() -> None:
    pass

cli.add_command(personal_emails)

if __name__ == "__main__":
    pass
