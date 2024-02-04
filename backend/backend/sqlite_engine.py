from sqlalchemy import create_engine

ENGINE = create_engine("sqlite:///../database/mf.db", echo=True)

