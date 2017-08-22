#! /usr/bin/env python3
# coding=utf-8
from pathlib import Path

import click
import requests

from random import randint
from sh import imgcat, curl


# Colors supported by click
_ansi_colors = ('black', 'red', 'green', 'yellow', 'blue', 'magenta',
                'cyan', 'white', 'reset')


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        hello()


def _style_quote(item, author):
    styled_item = click.style(item, fg="cyan")
    styled_author = click.style(f'---{author}', fg="red")
    return [styled_item, styled_author]


def _style_advice(item, author):
    styled_item = rainbow_print(item)
    styled_author = click.style(f'---{author}', fg="red")
    return [styled_item, styled_author]


def get_from_api(url, porcess_func, style_func):
    styled_text = "TODO"
    return styled_text


def get_item(filename, style_func):
    """Get random item from the items.txt file"""
    module_path = Path(__file__).parent

    with open(module_path / filename, "r") as f:
        items = [q.split("|") for q in f.readlines() if q.rstrip()]
        random_item = items[randint(0, len(items) - 1)]

        # provide default of empty string when the e.g. quote has no author
        item = random_item[0]
        author = random_item[1] if len(random_item) > 1 else ""

    return "\n".join(style_func(item, author))


def _add(where, new_item):
    module_path = Path(__file__).parent
    where = module_path / where
    with open(where, "a") as f:
        f.writelines(new_item + "\n")


@cli.command(name="advice")
@click.argument('new_item')
def add_advice(new_item):
    """Add ability to add advice from the command line"""
    click.echo("add advice")
    _add("advice.txt", new_item)


@cli.command(name="quote")
@click.argument('new_item')
def add_quote(new_item):
    """Add ability to add quote from the command line"""
    _add("quotes.txt", new_item)


def xkcd():
    """Pull the latest xkcd image and pipe to imgcat"""
    r = requests.get("https://xkcd.com/info.0.json")
    return imgcat(curl(r.json()["img"]))


def rainbow_print(text):
    def get_color(x, text):
        return _ansi_colors[text.index(x) % len(_ansi_colors)]
    styled = [click.style(x, fg=get_color(x, text)) for x in text]
    return "".join(styled)


def hello():
    click.echo("Good day to you 🎩 ")
    click.echo(get_item("quotes.txt", _style_quote))
    click.echo(xkcd())
    click.echo(get_item("advice.txt", _style_advice))
