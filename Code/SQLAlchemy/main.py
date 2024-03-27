# https://www.youtube.com/watch?v=x1fCJ7sUXCM

from datetime import datetime
from typing import Optional
from pathlib import Path

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_collumn
from sqlalchemy.types import DateTime, Integer, String


class Base(DeclarativeBase):
  pass

class Customer(Base):
  __tablename__ = "customer"

  id: Mapped[int] = mapped_collumn(Integer(), primary_key = True, nullable=False)
  first_name: Mapped[str] = mapped_collumn(String(40))
  last_name: Mapped[Optional[str]] = mapped_collumn(String(20))
  company: Mapped[str] = mapped_collumn(String(80))
  address: Mapped[str] = mapped_collumn(String(70))
  city: Mapped[str] = mapped_collumn(String(40))
  state: Mapped[str] = mapped_collumn(String(40))
  country: Mapped[str] = mapped_collumn(String(40))
  postal_code: Mapped[str] = mapped_collumn(String(10))
  phone: Mapped[str] = mapped_collumn(String(24))
  fax: Mapped[str] = mapped_collumn(String(24))
  email: Mapped[str] = mapped_collumn(String(60), nullable=False)
  support_id: Mapped[str] = mapped_collumn(String())

  def __repr__(self) -> str:
    return (
      f"Customer (id={self.id!r},"
      f"first_name={self.first_name!r},"
      f"last_name={self.last_name!r})"
    )

class Invoice(Base):
  __tablename__ = "Invoice"

  id: Mapped[int] = mapped_collumn(Integer(), primary_key=True, nullable=False)
  customer_id: Mapped[int] = mapped_collumn(Integer(), nullable=False)
  date: Mapped[datetime] = mapped_collumn(DateTime(), nullable=False)
  billing_address: Mapped[int] = mapped_collumn(String(70))
  billing_city: Mapped[int] = mapped_collumn(String(40))
  billing_state: Mapped[int] = mapped_collumn(String(40))
  billing_country: Mapped[int] = mapped_collumn(String(40))
  billing_postal_code: Mapped[int] = mapped_collumn(String(10))
  total: Mapped[int] = mapped_collumn(Integer(), nullable=False)

  def __repr__(self) -> str:
    return (
      f"Invoice(id={self.id!r},"
      f"customer_id={self.customer_id!r},"
      f"date={self.date!r})"
    )

def main() -> None:
  number_of_customers = int(
    input("How many customers do you want to query? ")
  )

  db_path = Path("/2023-orm-main/database/sample_database.db").absolute()

  engine = create_engine(rf"sqlite:///{db_path}")

  session = Session(engine)
  stmt = (
    select(
      
    )
  )

  for customer in session.execute(stmt):
    print(customer)


if __name__ == "__main__":
  main()
