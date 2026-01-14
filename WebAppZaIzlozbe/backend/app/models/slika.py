from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Text, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.izlozba import Izlozba
    from app.models.prijava import Prijava


class Slika(Base):
    __tablename__ = "slike"
    
    id_slika: Mapped[int] = mapped_column(primary_key=True, index=True)
    id_izlozba: Mapped[Optional[int]] = mapped_column(
        ForeignKey("izlozbe.id_izlozba"), nullable=True
    )
    slika: Mapped[str] = mapped_column(String(500))
    thumbnail: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    naslov: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    opis: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    fotograf: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    datum_otpremanja: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    istaknuta: Mapped[bool] = mapped_column(Boolean, default=False)
    naslovna: Mapped[bool] = mapped_column(Boolean, default=False)
    redosled: Mapped[int] = mapped_column(Integer, default=0)
    
    izlozba: Mapped[Optional["Izlozba"]] = relationship(
        "Izlozba",
        back_populates="slike",
        foreign_keys=[id_izlozba]
    )
    
    izlozba_naslovna: Mapped[List["Izlozba"]] = relationship(
        "Izlozba",
        back_populates="slika_naslovna",
        foreign_keys="[Izlozba.id_slika]"
    )
    
    prijave: Mapped[List["Prijava"]] = relationship(
        "Prijava",
        back_populates="slika",
        foreign_keys="[Prijava.id_slika]"
    )
    
    def __repr__(self) -> str:
        return f"<Slika(id={self.id_slika}, naslov='{self.naslov}')>"
