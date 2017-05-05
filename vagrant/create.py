from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine 
DBSession = sessionmaker(bind = engine)

session = DBSession()

####### Create #########
myFirstRestaurant = Restaurant(name = 'Pizza Palace')
session.add(myFirstRestaurant)
session.commit()

cheesepizza = MenuItem(name = 'Cheese Pizza', description = 'Made with all natural \
    ingredients and fresh mozzarella', course = 'Entree', price = '$8.99', 
    restaurant = myFirstRestaurant)
session.add(cheesepizza)
session.commit()


######### Read ############
firstResult = session.query(Restaurant).first()
# now you can do firstResult.name


######### Update ############
# 1. find the item you want to update
veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for veggieBurger in veggieBurgers:
    print veggieBurger.id 
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print "\n"

UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 8).one()
# 2. change 
UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit()


for veggieBurger in veggieBurgers:
    if veggieBurger.price != '$2.99':
        veggieBurger.price = '$2.99'
        session.add(veggieBurger)
        session.commit()

############# Delete ###########

spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
session.delete(spinach)
session.commit()



