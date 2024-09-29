from typing import Optional

from pydantic import BaseModel


class FormField(BaseModel):
    value: Optional[str] = None
    priority: int = 1
    need_verify: bool = False


class Pcc3Form(BaseModel):
    dzien_dokonania: FormField = FormField()
    cel_zlozenia: FormField = FormField()
    podmiot_skladajacy: FormField = FormField()
    rodzaj_podatnika: FormField = FormField()
    nip: FormField = FormField()
    pelna_nazwa_firmy: FormField = FormField()
    skrot_nazwa_firmy: FormField = FormField()
    identyfikator_podatkowy: FormField = FormField()
    identyfikator_podatkowy_wartosc: FormField = FormField()
    pierwsze_imie: FormField = FormField()
    nazwisko: FormField = FormField()
    data_urodzenia: FormField = FormField()
    imie_ojca: FormField = FormField()
    imie_matki: FormField = FormField()
    kraj: FormField = FormField()
    wojwodztwo: FormField = FormField()
    powiat: FormField = FormField()
    gmina: FormField = FormField()
    miejscowosc: FormField = FormField()
    ulica: FormField = FormField()
    numer_domu: FormField = FormField()
    numer_lokalu: FormField = FormField()
    kod_pocztowy: FormField = FormField()
    przedmiot_opodatkowania: FormField = FormField()
    zwiezle_okreslenie_tresci: FormField = FormField()
    rodzaj_czynnosci_cywilno_prawnej: FormField = FormField()
    umowa_sprzedazy_podstawa_2: FormField = FormField()
    umowa_pozyczki_podstawa: FormField = FormField()
