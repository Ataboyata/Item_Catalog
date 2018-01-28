from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

engine = create_engine('sqlite:///item_catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Ironman Category
category1 = Category(name="Ironman")
session.add(category1)
session.commit()

# Ironman 70.3 Category
category2 = Category(name="Ironman 70.3")
session.add(category2)
session.commit()

# Spartan Category
category3 = Category(name="Spartan")
session.add(category3)
session.commit()

# RocknRoll Category
category4 = Category(name="RocknRoll")
session.add(category4)
session.commit()

#Adding Users
user1 = User(name = "Arturo", email = "atorresarpi@hotmail.com", picture = "www.google.com")
session.add(user1)
session.commit()

#Adding a bunch of items
item1 = Item(name="African Championship", description = "Standard Bank Sponsors the IRONMAN African Championship to be hosted on April 15 on Nelson Mandela Bay, South Africa", category = category1, user = user1)
session.add(item1)
session.commit()

item2 = Item(name="Subic Bay Philippines", description = "Century Tuna Sponsors the Subic Bay Philippines Ironamn on June 3 in Subic Bay Philipines", category = category1, user = user1)
session.add(item2)
session.commit()

item3 = Item(name="70.3 Dubai", description = "Dubai will host an Ironman 70.3 on February 2 in Dubai, United Arab Emirates", category = category2, user = user1)
session.add(item3)
session.commit()

item4 = Item(name="70.3 Geelong", description = "Australia will have an Ironman 70.3 on February 18 in Geelong, Victoria", category = category2, user = user1)
session.add(item4)
session.commit()

item5 = Item(name="Arizona Super and Sprint Weekend", description = "February 10 will have a Super and Sprint Spartan Race in Arizona", category = category3, user = user1)
session.add(item5)
session.commit()

item6 = Item(name="South Florida Sprint Weekend", description = "The Sprint may be our shortest distance race, but it is still a favorite amongst both new and returning racers. It is the perfect distance for those looking to start their Spartan journey.", category = category3, user = user1)
session.add(item6)
session.commit()

item7 = Item(name="New Orleans Marathon", description = "For over 20 years, the RocknRoll Marathon Series has made running fun by infusing each course with live bands, cheer teams and more. In 2018, we are bringing our best to Humana Rock n Roll New Orleans Marathon and half marathon with more music, runner support, and community engagement every step of the way. This is a fast, flat course that is complemented by historic houses, iconic landmarks, a post-race party you wont want to miss. With distances for everyone, we invite you, your friends and family to run with us in New Orleans in 2018", category = category4, user = user1)
session.add(item7)
session.commit()

item8 = Item(name="Washington DC", description = "For over 20 years, the RocknRoll Marathon Series has made running fun by infusing each course with live bands, cheer teams and more. In 2018, the United Airlines Rock n Roll Washington DC Marathon and half marathon is celebrating 7 years running, and we are bringing our best with more music, runner support, and community engagement every step of the way. This event is the biggest running festival to hit the capital city with a marathon, half, and 5K, there is something for everyone. We invite you, your friends and family to run with us in 2018!", category = category4, user =user1)
session.add(item8)
session.commit()


print "added items!"
