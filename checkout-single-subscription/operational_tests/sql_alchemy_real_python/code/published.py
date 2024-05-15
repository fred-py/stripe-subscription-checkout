# published.py
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

author_publisher = Table(
    "author_publisher",
    Base.metadata,
    Column("author_id", Integer, ForeignKey("author.author_id")),
    Column("publisher_id", Integer, ForeignKey("publisher.publisher_id")),
)

book_publisher = Table(
    "book_publisher",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("book.book_id")),
    Column("publisher_id", Integer, ForeignKey("publisher.publisher_id")),
)

class Author(Base):
    __tablename__ = "author"

    author_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    books = relationship("Book", backref=backref("author"),
        cascade="all, delete-orphan")

    publishers = relationship("Publisher", secondary=author_publisher,
        back_populates="authors")

    def __repr__(self):
        return (
            f"Author(author_id={self.author_id!r}, "
            f"first_name={self.first_name!r}, last_name={self.last_name!r})"
        )
    
class Book(Base):
    __tablename__ = "book"

    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey("author.author_id"), nullable=False)

    publishers = relationship("Publisher", secondary=book_publisher,
        back_populates="books")

    def __repr__(self):
        return (
            f"Book(book_id={self.book_id!r}, "
            f"title={self.title!r}, author_id={self.author_id!r})"
        )

class Publisher(Base):
    __tablename__ = 'publisher'

    publisher_id = Column(Integer, primary_key=True)
    name = Column(String)

    authors = relationship("Author", secondary=author_publisher,
        back_populates="publishers")
    books = relationship("Book", secondary=book_publisher,
        back_populates="publishers")

    def __repr__(self):
        return (
            f"Publisher(publisher_id={self.publisher_id!r}, "
            f"name={self.name!r})"
        )



engine = create_engine('sqlite:///sqlalchemy_test22.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

# Create a Session class bound to the engine
Session = sessionmaker(bind=engine)

# Create an instance of the Session class
session = Session()

"""Query examples"""
# Create statemet
#stmt = select(Subscription)
# Scalars method is used instread of execute to 
# query all the customers in the database
#for customers in session.scalars(stmt):
#    print(customers)

"""stmt = select(Customer).join(Address.postcode).where(Address.postcode == '6085')
for customer in session.scalars(stmt):
    print(customer)"""

"""
stmt = select(Customer).where(Customer.first_name == 'Fred')
fred = session.scalars(stmt).one() # .one() returns one result
"""
results = session.query(Author).all()
print(results)