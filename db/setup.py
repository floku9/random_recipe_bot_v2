from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base


def get_session(connections_string: str):
    """
    Function to get a session using the provided connection string.

    :param connections_string: A string representing the connection details.
    :return: A session object for database interaction.
    """
    engine = create_engine(connections_string)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
