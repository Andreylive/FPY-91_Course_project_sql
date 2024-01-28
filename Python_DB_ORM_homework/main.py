import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Book, Shop, Publisher, Stock, Sale

# Создание подключения
DSN = "postgresql://postgres:@localhost:5432/books"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Cоздание объектов издательства
pub_1 = Publisher(name="Азбука")
pub_2 = Publisher(name="Речь")
pub_3 = Publisher(name="Слово")

session.add_all([pub_1, pub_2, pub_3])
session.commit()

# Cоздание объектов книги
book_1 = Book(name="Капитанская дочка", id_publisher=pub_1.id)
book_2 = Book(name="Руслан и Людмила", id_publisher=pub_1.id)
book_3 = Book(name="Капитанская дочка", id_publisher=pub_2.id)
book_4 = Book(name="Евгений Онегин", id_publisher=pub_3.id)

session.add_all([book_1, book_2, book_3, book_4])
session.commit()

# Cоздание объектов магазины
shop_1 = Shop(name='Буквоед')
shop_2 = Shop(name='Лабиринт')
shop_3 = Shop(name='Книжный дом')

session.add_all([shop_1, shop_2, shop_3])
session.commit()

# Cоздание объектов скалад
stock_1 = Stock(count=2000, id_book=book_1.id, id_shop=shop_1.id)
stock_2 = Stock(count=5000, id_book=book_1.id, id_shop=shop_2.id)
stock_3 = Stock(count=1000, id_book=book_2.id, id_shop=shop_1.id)
stock_4 = Stock(count=3000, id_book=book_2.id, id_shop=shop_3.id)
stock_5 = Stock(count=8000, id_book=book_3.id, id_shop=shop_1.id)
stock_6 = Stock(count=8000, id_book=book_3.id, id_shop=shop_2.id)
stock_7 = Stock(count=8000, id_book=book_3.id, id_shop=shop_3.id)
stock_8 = Stock(count=2000, id_book=book_4.id, id_shop=shop_1.id)
stock_9 = Stock(count=1000, id_book=book_4.id, id_shop=shop_2.id)
stock_9 = Stock(count=5000, id_book=book_4.id, id_shop=shop_3.id)

session.add_all([stock_1, stock_2, stock_3,
                 stock_4, stock_5, stock_6,
                 stock_7, stock_8, stock_9])
session.commit()

# Cоздание объектов продажи
sale_1 = Sale(price=200, date_sale='2022-11-09', count=50, id_stock=stock_1.id)
sale_2 = Sale(price=150, date_sale='2022-11-10', count=20, id_stock=stock_2.id)
sale_3 = Sale(price=130, date_sale='2022-11-11', count=10, id_stock=stock_3.id)
sale_4 = Sale(price=140, date_sale='2022-11-12', count=5, id_stock=stock_4.id)
sale_5 = Sale(price=140, date_sale='2022-11-13', count=10, id_stock=stock_5.id)
sale_6 = Sale(price=160, date_sale='2022-11-14', count=20, id_stock=stock_6.id)
sale_7 = Sale(price=140, date_sale='2022-11-15', count=10, id_stock=stock_7.id)
sale_8 = Sale(price=140, date_sale='2022-11-16', count=30, id_stock=stock_7.id)
sale_9 = Sale(price=140, date_sale='2022-11-17', count=5, id_stock=stock_8.id)
sale_10 = Sale(price=145, date_sale='2022-11-17', count=5, id_stock=stock_9.id)

session.add_all([sale_1, sale_2, sale_3, sale_4,
                 sale_5, sale_6, sale_7, sale_8,
                 sale_9, sale_10])
session.commit()


def get_sales(shop):
    """Select sales for shop name or id in gien input"""
    data = session.query(Book.name,
                         Shop.name,
                         Sale.price,
                         Sale.date_sale).select_from(Publisher)\
        .join(Book, Book.id_publisher == Publisher.id)\
        .join(Stock, Stock.id_book == Book.id)\
        .join(Shop, Shop.id == Stock.id_shop)\
        .join(Sale, Sale.id_stock == Stock.id)

    if word.isdigit():
        final_data = data.filter(Shop.id == shop).all()
    else:
        final_data = data.filter(Shop.name == shop).all()

    for Book.name, Shop.name, Sale.price, Sale.date_sale in final_data:
        print(f"{Book.name: <20} | {Shop.name: <10} | {Sale.price: 5} | {Sale.date_sale.strftime('%d-%m-%Y')}")


if __name__ == '__main__':
    word = input("Введите имя или id магазина: ").capitalize()
    get_sales(word)
session.close()
