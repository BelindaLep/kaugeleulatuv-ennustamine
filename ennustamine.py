from functions import *
import pickle

# Piiritletud osa muuta vastavalt vajadusele!
# -------------------------------------------
hetke_vanus = 22
hetke_naitaja_vaartus = 175
sugu = 0 # 0 - naine, 1 - mees
vanus_ennustamiseks = 80

mudeli_fail = "treenitud_mudel"
# --------------------------------------------

with open(f"{mudeli_fail}.pkl", "rb") as file:
    parimad_kaalud, patsiendid, mitu_lahimat, minid_ja_maxid, ennustatava_tunnuse_nimetus = pickle.load(file)


tulemus = ennusta(
    hetke_vanus, hetke_naitaja_vaartus, sugu, vanus_ennustamiseks, parimad_kaalud, mitu_lahimat, patsiendid, minid_ja_maxid
)
print(str(vanus_ennustamiseks) + "-aastaselt on sinu " + ennustatava_tunnuse_nimetus + " " + str(round(tulemus, 1)))
