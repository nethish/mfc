from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class FundHouse(Base):
    __tablename__ = "fund_house"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"FundHouse(id={self.id!r}, name={self.name!r})"

class FundScheme(Base):
    __tablename__ = "fund_scheme"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fund_house: Mapped[int] = mapped_column(
            ForeignKey("fund_house.id")
        )

    def __repr__(self) -> str:
        return f"FundScheme(id={self.id!r}, name={self.name!r}, fund_house={self.fund_house!r})"

class Company(Base):
    __tablename__ = "company"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    industry_code: Mapped[int] = mapped_column(nullable=True)
    bse_demat_code: Mapped[int] = mapped_column(nullable=True)
    nse_code: Mapped[int] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"Company(id={self.id!r}, name={self.name!r})"

class FundSchemeHolding(Base):
    __tablename__ = "fund_scheme_holding"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fund_id: Mapped[int] = mapped_column(ForeignKey("fund_scheme.id"))
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    holding: Mapped[float] = mapped_column()

if __name__ == "__main__":
    from sqlalchemy import create_engine
    engine = create_engine("sqlite:///./mf.db", echo=True)
    Base.metadata.create_all(engine)

