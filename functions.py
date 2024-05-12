import numpy as np
import sys
from sklearn.metrics import mean_squared_error
import random


class Patsient:
    def __init__(self, id, sugu, punktid, ennustatud):
        self.id = id
        self.sugu = sugu
        self.punktid = punktid
        self.ennustatud = ennustatud


def looPatsiendid(andmed, ennustatava_naitaja_nimetus, min_mootmisi_per_patsient):
    patsiendid_list = []
    for patsient_id, andmed in andmed:
        sugu = andmed["sugu"].iloc[0]
        punktid = list(zip(andmed["vanus"], andmed[ennustatava_naitaja_nimetus]))

        if len(punktid) >= min_mootmisi_per_patsient:
            patsient_objekt = Patsient(
                id=patsient_id, sugu=sugu, punktid=punktid, ennustatud=False
            )
            patsiendid_list.append(patsient_objekt)

    return patsiendid_list


def skoor(
    vanus,
    ennustatav_naitaja,
    sugu,
    patsient,
    punkt,
    vanuse_kaal,
    naitaja_kaal,
    kauguse_kaal,
    soo_kaal,
    minid_ja_maxid,
):
    min_poord_kaugus = 0
    max_poord_kaugus = 365.25
    min_vanus, max_vanus, min_naitaja, max_naitaja, min_sugu, max_sugu = minid_ja_maxid

    norm_vanus = (vanus - min_vanus) / (max_vanus - min_vanus)
    norm_vanus_punkt = (punkt[0] - min_vanus) / (max_vanus - min_vanus)
    norm_naitaja = (ennustatav_naitaja - min_naitaja) / (max_naitaja - min_naitaja)
    norm_naitaja_punkt = (punkt[1] - min_naitaja) / (max_naitaja - min_naitaja)

    norm_poord_kaugus = (
        (1 / (patsient.punktid[-1][0] + (1 / 365.25))) - min_poord_kaugus
    ) / (max_poord_kaugus - min_poord_kaugus)

    norm_sugu = (sugu - min_sugu) / (max_sugu - min_sugu)
    norm_sugu_patsient = (patsient.sugu - min_sugu) / (max_sugu - min_sugu)

    deltaT = abs(norm_vanus - norm_vanus_punkt)
    deltaL = abs(norm_naitaja - norm_naitaja_punkt)
    deltaF = abs(norm_vanus - norm_poord_kaugus)
    deltaG = abs(norm_sugu - norm_sugu_patsient)

    skoor_tulemus = (
        (vanuse_kaal * deltaT)
        + (naitaja_kaal * deltaL)
        + (kauguse_kaal * deltaF)
        + (soo_kaal * deltaG)
    )

    return skoor_tulemus


def patsiendi_skoor(
    vanus,
    ennustatav_naitaja,
    sugu,
    patsient,
    vanuse_kaal,
    naitaja_kaal,
    kauguse_kaal,
    soo_kaal,
    minid_ja_maxid,
):
    parim_skoor = sys.maxsize
    parim_punkt = None
    for punkt in patsient.punktid:
        if punkt == patsient.punktid[-1]:
            continue
        saadud_skoor = skoor(
            vanus,
            ennustatav_naitaja,
            sugu,
            patsient,
            punkt,
            vanuse_kaal,
            naitaja_kaal,
            kauguse_kaal,
            soo_kaal,
            minid_ja_maxid,
        )
        if saadud_skoor < parim_skoor:
            parim_skoor = saadud_skoor
            parim_punkt = punkt

    return parim_punkt, parim_skoor


def sarnane_skooriga(
    vanus,
    ennustatav_naitaja,
    soovitud_vanus,
    sugu,
    vanuse_kaal,
    naitaja_kaal,
    kauguse_kaal,
    soo_kaal,
    mitmes,
    on_esimene_skoorimine,
    patsiendid,
    minid_ja_maxid,
):
    parimad = [None] * mitmes
    parim = sys.maxsize

    for patsient in patsiendid:
        if patsient.ennustatud or patsient.punktid[-1][0] <= vanus:
            continue
        punkt, skoor = patsiendi_skoor(
            vanus,
            ennustatav_naitaja,
            sugu,
            patsient,
            vanuse_kaal,
            naitaja_kaal,
            kauguse_kaal,
            soo_kaal,
            minid_ja_maxid,
        )
        if skoor < parim:
            parim = skoor
            parimad = [patsient] + parimad[:-1]

    saadud_parimate_arv = (
        next(
            len(parimad) - i
            for i, j in enumerate(reversed(parimad), 1)
            if j is not None
        )
        + 1
    )
    if on_esimene_skoorimine:
        if saadud_parimate_arv >= mitmes:
            saadud_patsient = parimad[mitmes - 1]
        else:
            saadud_patsient = parimad[saadud_parimate_arv - 1]
    else:
        saadud_patsient = parimad[0]

    vastus_vanus = saadud_patsient.punktid[-1][0]
    vastus_naitaja = saadud_patsient.punktid[-1][1]

    if vastus_vanus > soovitud_vanus:
        vanused = []
        naitajad = []
        for punkt in saadud_patsient.punktid:
            vanused.append(punkt[0])
            naitajad.append(punkt[1])

        vastus_naitaja = np.interp(soovitud_vanus, vanused, naitajad)
        vastus_vanus = soovitud_vanus

    saadud_patsient.ennustatud = True

    return vastus_vanus, vastus_naitaja


