import sys

import click
import sqlalchemy_searchable
import yaml

from cal import db, User
from scrapers import scrapers

@click.group()
def cli():
    pass


@cli.command()
@click.option("--scraper", default="all",
              type=click.Choice(["all"] + list(scrapers.keys())))
@click.pass_context
def create(ctx, scraper):
    """Create database and run scrapers"""
    db.configure_mappers()  # needed for SQLAlchemy-Searchable
    db.create_all()

    update.invoke(ctx)


@cli.command()
@click.option("--scraper", default="all",
              type=click.Choice(["all"] + list(scrapers.keys())))
def update(scraper):
    """Run scrapers to fill database"""
    # Populate the user database
    with open('config/groups.yml') as fin:
        users = yaml.load(fin)
    for username, ids in users.items():
        if User.query.filter_by(name=username).first() is None:
            new_user = User(name=username)
            new_user.fb_id = ids.get('facebook', None)
            db.session.add(new_user)
    db.session.commit()

    if scraper == "all":
        for s in scrapers.values():
            s()
    else:
        scrapers[scraper]()


@cli.command()
def delete():
    """Delete the database"""
    db.drop_all()

    # drop sqlalchemy-searchable stuff
    with db.engine.connect() as conn:
        for column in sqlalchemy_searchable.search_manager.processed_columns:
            query = str(sqlalchemy_searchable.DropSearchFunctionSQL(column))
            conn.execute(query)


@cli.command()
@click.pass_context
def connect(ctx):
    """Open a pgcli REPL to the database"""
    try:
        from pgcli.main import cli as pgcli
    except ImportError:
        sys.exit("You need to install `pgcli` for this command to work. Try:"
                 "\n\tpip install pgcli")

    pgcli.main([str(db.engine.url)])


if __name__ == "__main__":
    cli()
