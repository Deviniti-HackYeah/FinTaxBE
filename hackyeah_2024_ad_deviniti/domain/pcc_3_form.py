from typing import Optional

from pydantic import BaseModel


class FormField(BaseModel):
    value: Optional[str]
    priority: int
    need_verify: bool


class Pcc3Form(BaseModel):
    dzien_dokonania: FormField
    cel_zlozenia: FormField
    podmiot_skladajacy: FormField
    rodzaj_podatnika: FormField
    nip: FormField
    pelna_nazwa_firmy: FormField
    skrot_nazwa_firmy: FormField
    identyfikator_podatkowy: FormField
    identyfikator_podatkowy_wartosc: FormField
    pierwsze_imie: FormField
    nazwisko: FormField
    data_urodzenia: FormField
    imie_ojca: FormField
    imie_matki: FormField
    kraj: FormField
    wojwodztwo: FormField
    powiat: FormField
    gmina: FormField
    miejscowosc: FormField
    ulica: FormField
    numer_domu: FormField
    numer_lokalu: FormField
    kod_pocztowy: FormField
    przedmiot_opodatkowania: FormField
    zwiezle_okreslenie_tresci: FormField
    rodzaj_czynnosci_cywilno_prawnej: FormField
    umowa_sprzedazy_podstawa_2: FormField
    umowa_pozyczki_podstawa: FormField
