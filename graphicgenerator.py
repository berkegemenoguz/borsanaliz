import os
import borsapy as bp
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import MultipleLocator
import pandas as pd

GRAFIK_KLASORU = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grafikler")
os.makedirs(GRAFIK_KLASORU, exist_ok=True)


def hacim_format(v):
    if v >= 1_000_000_000:
        return f"{v / 1_000_000_000:.1f}B"
    if v >= 1_000_000:
        return f"{v / 1_000_000:.1f}M"
    if v >= 1_000:
        return f"{v / 1_000:.1f}K"
    return str(int(v))


def grafik_ciz(sembol, start, end, interval="5m"):
    hisse = bp.Ticker(sembol)
    df = hisse.history(start=start, end=end, interval=interval)

    if df.empty:
        print(f"  '{sembol}' için veri bulunamadı.")
        return

    if df.index.dtype != "int64":
        df["Datetime"] = pd.to_datetime(df.index)
        df = df.reset_index(drop=True)
    else:
        df["Datetime"] = pd.to_datetime(df["Datetime"])

    df = df.sort_values("Datetime").reset_index(drop=True)

    acilis = df.iloc[0]["Open"]
    kapanis = df.iloc[-1]["Close"]
    en_yuksek_idx = df["High"].idxmax()
    en_dusuk_idx = df["Low"].idxmin()
    en_yuksek = df.loc[en_yuksek_idx, "High"]
    en_dusuk = df.loc[en_dusuk_idx, "Low"]
    en_yuksek_saat = df.loc[en_yuksek_idx, "Datetime"].strftime("%H:%M")
    en_dusuk_saat = df.loc[en_dusuk_idx, "Datetime"].strftime("%H:%M")
    fark_tl = kapanis - acilis
    gun_ici_range = en_yuksek - en_dusuk
    degisim = (kapanis - acilis) / acilis * 100
    toplam_hacim = df["Volume"].sum()

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(14, 8),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True
    )
    fig.patch.set_facecolor("#0d1117")
    ax1.set_facecolor("#0d1117")
    ax2.set_facecolor("#0d1117")

    for i, row in df.iterrows():
        o, h, l, c = row["Open"], row["High"], row["Low"], row["Close"]
        renk = "#26a69a" if c >= o else "#ef5350"
        body_bottom = min(o, c)
        body_height = abs(c - o) if abs(c - o) > 0 else 0.001
        ax1.bar(i, body_height, bottom=body_bottom, color=renk, width=0.6, zorder=2)
        ax1.plot([i, i], [l, h], color=renk, linewidth=0.8, zorder=1)

    for i, row in df.iterrows():
        renk = "#26a69a" if row["Close"] >= row["Open"] else "#ef5350"
        ax2.bar(i, row["Volume"], color=renk, width=0.6, alpha=0.8)

    tick_step = max(1, len(df) // 12)
    ticks = list(range(0, len(df), tick_step))
    labels = [df.loc[i, "Datetime"].strftime("%H:%M") for i in ticks]
    ax2.set_xticks(ticks)
    ax2.set_xticklabels(labels, rotation=45, ha="right", color="#aaaaaa", fontsize=8)

    for ax in (ax1, ax2):
        ax.tick_params(colors="#aaaaaa")
        ax.spines[:].set_color("#333333")
        ax.yaxis.label.set_color("#aaaaaa")
        ax.grid(color="#1e2a38", linewidth=0.5, zorder=0)

    ax1.set_title(f"{sembol}  |  {start} - {end} |  {interval} mum grafik",
                  color="white", fontsize=13, pad=10)
    ax1.yaxis.set_major_locator(MultipleLocator(0.5))
    ax1.set_ylabel("Fiyat (TL)", color="#aaaaaa")
    ax2.set_ylabel("Hacim", color="#aaaaaa")

    yesil = mpatches.Patch(color="#26a69a", label="Yükseliş")
    kirmizi = mpatches.Patch(color="#ef5350", label="Düşüş")
    ax1.legend(handles=[yesil, kirmizi], facecolor="#161b22",
               labelcolor="white", edgecolor="#333333")

    degisim_ok = "▲" if degisim >= 0 else "▼"
    degisim_renk = "#26a69a" if degisim >= 0 else "#ef5350"
    fark_isaret = "+" if fark_tl >= 0 else ""

    ozet_satir = (
        f"Acilis: {acilis:.2f} TL   |   "
        f"Kapanis: {kapanis:.2f} TL   |   "
        f"En Yuksek: {en_yuksek:.2f} TL ({en_yuksek_saat})   |   "
        f"En Dusuk: {en_dusuk:.2f} TL ({en_dusuk_saat})   |   "
        f"Fark: {fark_isaret}{fark_tl:.2f} TL   |   "
        f"Range: {gun_ici_range:.2f} TL   |   "
        f"Hacim: {hacim_format(toplam_hacim)}   |   "
        f"{degisim_ok} {degisim:+.2f}%"
    )

    ax1.axhline(y=kapanis, color=degisim_renk, linestyle="--",
                linewidth=0.8, alpha=0.7, zorder=3)
    ax1.text(len(df) - 1, kapanis, f" {kapanis:.2f}",
             fontsize=7, color=degisim_renk, fontweight="bold",
             verticalalignment="center",
             bbox=dict(boxstyle="round,pad=0.2", facecolor="#161b22",
                       edgecolor=degisim_renk, alpha=0.9))

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.13)
    fig.text(0.5, 0.02, ozet_satir, ha="center", va="center",
             fontsize=8, fontfamily="monospace", color="white",
             bbox=dict(boxstyle="round,pad=0.5", facecolor="#161b22",
                       edgecolor="#333333", alpha=0.9))
    grafik_adi = f"Z{sembol}_{start}_{end}.png"
    grafik_yolu = os.path.join(GRAFIK_KLASORU, grafik_adi)
    plt.savefig(grafik_yolu, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"Grafik kaydedildi: {grafik_yolu}")
    plt.show()


if __name__ == "__main__":
    sembol = input("Hisse kodu: ").strip().upper()
    start = input("Başlangıç tarihi (YYYY-MM-DD): ").strip()
    end = input("Bitiş tarihi (YYYY-MM-DD): ").strip()
    interval = input("Interval (5m/15m/1h) [5m]: ").strip() or "5m"
    grafik_ciz(sembol, start, end, interval)
