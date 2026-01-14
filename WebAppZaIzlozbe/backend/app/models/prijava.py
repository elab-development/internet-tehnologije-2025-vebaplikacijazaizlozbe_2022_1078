from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.korisnik import Korisnik
    from app.models.izlozba import Izlozba
    from app.models.slika import Slika


class Prijava(Base):
    __tablename__ = "prijave"
    
    id_prijava: Mapped[int] = mapped_column(primary_key=True, index=True)
    id_korisnik: Mapped[int] = mapped_column(
        ForeignKey("korisnici.id_korisnik")
    )
    id_izlozba: Mapped[int] = mapped_column(
        ForeignKey("izlozbe.id_izlozba")
    )
    id_slika: Mapped[Optional[int]] = mapped_column(
        ForeignKey("slike.id_slika"), nullable=True
    )
    broj_karata: Mapped[int] = mapped_column(Integer, default=1)
    qr_kod: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    validirano: Mapped[bool] = mapped_column(Boolean, default=False)
    datum_registracije: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    slika_qr: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    verifikovan_email: Mapped[bool] = mapped_column(Boolean, default=False)
    email_poslat: Mapped[bool] = mapped_column(Boolean, default=False)
    datum_slanja_emaila: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )
    
    korisnik: Mapped["Korisnik"] = relationship(
        "Korisnik",
        back_populates="prijave"
    )
    
    izlozba: Mapped["Izlozba"] = relationship(
        "Izlozba",
        back_populates="prijave"
    )
    
    slika: Mapped[Optional["Slika"]] = relationship(
        "Slika",
        back_populates="prijave",
        foreign_keys=[id_slika]
    )
    
    def __repr__(self) -> str:
        return f"<Prijava(id={self.id_prijava}, korisnik={self.id_korisnik}, izlozba={self.id_izlozba})>"
