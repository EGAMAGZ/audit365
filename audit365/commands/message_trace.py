import pathlib

import click
import pandas as pd

DEFAULT_ENCODING = "utf-16-le"

DEFAULT_PARSING_METHOD = {
    "encoding": DEFAULT_ENCODING,
    "engine": "python"
}

PERSONAL_DOMAINS = [
    "@gmail.com",
    "@googlemail.com",
    "@outlook.com",
    "@hotmail.com",
    "@live.com",
    "@msn.com",
    "@yahoo.com",
    "@ymail.com",
    "@rocketmail.com",
    "@icloud.com",
    "@me.com",
    "@mac.com",
    "@aol.com",
    "@love.com",
    "@zoho.com",
    "@mail.com",
    "@usa.com",
    "@consultant.com",
    "@engineer.com",
    "@techie.com",
    "@gmx.com",
    "@gmx.net",
    "@gmx.de",
    "@proton.me",
    "@protonmail.com",
    "@tutanota.com",
    "@tutanota.de",
    "@tutamail.com",
    "@tuta.io",
    "@yandex.com",
    "@yandex.ru",
    "@mail.ru",
    "@bk.ru",
    "@inbox.ru",
    "@list.ru",
    "@fastmail.com",
    "@fastmail.fm",
    "@fastmail.net",
    "@mailbolt.com",
    "@pm.me",
]

def is_personal_email(recipient_status: str, domains: list[str]) -> int:
    if pd.isnull(recipient_status):
        return 0

    recipient_status_lower = recipient_status.lower()
    return 1 if any(domain in recipient_status_lower for domain in domains) else 0

@click.group("message-trace")
def message_trace() -> None:
    pass


@message_trace.command("personal-domains")
@click.argument("input_path", type=click.Path(exists=True))
@click.option("--personal-domains", "-p", "personal_domains", multiple=True, help="Additional personal domains (eg. --personal-domains protonmail.com)")
def personal_domains(input_path, personal_domains) -> None:

    all_domains = list(PERSONAL_DOMAINS) + list(personal_domains)
    path_to_audit = pathlib.Path(input_path)

    csv_files: list[pathlib.Path] = []

    if path_to_audit.is_file() and path_to_audit.suffix.lower() == ".csv":
        csv_files = [path_to_audit]
    elif path_to_audit.is_dir():
        csv_files = list(path_to_audit.glob("*.csv"))

    if not csv_files:
        click.echo("No csv files founds in the specified path.")
        return


    for csv_file in csv_files:
        original_csv = pd.read_csv(
            csv_file,
            encoding=DEFAULT_PARSING_METHOD["encoding"],
            engine=DEFAULT_PARSING_METHOD["engine"],
            header=0,
            quotechar='"',
            skipinitialspace=True,
            on_bad_lines="skip",
            skip_blank_lines=True
        )
        original_csv.columns = original_csv.columns.str.strip()

        if "recipient_status" not in original_csv.columns:
            click.echo(f"Error: 'recipient_status' column not found. Available columns: {list(original_csv.columns)}")
            return
        original_csv["sent_to_personal_acc"] = original_csv["recipient_status"].apply(
            lambda recipient_status: is_personal_email(recipient_status, all_domains)
        )

        output_file = csv_file.with_suffix(".xlsx")
        original_csv.to_excel(output_file, index=False)

