from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.korisnik import Korisnik
from app.schemas.korisnik import KorisnikCreate, KorisnikResponse, KorisnikLogin
from app.schemas.token import Token
from app.utils.security import verify_password, get_password_hash, create_access_token
from app.utils.dependencies import get_current_user, get_current_user_required
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["Autentifikacija"])


@router.post("/register", response_model=KorisnikResponse, status_code=status.HTTP_201_CREATED)
async def register(
    korisnik: KorisnikCreate,
    db: Session = Depends(get_db)
):
    existing_username = db.query(Korisnik).filter(
        Korisnik.username == korisnik.username
    ).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Korisničko ime već postoji"
        )
    
    existing_email = db.query(Korisnik).filter(
        Korisnik.email == korisnik.email
    ).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email adresa već postoji"
        )
    
    hashed_password = get_password_hash(korisnik.lozinka)
    db_korisnik = Korisnik(
        username=korisnik.username,
        email=korisnik.email,
        lozinka=hashed_password,
        ime=korisnik.ime,
        prezime=korisnik.prezime,
        telefon=korisnik.telefon,
        profilna_slika=korisnik.profilna_slika,
        aktivan=True,
        osoblje=False,
        super_korisnik=False,
        datum_pridruzivanja=datetime.utcnow()
    )
    
    db.add(db_korisnik)
    db.commit()
    db.refresh(db_korisnik)
    
    return db_korisnik


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(Korisnik).filter(
        Korisnik.username == form_data.username
    ).first()
    
    if not user or not verify_password(form_data.password, user.lozinka):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Pogrešno korisničko ime ili lozinka",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.aktivan:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Korisnički nalog je deaktiviran"
        )
    
    user.poslednja_prijava = datetime.utcnow()
    db.commit()
    
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id_korisnik}
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.post("/logout")
async def logout(
    current_user: Korisnik = Depends(get_current_user_required)
):
    return {"message": "Uspešno ste se odjavili"}


@router.get("/me", response_model=KorisnikResponse)
async def get_me(
    current_user: Korisnik = Depends(get_current_user_required)
):
    return current_user
