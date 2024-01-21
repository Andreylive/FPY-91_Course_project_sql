Капитанская дочка | Буквоед     | 600 | 09-11-2022
Руслан и Людмила  | Буквоед     | 500 | 08-11-2022
Капитанская дочка | Лабиринт    | 580 | 05-11-2022
Евгений Онегин    | Книжный дом | 490 | 02-11-2022
Капитанская дочка | Буквоед     | 600 | 26-10-2022

js = Course(name="JavaScript")
print(js.id)
hw1 = Homework(number=1, description="первое задание", course=js)
hw2 = Homework(number=2, description="второе задание (сложное)", course=js)

book_1 = Book(name="Капитанская дочка", publisher = "Буквоед", )

session.add_all([pub_1, pub_2, pub_3])
session.add_all([book_1])




