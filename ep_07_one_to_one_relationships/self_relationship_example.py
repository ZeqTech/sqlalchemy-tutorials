from sqlalchemy import (Column, ForeignKey, Integer, String, create_engine, Table, DateTime)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

db_url = "sqlite:///ep_07_one_to_one_relationships/database_2.db"

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Node(Base):
    __tablename__ = 'nodes'

    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)

    node_id = Column(Integer, ForeignKey('nodes.id'))
    next_node = relationship("Node", remote_side=[id], uselist=False)

    def __repr__(self):
        return f"<Node value={self.value}, next value={self.next_node}>"

Base.metadata.create_all(engine)

node1 = Node(value=1)
node2 = Node(value=2)
node3 = Node(value=3)

node1.next_node = node2
node2.next_node = node3
node3.next_node = node1

session.add_all([node1, node2, node3])
session.commit()

print(node1)
print(node2)
print(node3)
