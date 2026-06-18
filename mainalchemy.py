import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    books = relationship("Book", back_populates="publisher")


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=80), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship("Publisher", back_populates="books")
    stocks = relationship("Stock", back_populates="book")


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    stocks = relationship("Stock", back_populates="shop")


class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship("Book", back_populates="stocks")
    shop = relationship("Shop", back_populates="stocks")
    sales = relationship("Sale", back_populates="stock")


class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship("Stock", back_populates="sales")


engine = sq.create_engine("postgresql://postgres:postgres@localhost:5432/netology_db")

with Session(engine) as session:
    publisher_input = input("Введите имя или id издателя: ")

    query = (
        session.query(
            Book.title,
            Shop.name,
            Sale.price,
            Sale.date_sale
        )
        .join(Stock, Stock.id_book == Book.id)
        .join(Shop, Shop.id == Stock.id_shop)
        .join(Sale, Sale.id_stock == Stock.id)
        .join(Publisher, Publisher.id == Book.id_publisher)
    )

    if publisher_input.isdigit():
        query = query.filter(Publisher.id == int(publisher_input))
    else:
        query = query.filter(Publisher.name == publisher_input)

    for title, shop_name, price, date_sale in query.all():
        print(f"{title} | {shop_name} | {price} | {date_sale}")