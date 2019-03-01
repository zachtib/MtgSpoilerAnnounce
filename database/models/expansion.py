from sqlalchemy import Column, String, Integer, Date, Boolean

from database.models import Base


class Expansion(Base):
    __tablename__ = 'expansions'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    code = Column(String(10), nullable=False)
    kind = Column(String(20), nullable=False)
    watched = Column(Boolean, default=False)
    release_date = Column(Date)
    scryfall_id = Column(String(60), nullable=True)

    def __repr__(self):
        return f'<Expansion: {self.name}>'
