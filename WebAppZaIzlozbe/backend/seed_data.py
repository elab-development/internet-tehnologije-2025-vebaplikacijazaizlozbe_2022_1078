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

        osoblje_user = db.query(Korisnik).filter(Korisnik.username == "osoblje").first()
        if osoblje_user:
            print("Brisanje zaostalog 'osoblje' korisnika...")
            db.delete(osoblje_user)
            db.commit()

        if db.query(Korisnik).count() > 0 and not osoblje_user:
            print("Podaci već postoje.")
            return
        
        print("Kreiranje test podataka...")
        
        admin = Korisnik(
            username="admin",
            email="admin@galerija.rs",
            lozinka=get_password_hash("admin123"),
            ime="Admin",
            prezime="Korisnik",
            telefon="+381601234567",
            aktivan=True,
            super_korisnik=True,
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
            super_korisnik=False,
            datum_pridruzivanja=datetime.utcnow()
        )
        
        db.add_all([admin, korisnik])
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
        
        lokacija4 = Lokacija(
            naziv="Narodni muzej Niš",
            opis="Multimedijalni muzejski kompleks sa stalnom postavkom i povremenim izložbama",
            g_sirina=43.3209,
            g_duzina=21.8958,
            adresa="Generala Milojka Lešjanina 21",
            grad="Niš"
        )
        
        lokacija5 = Lokacija(
            naziv="Galerija RIMA Kragujevac",
            opis="Savremena galerija sa fokusom na modernu umetnost",
            g_sirina=44.0128,
            g_duzina=20.9114,
            adresa="Trg Radomira Putnika 4",
            grad="Kragujevac"
        )
        
        lokacije = [lokacija1, lokacija2, lokacija3, lokacija4, lokacija5]
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
            ),
            Izlozba(
                naslov="Fotografija Niškog kraja",
                slug="fotografija-niskog-kraja",
                opis="Ekskluzivna izložba fotografija koje prikazuju lepotu i tradiciju Niškog kraja. Od Niške tvrđave do živopisnih pejzaža.",
                kratak_opis="Otkrijte lepotu Niša kroz objektiv lokalnih fotografa",
                datum_pocetka=date(2026, 2, 1),
                datum_zavrsetka=date(2026, 4, 30),
                id_lokacija=lokacije[3].id_lokacija,
                kapacitet=100,
                osmislio="Kustos Milena Jovanović",
                aktivan=True,
                objavljeno=True,
                thumbnail=slike[6].thumbnail,
                id_slika=slike[6].id_slika,
                datum_kreiranja=datetime.utcnow()
            ),
            Izlozba(
                naslov="Industrijsko Nasleđe Šumadije",
                slug="industrijsko-nasledje-sumadije",
                opis="Fotografska dokumentacija industrijskog razvoja Kragujevca i Šumadije. Od Zastave do savremene industrije.",
                kratak_opis="Industrijsko nasleđe regiona kroz fotografiju",
                datum_pocetka=date(2026, 1, 15),
                datum_zavrsetka=date(2026, 3, 15),
                id_lokacija=lokacije[4].id_lokacija,
                kapacitet=80,
                osmislio="Dr Aleksandar Nikolić",
                aktivan=True,
                objavljeno=True,
                thumbnail=slike[0].thumbnail,
                id_slika=slike[0].id_slika,
                datum_kreiranja=datetime.utcnow()
            )
        ]
        
        db.add_all(izlozbe)
        db.commit()
        
        unsplash_ids = [
            "1545989254-660df955dbd6", "1576016773942-0040248e1a48", "1551913902-1322fc692c27",
            "1536924940846-227afb31e215", "1569407334754-1b31f8af84ec", "1580136906911-37d46532454a",
            "1577720580479-7d839d829c73", "1515405295579-ba7a4592924a", "1550684848-fac1c5b4e853",
            "1578301978693-85fa9c0320b9", "1547826039-bfc35e0f1ea8", "1578925518479-0af2e572e969",
            "1577083552431-6e5fd01988ec", "1549490349-8643362247b5", "1577083288073-40892c0860a4",
            "1518998053901-5348d3969104", "1579783902614-a3fb3927b6a5", "1576506542790-51244b486a6b"
        ]
        
        for i, izlo in enumerate(izlozbe):
            img1_id = unsplash_ids[(i * 2) % len(unsplash_ids)]
            img2_id = unsplash_ids[(i * 2 + 1) % len(unsplash_ids)]
            
            dodatne_slike = [
                Slika(
                    slika=f"https://images.unsplash.com/photo-{img1_id}?auto=format&fit=crop&q=80&w=1000",
                    thumbnail=f"https://images.unsplash.com/photo-{img1_id}?auto=format&fit=crop&q=80&w=400",
                    naslov=f"Eksponat {i+1}-A",
                    id_izlozba=izlo.id_izlozba
                ),
                Slika(
                    slika=f"https://images.unsplash.com/photo-{img2_id}?auto=format&fit=crop&q=80&w=1000",
                    thumbnail=f"https://images.unsplash.com/photo-{img2_id}?auto=format&fit=crop&q=80&w=400",
                    naslov=f"Eksponat {i+1}-B",
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
        print("  Admin:    admin / admin123")
        print("  Korisnik: marko / marko123")
        print("="*50)
        
    except Exception as e:
        print(f"Greška: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
