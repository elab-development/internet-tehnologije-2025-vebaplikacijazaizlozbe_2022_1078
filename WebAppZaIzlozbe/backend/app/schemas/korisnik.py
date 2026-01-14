from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class KorisnikBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    ime: str = Field(..., min_length=1, max_length=50)
    prezime: str = Field(..., min_length=1, max_length=50)
    telefon: Optional[str] = Field(None, max_length=20)
    grad: Optional[str] = Field(None, max_length=100)
    adresa: Optional[str] = Field(None, max_length=200)
    profilna_slika: Optional[str] = None


class KorisnikCreate(KorisnikBase):
    lozinka: str = Field(..., min_length=6, max_length=100)


class KorisnikUpdate(BaseModel):
    ime: Optional[str] = Field(None, min_length=1, max_length=50)
    prezime: Optional[str] = Field(None, min_length=1, max_length=50)
    telefon: Optional[str] = Field(None, max_length=20)
    grad: Optional[str] = Field(None, max_length=100)
    adresa: Optional[str] = Field(None, max_length=200)
    profilna_slika: Optional[str] = None
    aktivan: Optional[bool] = None
    osoblje: Optional[bool] = None
    super_korisnik: Optional[bool] = None


class KorisnikResponse(KorisnikBase):
    id_korisnik: int
    aktivan: bool
    osoblje: bool
    super_korisnik: bool
    datum_pridruzivanja: datetime
    poslednja_prijava: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class KorisnikLogin(BaseModel):
    username: str
    lozinka: str
