from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Bank(Base):
    __tablename__ = "banks"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    source = Column(String(255), nullable=True)
    reviews = relationship("Review", back_populates="bank")


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    bank_id = Column(Integer, ForeignKey("banks.id"),
                     nullable=False, index=True)
    review = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)
    date = Column(Date, nullable=True)
    source = Column(String(255), nullable=True)
    bank = relationship("Bank", back_populates="reviews")
