import borsapy as bp
import pandas as pd

# Tüm şirketler
sirketler = bp.companies()

# DataFrame'e çevir
df = pd.DataFrame(sirketler)
print(f"Toplam şirket sayısı: {len(df)}")
print(df)

# CSV olarak kaydet
df.to_csv("bist_sirketleri.csv", index=False, encoding="utf-8")
print("bist_sirketleri.csv olarak kaydedildi")