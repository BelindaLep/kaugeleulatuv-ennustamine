from functions import *
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle

# Piiritletud osa muuta vastavalt vajadusele!
# ---------------------------------------------------------------------------
ennustatava_naitaja_nimetus = "pikkus"
epohhid = 10
mitu_lahimat = 2
min_mootmisi_per_patsient = 3

alusandmestik_df = pd.read_excel("alusandmed.xlsx")
treening_ja_test_andmed = pd.read_excel("treening_ja_test.xlsx")

test_suurus = 0.2

# mudeli_fail = "treenitud_mudel"
# ---------------------------------------------------------------------------


treening_ja_test_andmed = treening_ja_test_andmed.sample(frac=1)
treening_andmed, test_andmed = train_test_split(
    treening_ja_test_andmed, test_size=test_suurus, random_state=42
)

min_vanus = alusandmestik_df["vanus"].min()
max_vanus = alusandmestik_df["vanus"].max()
min_sugu = alusandmestik_df["sugu"].min()
max_sugu = alusandmestik_df["sugu"].max()
min_naitaja = alusandmestik_df[ennustatava_naitaja_nimetus].min()
max_naitaja = alusandmestik_df[ennustatava_naitaja_nimetus].max()

minid_ja_maxid = [min_vanus, max_vanus, min_naitaja, max_naitaja, min_sugu, max_sugu]

alusandmestik_df = alusandmestik_df.sort_values(by=["patsient", "vanus"])
alusandmestik_df = alusandmestik_df.groupby("patsient")

patsiendid = looPatsiendid(
    alusandmestik_df, ennustatava_naitaja_nimetus, min_mootmisi_per_patsient
)

parimrmse, parimad_kaalud = treeni(
    treening_andmed,
    epohhid,
    ennustatava_naitaja_nimetus,
    mitu_lahimat,
    patsiendid,
    minid_ja_maxid,
)

print("Treenimise parim RMSE:", parimrmse)
print("See on saadud kaaludega:")
print("vanus", parimad_kaalud[0])
print(ennustatava_naitaja_nimetus, parimad_kaalud[1])
print("kaugus", parimad_kaalud[2])
print("sugu", parimad_kaalud[3])
print()

testtulemus = testi(
    test_andmed,
    parimad_kaalud,
    ennustatava_naitaja_nimetus,
    mitu_lahimat,
    patsiendid,
    minid_ja_maxid,
)
print("Testimise RMSE:", testtulemus)

# with open(f"{mudeli_fail}.pkl", "wb") as f:
#     pickle.dump((parimad_kaalud, patsiendid, mitu_lahimat, minid_ja_maxid, ennustatava_naitaja_nimetus), f)
