import borsapy as bp

start = "2026-07-01"
end = "2026-07-01"

hisse = bp.Ticker("THYAO")
df = hisse.history(
    start=start,
    end=end,
    interval="5m"
)

# Tarih ve saat sütununu ayır
df["Tarih"] = df.index.date
df["Saat"] = df.index.time
df = df.reset_index(drop=True)

dosya_adi = f"thyaobist_{start}//{end}.csv"
df.to_csv(dosya_adi, index=False, encoding="utf-8")
print(f"{dosya_adi} olarak kaydedildi")