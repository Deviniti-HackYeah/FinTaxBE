class Prompts:

    get_address = """
Dla podanego adresu: 
%%ADDRESS
podaj miasto, kod pocztowy, ulicę numer domu, Wojewodztwo, Powiat, Gminę i kod właściwego urzędu skarbowego, odpwiedz w formacie json"""

    # jakby nie dał kodu urzedu, to zapytać poniższym pytaniem, wklejając na końcu dane adresowe
    get_us_uscode = """
Podaj mi kod urzędu skarbowego dla poniższego adresu:
Miasto: %%MIASTO
Kod pocztowy: %%KOD
Ulica i numer domu: %%ULICA_NR_DOMU
Województwo: %%WOJEWODZTWO
Powiat: %%POWIAT
Gmina: %%GMINA.
Odpowiedz wyłącznie kodem urzędu.
"""