def ennustus(
    vanus,
    naitaja,
    soovitud_vanus,
    sugu,
    vanuse_kaal,
    naitaja_kaal,
    kauguse_kaal,
    soo_kaal,
    mitu_lahimat,
    patsiendid,
    minid_ja_maxid,
):

    naitajate_summa = 0
    for mitmes in range(mitu_lahimat):
        algvanus = vanus
        algnaitaja = naitaja
        esimene_skoorimine = True
        while algvanus != soovitud_vanus:
            sarnane_inimene = sarnane_skooriga(
                algvanus,
                algnaitaja,
                soovitud_vanus,
                sugu,
                vanuse_kaal,
                naitaja_kaal,
                kauguse_kaal,
                soo_kaal,
                (mitmes + 1),
                esimene_skoorimine,
                patsiendid,
                minid_ja_maxid,
            )

            if sarnane_inimene == None:
                return "Sobivaid inimesi ei ole"

            esimene_skoorimine = False
            algvanus, algnaitaja = sarnane_inimene[0], sarnane_inimene[1]

        naitajate_summa += algnaitaja
        for p in patsiendid:
            p.ennustatud = False

        loppnaitaja = naitajate_summa / mitu_lahimat

    return vanus, loppnaitaja


def arvuta_rmse(oiged_naitajad, ennustatud_naitajad):
    mse = mean_squared_error(oiged_naitajad, ennustatud_naitajad)
    rmse = np.sqrt(mse)
    return rmse


def hinda_mudelit(
    andmed,
    vanuse_kaal,
    naitaja_kaal,
    kauguse_kaal,
    soo_kaal,
    ennustatava_naitaja_nimetus,
    mitu_lahimat,
    patsiendid,
    minid_ja_maxid,
):

    ennustatud_naitajad = []
    oiged_naitajad = []

    for i, inimene in andmed.iterrows():
        sugu = inimene["sugu"]
        antud_vanus = inimene["algvanus"]
        antud_naitaja_vaartus = inimene[f"alg{ennustatava_naitaja_nimetus}"]
        soovitud_vanus = inimene["loppvanus"]
        oige_naitaja_vaartus = inimene[f"lopp{ennustatava_naitaja_nimetus}"]

        ennustatud_vanus, ennustatud_naitaja = ennustus(
            antud_vanus,
            antud_naitaja_vaartus,
            soovitud_vanus,
            sugu,
            vanuse_kaal,
            naitaja_kaal,
            kauguse_kaal,
            soo_kaal,
            mitu_lahimat,
            patsiendid,
            minid_ja_maxid,
        )
        oiged_naitajad.append(oige_naitaja_vaartus)
        ennustatud_naitajad.append(ennustatud_naitaja)

    rmse = arvuta_rmse(oiged_naitajad, ennustatud_naitajad)
    return rmse


def tuuni_kaalusid(
    andmed,
    epohhid,
    ennustatava_naitaja_nimetus,
    mitu_lahimat,
    patsiendid,
    minid_ja_maxid,
):

    parim_rmse = sys.maxsize
    parimad_kaalud = None
    koik_tulemused = []

    for i in range(epohhid):
        vanuse_kaal = random.random()
        naitaja_kaal = random.random()
        kauguse_kaal = random.random()
        soo_kaal = random.random()

        rmse = hinda_mudelit(
            andmed,
            vanuse_kaal,
            naitaja_kaal,
            kauguse_kaal,
            soo_kaal,
            ennustatava_naitaja_nimetus,
            mitu_lahimat,
            patsiendid,
            minid_ja_maxid,
        )

        koik_tulemused.append(
            ((vanuse_kaal, naitaja_kaal, kauguse_kaal, soo_kaal), rmse)
        )
        if rmse < parim_rmse:
            parim_rmse = rmse
            parimad_kaalud = (vanuse_kaal, naitaja_kaal, kauguse_kaal, soo_kaal)

        print("Epohh: ", str(i + 1), "/", epohhid)
        print(
            "Kaalud:",
            (vanuse_kaal, naitaja_kaal, kauguse_kaal, soo_kaal),
        )
        print("Saadud RMSE:", rmse)
        print("Siiani parim RMSE:", parim_rmse)
        print()

    return parimad_kaalud, parim_rmse, koik_tulemused


def treeni(
    treening_andmed,
    epohhid,
    ennustatava_naitaja_nimetus,
    mitu_lahimat,
    patsiendid,
    minid_ja_maxid,
):
    parimad_kaalud, parim_rmse, koik_tulemused = tuuni_kaalusid(
        treening_andmed,
        epohhid,
        ennustatava_naitaja_nimetus,
        mitu_lahimat,
        patsiendid,
        minid_ja_maxid,
    )
    return parim_rmse, parimad_kaalud


def testi(
    testandmed,
    parimad_kaalud,
    ennustatava_naitaja_nimetus,
    mitu_lahimat,
    patsiendid,
    minid_ja_maxid,
):
    return hinda_mudelit(
        testandmed,
        parimad_kaalud[0],
        parimad_kaalud[1],
        parimad_kaalud[2],
        parimad_kaalud[3],
        ennustatava_naitaja_nimetus,
        mitu_lahimat,
        patsiendid,
        minid_ja_maxid,
    )


def ennusta(
    vanus,
    naitaja,
    sugu,
    soovitud_vanus,
    parimad_kaalud,
    mitu_lahimat,
    patsiendid,
    minid_ja_maxid,
):
    loppvanus, tulemus = ennustus(
        vanus,
        naitaja,
        soovitud_vanus,
        sugu,
        parimad_kaalud[0],
        parimad_kaalud[1],
        parimad_kaalud[2],
        parimad_kaalud[3],
        mitu_lahimat,
        patsiendid,
        minid_ja_maxid,
    )
    return tulemus