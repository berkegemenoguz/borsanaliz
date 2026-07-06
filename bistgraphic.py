import borsapy as bp
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

#parameters
sembol = "THYAO"
start = "2026-07-01"
end = "2026-07-01"
interval = "5m"

#data
hisse = bp.Ticker(sembol)
df = hisse.history(start=start, end=end, interval=interval)

# Index datetime row
if df.index.dtype != "int64":
    df["Datetime"] = pd.to_datetime(df.index)
    df = df.reset_index(drop=True)
else:
    df["Datetime"] = pd.to_datetime(df["Datetime"])

df = df.sort_values("Datetime").reset_index(drop=True)

#csv
dosya_adi = f"{sembol}_{start}_{end}"
df["Tarih"] = df["Datetime"].dt.date
df["Saat"] = df["Datetime"].dt.time
df.to_csv(f"{dosya_adi}.csv", index=False, encoding="utf-8")
print(f"CSV kaydedildi: {dosya_adi}.csv")

#candlestick
fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(14, 8),
    gridspec_kw={"height_ratios": [3, 1]},
    sharex=True
)
fig.patch.set_facecolor("#0d1117")
ax1.set_facecolor("#0d1117")
ax2.set_facecolor("#0d1117")

x = range(len(df))

for i, row in df.iterrows():
    o, h, l, c = row["Open"], row["High"], row["Low"], row["Close"]
    renk = "#26a69a" if c >= o else "#ef5350"  # red/green

    #body
    body_bottom = min(o, c)
    body_height = abs(c - o) if abs(c - o) > 0 else 0.001
    ax1.bar(i, body_height, bottom=body_bottom, color=renk, width=0.6, zorder=2)

    #wick
    ax1.plot([i, i], [l, h], color=renk, linewidth=0.8, zorder=1)

#volume
for i, row in df.iterrows():
    renk = "#26a69a" if row["Close"] >= row["Open"] else "#ef5350"
    ax2.bar(i, row["Volume"], color=renk, width=0.6, alpha=0.8)

# X axis notes
tick_step = max(1, len(df) // 12)
ticks = list(range(0, len(df), tick_step))
labels = [df.loc[i, "Datetime"].strftime("%H:%M") for i in ticks]
ax2.set_xticks(ticks)
ax2.set_xticklabels(labels, rotation=45, ha="right", color="#aaaaaa", fontsize=8)

#style
for ax in (ax1, ax2):
    ax.tick_params(colors="#aaaaaa")
    ax.spines[:].set_color("#333333")
    ax.yaxis.label.set_color("#aaaaaa")
    ax.grid(color="#1e2a38", linewidth=0.5, zorder=0)

ax1.set_title(f"{sembol}  |  {start}  |  {interval} mum grafik",
              color="white", fontsize=13, pad=10)
ax1.set_ylabel("Fiyat (TL)", color="#aaaaaa")
ax2.set_ylabel("Hacim", color="#aaaaaa")

yesil = mpatches.Patch(color="#26a69a", label="Yükseliş")
kirmizi = mpatches.Patch(color="#ef5350", label="Düşüş")
ax1.legend(handles=[yesil, kirmizi], facecolor="#161b22",
           labelcolor="white", edgecolor="#333333")

plt.tight_layout()
grafik_adi = f"{dosya_adi}_candlestick.png"
plt.savefig(grafik_adi, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"Grafik kaydedildi: {grafik_adi}")
plt.show()