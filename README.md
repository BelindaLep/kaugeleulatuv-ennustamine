# Pidevate tervisenäitajate kaugeleulatuv ennustamine

Programmi töötamiseks peavad olema paigaldatud:
- Python: versioon 3.12.2 <br>
ja järgnevad paketid:
    - pandas (versioon 2.2.2)
    - scikit-learn (versioon 1.4.2)
    - numpy (versioon 1.26.4)
    - openpyxl (versioon 3.1.2)

## Kirjeldus

Loodud mudel põhineb lühiajalise vaatlusaknaga alusandmestikul. Vastavalt lähteparameetritele valitakse neile kõige sarnasem patsient ning liigutakse samm-sammult mööda tema ja teiste patsientide andmeid edasi, mille tulemusel moodustub kaugeleulatuv prognoos. <br><br>
Näidisena on mudelit treenitud väga väikeste näidisandmestike abil. See treenitud näidismudel on salvestadud faili ja selle alusel saab teha ka ennustusi. Paremate ja tegelike tulemuste jaoks tuleb mudelile ette anda mahukamad andmestikud.

## Juhised

### Mudeli treenimine

Mudelit saab treenida ja testida failis "mudel.py". Oma mudeli treenimiseks on vaja faili alguses olevas piiritletud osas parameetrite väärtused muuta vastavalt enda soovile ja andmetele. 
<br><br>
Koodile tuleb ette anda <strong>Exceli (.xlsx)</strong> formaadis andmefailid. <strong>Alusandmestikus</strong> peavda olema <strong>veerud: patsient, sugu, vanus ja {ennustatav tunnus}</strong>. <strong>Treening- ja testandmestikus</strong> peavad olema <strong>veerud: sugu,algvanus, alg{ennustatav tunnus}, loppvanus, lopp{ennustatav tunnus}</strong>. 
<br><br>
Näitena on toodud ennustatavaks tunnuseks pikkus, mille algandmestik ning treening- ja testandmestik on toodud vastavates Exceli failides. 
<br> <br>
Soovi korral saab treenitud mudelit salvestada faili, et seda ennustamisel kasutada. Selleks tuleb piiritletud osas ja faili lõpus väljakommenteeritud osa tagasi koodi lisada ja piiritletud osas valida treenitud mudelile sobiv nimi. Näitefailide peal treenitud mudel on salvestatud faili "treenitud_mudel.pkl".


### Mudeli kasutamine

Treenitud mudelit saab kasutada failis "ennustamine.py". Soovitud ennustuse tegemiseks on vaja piiritletud osas parameetrite väärtused muuta vastavalt oma soovile ja andmetele. Enda treenitud mudeli kaustamiseks tuleb ka muuta treenitud mudeli faili nime.