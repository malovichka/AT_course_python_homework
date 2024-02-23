import sqlalchemy as sa


engine = sa.create_engine("sqlite+pysqlite:///films_db.sqlite")
metadata = sa.MetaData()

# describing table with metadata object
films_table = sa.Table(
    "films",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("title", sa.String),
    sa.Column("director", sa.String),
    sa.Column("release_year", sa.Integer),
    # adding constraint for unique title+year combination to avoid duplicates
    sa.UniqueConstraint("title", "release_year", name="unique_name_in_release_year"),
)


films_to_insert = [
    {"title": "Snatch", "director": "Guy Ritchie", "release_year": 2000},
    {
        "title": "Inglourious Basterds",
        "director": "Quentin Tarantino",
        "release_year": 2009,
    },
    {"title": "Twilight", "director": "Robert Pattinson", "release_year": 2008},
]

# binding parameters for update
update_director = (
    sa.update(films_table)
    .where(films_table.c.director == sa.bindparam("old_director"))
    .values(director=sa.bindparam("new_director"))
)


def create_table():
    """This function creates table"""
    metadata.create_all(engine)


def add_data():
    """This function adds data(rows) to films_table"""
    with engine.connect() as connection:
        result = connection.execute(
            sa.insert(films_table),
            films_to_insert,
        )
        connection.commit()


def update_data():
    """This function updates director name"""
    with engine.connect() as connection:
        result = connection.execute(
            update_director,
            [
                {
                    "old_director": "Robert Pattinson",
                    "new_director": "Catherine Hardwicke",
                }
            ],
        )
        connection.commit()


def print_data():
    """This function prints the contents of the films_table"""
    with engine.connect() as connection:
        for row in connection.execute(sa.select(films_table)):
            print(row)


def delete_data():
    """This function deletes data from the films_table"""
    with engine.connect() as connection:
        result = connection.execute(sa.delete(films_table))
        connection.commit()


def delete_table():
    """This function deletes table"""
    films_table.drop(engine)


if __name__ == "__main__":
    create_table()
    add_data()
    update_data()
    print_data()
    delete_data()
    # delete_table()
