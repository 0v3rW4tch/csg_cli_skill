# -*- coding: utf-8 -*-
import datetime
import json
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.json import JSON
from rich.table import Table

sys.path.insert(0, str(Path(__file__).parent))

from csg_client import CSGClient, CSGElectricityAccount

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]}, add_completion=False)
console = Console()
SESSION_FILE = Path("session.json")


def get_client() -> CSGClient:
    if not SESSION_FILE.exists():
        console.print("[red]Not logged in. Run: login-sms PHONE[/red]")
        raise typer.Exit(1)
    with open(SESSION_FILE) as f:
        return CSGClient.load(json.load(f))


def get_account(client: CSGClient, account_idx: int = 0) -> CSGElectricityAccount:
    client.initialize()
    accounts = client.get_all_electricity_accounts()
    if not accounts:
        console.print("[red]No accounts found[/red]")
        raise typer.Exit(1)
    if account_idx >= len(accounts):
        console.print(f"[red]Account {account_idx} not found[/red]")
        raise typer.Exit(1)
    return accounts[account_idx]


@app.command()
def send_sms(phone: str):
    client = CSGClient()
    client.api_send_login_sms(phone)
    console.print("[green]SMS sent to {}. Check your phone for the 6-digit code.[/green]".format(phone))
    console.print("[yellow]Next: Run 'login-sms PHONE CODE' to complete login.[/yellow]")


@app.command()
def login_sms(phone: str, code: str):
    client = CSGClient()
    auth_token = client.api_login_with_sms_code(phone, code)
    client.set_authentication_params(auth_token)
    with open(SESSION_FILE, "w") as f:
        json.dump(client.dump(), f)
    console.print("[green]Logged in successfully![/green]")


@app.command()
def logout():
    """Logout and clear session."""
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()
        console.print("[green]Logged out[/green]")
    else:
        console.print("[yellow]Not logged in[/yellow]")


@app.command()
def status():
    """Check login status."""
    try:
        client = get_client()
        client.initialize()
        if client.verify_login():
            console.print("[green]Logged in[/green]")
        else:
            console.print("[red]Session expired[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@app.command()
def accounts():
    """List all electricity accounts."""
    client = get_client()
    client.initialize()
    accounts = client.get_all_electricity_accounts()

    table = Table(title=f"Accounts ({len(accounts)})")
    table.add_column("Idx", justify="right")
    table.add_column("Account")
    table.add_column("User")
    table.add_column("Address")

    for i, acc in enumerate(accounts):
        table.add_row(
            str(i),
            acc.account_number or "N/A",
            acc.user_name or "N/A",
            acc.address or "N/A",
        )

    console.print(table)


@app.command()
def balance(account: int = 0):
    """Get account balance and arrears."""
    client = get_client()
    acc = get_account(client, account)
    bal, arr = client.get_balance_and_arrears(acc)
    console.print(
        JSON.from_data(
            {"account": acc.account_number, "balance_cny": bal, "arrears_cny": arr}
        )
    )


@app.command()
def yesterday(account: int = 0):
    """Get yesterday's electricity usage (kWh)."""
    client = get_client()
    acc = get_account(client, account)
    kwh = client.get_yesterday_kwh(acc)
    date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    console.print(
        JSON.from_data({"account": acc.account_number, "date": date, "power_kwh": kwh})
    )


@app.command()
def calendar(year: int = None, month: int = None, account: int = 0):
    """Get daily electricity and temperature data for a month."""
    now = datetime.datetime.now()
    year = year or now.year
    month = month or now.month

    client = get_client()
    acc = get_account(client, account)
    data = client.api_query_electricity_calender(
        year,
        month,
        acc.area_code,
        acc.ele_customer_id,
        acc.metering_point_id,
        acc.metering_point_number,
    )
    console.print(JSON.from_data(data))


@app.command()
def elec_bill(year: int, month: int, account: int = 0):
    """Get electricity bill (charge and power) for a month."""
    client = get_client()
    acc = get_account(client, account)
    charge, power = client.get_elec_bill_list(acc, (year, month))
    console.print(
        JSON.from_data(
            {
                "account": acc.account_number,
                "year_month": f"{year}{month:02d}",
                "total_charge_cny": charge,
                "total_power_kwh": power,
            }
        )
    )


@app.command()
def year_stats(year: int, account: int = 0):
    """Get yearly statistics (total charge, total power, monthly breakdown)."""
    client = get_client()
    acc = get_account(client, account)
    total_charge, total_power, by_month = client.get_year_month_stats(acc, year)
    console.print(
        JSON.from_data(
            {
                "account": acc.account_number,
                "year": year,
                "total_charge_cny": total_charge,
                "total_power_kwh": total_power,
                "monthly": by_month,
            }
        )
    )


if __name__ == "__main__":
    app()
