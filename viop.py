import borsapy as bp

AY_KODLARI = ["N2026", "Q2026", "V2026", "Z2026"]  # Temmuz, Ağustos, Ekim, Aralık

hisseler = ["GARAN", "AKBNK", "ASELS", "EREGL", "TUPRS", "SISE"]

for hisse in hisseler:
    bulunanlar = []
    for ay in AY_KODLARI:
        sembol = f"{hisse}{ay}"
        try:
            df = bp.Ticker(sembol).history(period="5g")
            if len(df) > 0:
                son_hacim = df.iloc[-1]["Volume"]
                bulunanlar.append(f"{sembol}(hacim:{son_hacim:.0f})")
        except:
            pass
    if bulunanlar:
        print(f"{hisse}: {', '.join(bulunanlar)}")
    else:
        print(f"{hisse}: VIOP kontrati yok")



        df = hisse.history(
            start="2026-06-30",
            end="2026-06-30",
            interval="1h"
        )
        print(df)
        print("Satır sayısı:", len(df))