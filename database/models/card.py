from sqlalchemy import Column, String, Integer

from database.models import Base


class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    expansion = Column(String(4), nullable=False)
    scryfall_id = Column(String(60), nullable=True)

    def __repr__(self):
        return f'<Card: {self.name}>'
