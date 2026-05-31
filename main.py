
import numpy as np
from hamming import hamming_encode

def main():
    # Proje parametreleri ve ana degiskenler
    personal_message = "ECC2026-S02B"
    seeds = [4129, 9533, 17021]
    channel_bers = [0.001, 0.01, 0.05, 0.10, 0.15]
    
    print("--- Sistem Parametreleri ---")
    print(f"Mesaj: {personal_message}")
    print(f"Seeds: {seeds}")
    print(f"BER Listesi: {channel_bers}\n")
    
    # Hamming kodlayici fonksiyon testi
    print("--- Hamming Kodlayici Testi ---")
    test_bits = [1, 0, 1, 1]
    codeword = hamming_encode(test_bits)
    
    print(f"Giris Blogu (u): {test_bits}")
    print(f"Kod Sozcugu (c): {list(codeword)}")

if __name__ == "__main__":
    main()