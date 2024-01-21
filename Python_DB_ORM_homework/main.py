import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from models import create_tables, Book, Shop, Publisher, Stock, Sale

# Создание подключения
DSN = "postgresql://postgres:@localhost:5432/books"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Cоздание объектов
pub_1 = Publisher(name="Буквоед")
pub_2 = Publisher(name="Лабиринт")
pub_3 = Publisher(name="Книжный дом")

session.add_all([pub_1, pub_2, pub_3])
session.commit()

book_1 = Book(name="Капитанская дочка", id_publisher = pub_1.id)
book_2 = Book(name="Руслан и Людмила", id_publisher = pub_1.id)
book_3 = Book(name="Капитанская дочка", id_publisher = pub_2.id)
book_4 = Book(name="Евгений Онегин", id_publisher = pub_3.id)

session.add_all([book_1, book_2, book_3, book_4])
session.commit()

session.close()