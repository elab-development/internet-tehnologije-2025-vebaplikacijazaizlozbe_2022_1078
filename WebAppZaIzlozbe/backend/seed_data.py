import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, date, timedelta
from app.database import SessionLocal, engine, Base
from app.models import Korisnik, Lokacija, Slika, Izlozba, Prijava
from app.utils.security import get_password_hash

Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    
    try:
        print("Brisanje i re-kreiranje šeme baze...")
        from sqlalchemy import text
        db.execute(text("DROP TABLE IF EXISTS prijave CASCADE"))
        db.execute(text("DROP TABLE IF EXISTS slike CASCADE"))
        db.execute(text("DROP TABLE IF EXISTS izlozbe CASCADE"))
        db.execute(text("DROP TABLE IF EXISTS lokacije CASCADE"))
        db.execute(text("DROP TABLE IF EXISTS korisnici CASCADE"))
        db.commit()
        
        Base.metadata.create_all(bind=engine)
        
        print("Kreiranje test podataka...")
        
        admin = Korisnik(
            username="admin",
            email="admin@galerija.rs",
            lozinka=get_password_hash("admin123"),
            ime="Admin",
            prezime="Korisnik",
            telefon="+381601234567",
            aktivan=True,
            osoblje=True,
            super_korisnik=True,
            datum_pridruzivanja=datetime.utcnow()
        )
        
        osoblje = Korisnik(
            username="osoblje",
            email="osoblje@galerija.rs",
            lozinka=get_password_hash("osoblje123"),
            ime="Petar",
            prezime="Petrović",
            telefon="+381611234567",
            aktivan=True,
            osoblje=True,
            super_korisnik=False,
            datum_pridruzivanja=datetime.utcnow()
        )
        
        korisnik = Korisnik(
            username="marko",
            email="marko@email.com",
            lozinka=get_password_hash("marko123"),
            ime="Marko",
            prezime="Marković",
            telefon="+381621234567",
            aktivan=True,
            osoblje=False,
            super_korisnik=False,
            datum_pridruzivanja=datetime.utcnow()
        )
        
        db.add_all([admin, osoblje, korisnik])
        db.commit()
        print("✓ Korisnici kreirani")
        
        lokacija1 = Lokacija(
            naziv="Galerija SANU",
            opis="Galerija Srpske akademije nauka i umetnosti",
            g_sirina=44.8176,
            g_duzina=20.4569,
            adresa="Knez Mihailova 35",
            grad="Beograd"
        )
        
        lokacija2 = Lokacija(
            naziv="Muzej savremene umetnosti",
            opis="Muzej savremene umetnosti Beograd",
            g_sirina=44.8184,
            g_duzina=20.4111,
            adresa="Ušće 10, blok 15",
            grad="Beograd"
        )
        
        lokacija3 = Lokacija(
            naziv="Galerija Matice srpske",
            opis="Najstarija srpska institucija kulture",
            g_sirina=45.2551,
            g_duzina=19.8451,
            adresa="Trg galerija 1",
            grad="Novi Sad"
        )
        
        lokacije = [lokacija1, lokacija2, lokacija3]
        db.add_all(lokacije)
        db.commit()
        print("✓ Lokacije kreirane")
        
        slike = [
            Slika(
                slika="https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?q=80&w=1000&auto=format&fit=crop",
                thumbnail="https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?q=80&w=400&auto=format&fit=crop",
                naslov="American Gothic",
                opis="Jedno od najpoznatijih dela američke umetnosti",
                fotograf="Grant Wood",
                datum_otpremanja=datetime.utcnow(),
                istaknuta=True,
                naslovna=True,
                redosled=1
            ),
            Slika(
                slika="https://images.unsplash.com/photo-1576016773942-0040248e1a48?q=80&w=1000&auto=format&fit=crop",
                thumbnail="https://images.unsplash.com/photo-1576016773942-0040248e1a48?q=80&w=400&auto=format&fit=crop",
                naslov="A Sunday on La Grande Jatte",
                opis="Remek delo neoimpresionizma",
                fotograf="Georges Seurat",
                datum_otpremanja=datetime.utcnow(),
                istaknuta=True,
                naslovna=False,
                redosled=2
            ),
            Slika(
                slika="https://images.unsplash.com/photo-1543857778-c4a1a3e0b2eb?q=80&w=1000&auto=format&fit=crop",
                thumbnail="https://images.unsplash.com/photo-1543857778-c4a1a3e0b2eb?q=80&w=400&auto=format&fit=crop",
                naslov="Nighthawks",
                opis="Ikonična slika američkog realizma",
                fotograf="Edward Hopper",
                datum_otpremanja=datetime.utcnow(),
                istaknuta=True,
                naslovna=False,
                redosled=3
            ),
            Slika(
                slika="https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?q=80&w=1000&auto=format&fit=crop",
                thumbnail="https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?q=80&w=400&auto=format&fit=crop",
                naslov="The Bedroom",
                opis="Van Goghova soba u Arlu",
                fotograf="Vincent van Gogh",
                datum_otpremanja=datetime.utcnow(),
                istaknuta=False,
                naslovna=False,
                redosled=4
            ),
            Slika(
                slika="https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8?q=80&w=1000&auto=format&fit=crop",
                thumbnail="https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8?q=80&w=400&auto=format&fit=crop",
                naslov="Abstract Harmony",
                opis="Studija boja i oblika",
                fotograf="Wassily Kandinsky",
                datum_otpremanja=datetime.utcnow(),
                istaknuta=False,
                naslovna=False,
                redosled=5
            ),
            Slika(
                slika="https://images.unsplash.com/photo-1549490349-8643362247b5?q=80&w=1000&auto=format&fit=crop",
                thumbnail="https://images.unsplash.com/photo-1549490349-8643362247b5?q=80&w=400&auto=format&fit=crop",
                naslov="The Persistence of Memory",
                opis="Nadrealističko remek delo",
                fotograf="Salvador Dali",
                datum_otpremanja=datetime.utcnow(),
                istaknuta=False,
                naslovna=False,
                redosled=6
            ),
            Slika(
                slika="https://images.unsplash.com/photo-1580136906911-37d46532454a?q=80&w=1000&auto=format&fit=crop",
                thumbnail="https://images.unsplash.com/photo-1580136906911-37d46532454a?q=80&w=400&auto=format&fit=crop",
                naslov="Girl with a Pearl Earring",
                opis="Holandsko zlatno doba",
                fotograf="Johannes Vermeer",
                datum_otpremanja=datetime.utcnow(),
                istaknuta=False,
                naslovna=False,
                redosled=7
            )
        ]
        
        db.add_all(slike)
        db.commit()
        print("✓ Slike kreirane")
        
        today = date.today()
        
        izlozbe = [
            Izlozba(
                naslov="Van Gogh: Boje emocija",
                slug="van-gogh-boje-emocija",
                opis="Ekskluzivna retrospektiva Van Goghovih dela, fokusirana na njegov period u Arlu. Izložba prikazuje emocionalnu dubinu i intenzitet boja karakterističnih za postimpresionizam.",
                kratak_opis="Ekskluzivna retrospektiva Van Goghovih dela",
                datum_pocetka=date(2026, 1, 19),
                datum_zavrsetka=date(2026, 4, 19),
                id_lokacija=lokacije[0].id_lokacija,
                kapacitet=100,
                osmislio="Dr Sofija Radovanović",
                aktivan=True,
                objavljeno=True,
                thumbnail=slike[3].thumbnail,
                id_slika=slike[3].id_slika,
                datum_kreiranja=datetime.utcnow()
            ),
            Izlozba(
                naslov="Impresionizam i neoimpresionizam",
                slug="impresionizam-i-neoimpresionizam",
                opis="Od Monea do Seurata - evolucija svetlosti u slikarstvu. Istražite kako su umetnici manipulisali svetlošću i bojom da stvore nezaboravne scene prirode i urbanog života.",
                kratak_opis="Od Monea do Seurata - evolucija svetlosti u slikarstvu",
                datum_pocetka=date(2025, 12, 27),
                datum_zavrsetka=date(2026, 3, 20),
                id_lokacija=lokacije[1].id_lokacija,
                kapacitet=200,
                osmislio="Prof. Ana Nikolić",
                aktivan=True,
                objavljeno=True,
                thumbnail=slike[1].thumbnail,
                id_slika=slike[1].id_slika,
                datum_kreiranja=datetime.utcnow()
            ),
            Izlozba(
                naslov="Američki realizam XX veka",
                slug="americki-realizam-20-veka",
                opis="Istraživanje američkog realizma kroz ikonična dela XX veka. Od usamljenosti Edwarda Hoppera do ruralnih scena Granta Wooda.",
                kratak_opis="Istraživanje američkog realizma kroz ikonična dela XX veka",
                datum_pocetka=date(2025, 12, 20),
                datum_zavrsetka=date(2026, 2, 18),
                id_lokacija=lokacije[0].id_lokacija,
                kapacitet=150,
                osmislio="Kustos Marko Petrović",
                aktivan=True,
                objavljeno=True,
                thumbnail=slike[2].thumbnail,
                id_slika=slike[2].id_slika,
                datum_kreiranja=datetime.utcnow()
            ),
            Izlozba(
                naslov="Apstraktna Harmonija",
                slug="apstraktna-harmonija",
                opis="Putovanje kroz istoriju apstraktne umetnosti. Kandinsky i njegova revolucija oblika i boja.",
                kratak_opis="Putovanje kroz istoriju apstraktne umetnosti",
                datum_pocetka=date(2026, 2, 15),
                datum_zavrsetka=date(2026, 5, 15),
                id_lokacija=lokacije[1].id_lokacija,
                kapacitet=120,
                osmislio="Dr Ivan Savić",
                aktivan=True,
                objavljeno=True,
                thumbnail=slike[4].thumbnail,
                id_slika=slike[4].id_slika,
                datum_kreiranja=datetime.utcnow()
            ),
            Izlozba(
                naslov="Nadrealizam u fokusu",
                slug="nadrealizam-u-fokusu",
                opis="Istražite snove i podsvest kroz dela Salvadora Dalija i drugih nadrealista. Izložba koja izaziva percepciju.",
                kratak_opis="Snovi i podsvest kroz dela nadrealista",
                datum_pocetka=date(2026, 3, 10),
                datum_zavrsetka=date(2026, 6, 10),
                id_lokacija=lokacije[0].id_lokacija,
                kapacitet=180,
                osmislio="Kustos Jelena M.",
                aktivan=True,
                objavljeno=True,
                thumbnail=slike[5].thumbnail,
                id_slika=slike[5].id_slika,
                datum_kreiranja=datetime.utcnow()
            )
        ]
        
        db.add_all(izlozbe)
        db.commit()
        
        for i, izlo in enumerate(izlozbe):
            dodatne_slike = [
                Slika(
                    slika=f"https://images.unsplash.com/photo-{1500000000000 + i}?auto=format&fit=crop&q=80&w=1000",
                    thumbnail=f"https://images.unsplash.com/photo-{1500000000000 + i}?auto=format&fit=crop&q=80&w=400",
                    naslov=f"Detalj {i+1}",
                    id_izlozba=izlo.id_izlozba
                ),
                Slika(
                    slika=f"https://images.unsplash.com/photo-{1600000000000 + i}?auto=format&fit=crop&q=80&w=1000",
                    thumbnail=f"https://images.unsplash.com/photo-{1600000000000 + i}?auto=format&fit=crop&q=80&w=400",
                    naslov=f"Detalj {i+2}",
                    id_izlozba=izlo.id_izlozba
                )
            ]
            db.add_all(dodatne_slike)
        
        db.commit()
        print("✓ Izložbe kreirane")
        
        print("\n" + "="*50)
        print("Test podaci uspešno kreirani!")
        print("="*50)
        print("\nKorisnički nalozi:")
        print("  Admin:   admin / admin123")
        print("  Osoblje: osoblje / osoblje123")
        print("  Korisnik: marko / marko123")
        print("="*50)
        
    except Exception as e:
        print(f"Greška: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
