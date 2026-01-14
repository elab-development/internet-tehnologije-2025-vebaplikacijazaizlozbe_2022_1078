from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.izlozba import Izlozba


class Lokacija(Base):
    __tablename__ = "lokacije"
    
    id_lokacija: Mapped[int] = mapped_column(primary_key=True, index=True)
    naziv: Mapped[str] = mapped_column(String(200))
    opis: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    g_sirina: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    g_duzina: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    adresa: Mapped[str] = mapped_column(String(300))
    grad: Mapped[str] = mapped_column(String(100), index=True)
    
    izlozbe: Mapped[List["Izlozba"]] = relationship(
        "Izlozba",
        back_populates="lokacija",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Lokacija(id={self.id_lokacija}, naziv='{self.naziv}')>"
