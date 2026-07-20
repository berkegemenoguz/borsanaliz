from bist import main as bist_main
from viop import main as viop_main


def main():
    print("\n" + "=" * 40)
    print("  BORSA ANALİZ ARACI")
    print("=" * 40)
    print("  1. BIST Pay Piyasası")
    print("  2. VIOP Vadeli İşlemler")
    print("  q. Çıkış")
    print("=" * 40)

    while True:
        secim = input("\nSeçiminiz (1/2/q): ").strip().lower()

        if secim == "1":
            bist_main()
        elif secim == "2":
            viop_main()
        elif secim == "q":
            print("Çıkış yapılıyor.")
            break
        else:
            print("  Geçersiz seçim. 1, 2 veya q girin.")


if __name__ == "__main__":
    main()
