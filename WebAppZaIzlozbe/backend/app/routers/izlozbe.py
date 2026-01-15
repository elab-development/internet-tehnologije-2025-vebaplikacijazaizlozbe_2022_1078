from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.database import get_db
from app.models.izlozba import Izlozba
from app.models.lokacija import Lokacija
from app.models.korisnik import Korisnik
from app.schemas.izlozba import (
    IzlozbaCreate, IzlozbaUpdate, IzlozbaResponse, IzlozbaListResponse
)
from app.utils.dependencies import get_current_staff, get_current_admin

router = APIRouter(prefix="/api/izlozbe", tags=["Izložbe"])


@router.get("/", response_model=IzlozbaListResponse)
async def list_izlozbe(
    page: int = Query(1, ge=1),
    per_page: int = Query(12, ge=1, le=50),
    search: Optional[str] = None,
    grad: Optional[str] = None,
    aktivan: Optional[bool] = None,
    objavljeno: Optional[bool] = None,
    od_datuma: Optional[date] = None,
    do_datuma: Optional[date] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Izlozba).options(
        joinedload(Izlozba.lokacija),
        joinedload(Izlozba.slika_naslovna),
        joinedload(Izlozba.slike)
    )
    
    if search:
        query = query.filter(
            or_(
                Izlozba.naslov.ilike(f"%{search}%"),
                Izlozba.opis.ilike(f"%{search}%"),
                Izlozba.kratak_opis.ilike(f"%{search}%")
            )
        )
    
    if grad:
        query = query.join(Lokacija).filter(Lokacija.grad.ilike(f"%{grad}%"))
    
    if aktivan is not None:
        query = query.filter(Izlozba.aktivan == aktivan)
    
    if objavljeno is not None:
        query = query.filter(Izlozba.objavljeno == objavljeno)
    
    if od_datuma:
        query = query.filter(Izlozba.datum_pocetka >= od_datuma)
    
    if do_datuma:
        query = query.filter(Izlozba.datum_zavrsetka <= do_datuma)
    
    total = query.count()
    
    skip = (page - 1) * per_page
    izlozbe = query.order_by(Izlozba.datum_pocetka.desc()).offset(skip).limit(per_page).all()
    
    items = []
    for izlozba in izlozbe:
        izlozba_dict = IzlozbaResponse.model_validate(izlozba).model_dump()
        izlozba_dict["preostali_kapacitet"] = izlozba.preostali_kapacitet
        items.append(IzlozbaResponse(**izlozba_dict))
    
    return IzlozbaListResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        pages=(total + per_page - 1) // per_page
    )


@router.get("/slug/{slug}", response_model=IzlozbaResponse)
async def get_izlozba_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    izlozba = db.query(Izlozba).options(
        joinedload(Izlozba.lokacija),
        joinedload(Izlozba.slika_naslovna),
        joinedload(Izlozba.slike)
    ).filter(Izlozba.slug == slug).first()
    
    if not izlozba:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Izložba nije pronađena"
        )
    
    response = IzlozbaResponse.model_validate(izlozba)
    response_dict = response.model_dump()
    response_dict["preostali_kapacitet"] = izlozba.preostali_kapacitet
    
    return IzlozbaResponse(**response_dict)
    
@router.get("/{izlozba_id}", response_model=IzlozbaResponse)
async def get_izlozba(
    izlozba_id: int,
    db: Session = Depends(get_db)
):
    izlozba = db.query(Izlozba).options(
        joinedload(Izlozba.lokacija),
        joinedload(Izlozba.slika_naslovna),
        joinedload(Izlozba.slike)
    ).filter(Izlozba.id_izlozba == izlozba_id).first()
    
    if not izlozba:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Izložba nije pronađena"
        )
    
    response = IzlozbaResponse.model_validate(izlozba)
    response_dict = response.model_dump()
    response_dict["preostali_kapacitet"] = izlozba.preostali_kapacitet
    
    return IzlozbaResponse(**response_dict)


@router.post("/", response_model=IzlozbaResponse, status_code=status.HTTP_201_CREATED)
async def create_izlozba(
    izlozba: IzlozbaCreate,
    db: Session = Depends(get_db),
    current_user: Korisnik = Depends(get_current_staff)
):
    lokacija = db.query(Lokacija).filter(
        Lokacija.id_lokacija == izlozba.id_lokacija
    ).first()
    
    if not lokacija:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lokacija ne postoji"
        )
    
    existing_slug = db.query(Izlozba).filter(Izlozba.slug == izlozba.slug).first()
    if existing_slug:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Izložba sa ovim slugom već postoji"
        )
    
    izlozba_data = izlozba.model_dump()
    slike_urls = izlozba_data.pop("slike_urls", [])
    
    db_izlozba = Izlozba(**izlozba_data)
    db.add(db_izlozba)
    db.commit()
    db.refresh(db_izlozba)
    
    from app.models.slika import Slika
    for url in slike_urls:
        if url.strip():
            nova_slika = Slika(
                slika=url,
                thumbnail=url, 
                id_izlozba=db_izlozba.id_izlozba,
                naslov=db_izlozba.naslov
            )
            db.add(nova_slika)
    
    if slike_urls:
        db.commit()
        db.refresh(db_izlozba)
    
    return db_izlozba


@router.put("/{izlozba_id}", response_model=IzlozbaResponse)
async def update_izlozba(
    izlozba_id: int,
    izlozba_update: IzlozbaUpdate,
    db: Session = Depends(get_db),
    current_user: Korisnik = Depends(get_current_staff)
):
    izlozba = db.query(Izlozba).filter(
        Izlozba.id_izlozba == izlozba_id
    ).first()
    
    if not izlozba:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Izložba nije pronađena"
        )
    
    update_data = izlozba_update.model_dump(exclude_unset=True)
    slike_urls = update_data.pop("slike_urls", None)
    
    if "slug" in update_data and update_data["slug"] != izlozba.slug:
        existing_slug = db.query(Izlozba).filter(Izlozba.slug == update_data["slug"]).first()
        if existing_slug:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Izložba sa ovim slugom već postoji"
            )

    if "kapacitet" in update_data:
        ukupno_prijava = sum(p.broj_karata for p in izlozba.prijave)
        if update_data["kapacitet"] < ukupno_prijava:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Kapacitet ne može biti manji od broja prijava ({ukupno_prijava})"
            )
    
    for field, value in update_data.items():
        setattr(izlozba, field, value)
    
    if slike_urls is not None:
        from app.models.slika import Slika
        db.query(Slika).filter(Slika.id_izlozba == izlozba_id).delete()
        
        for url in slike_urls:
            if url.strip():
                nova_slika = Slika(
                    slika=url,
                    thumbnail=url,
                    id_izlozba=izlozba_id,
                    naslov=izlozba.naslov
                )
                db.add(nova_slika)

    db.commit()
    db.refresh(izlozba)
    
    return izlozba


@router.delete("/{izlozba_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_izlozba(
    izlozba_id: int,
    db: Session = Depends(get_db),
    current_user: Korisnik = Depends(get_current_admin)
):
    izlozba = db.query(Izlozba).filter(
        Izlozba.id_izlozba == izlozba_id
    ).first()
    
    if not izlozba:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Izložba nije pronađena"
        )
    
    db.delete(izlozba)
    db.commit()
    
    return None
