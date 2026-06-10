import numpy as np
from hamming import hamming_encode, hamming_decode
from convolutional import convolutional_encode, viterbi_decode
from channel import binary_symmetric_channel, calculate_bit_errors

def run_concatenated_pipeline(message_bits, ber, seed=None):
    """
    Hamming ve Konvolusyonel kodlari ardisik (serial concatenation) baglar.
    Veriyi sirasiyla kodlar, kanaldan gecirir ve tersi sirayla cozer.
    """
    # Hamming kodlama adimi (Blok kodlama)
    hamming_encoded = []
    for i in range(0, len(message_bits), 4):
        block = message_bits[i:i+4]
        encoded_block = hamming_encode(block)
        hamming_encoded.extend(encoded_block)
        
    # Konvolusyonel kodlama adimi (Surekli kodlama)
    fully_encoded = convolutional_encode(hamming_encoded)
    
    # Gurultulu kanal (BSC) simülasyonu
    channel_output = binary_symmetric_channel(fully_encoded, ber, seed=seed)
    
    # Viterbi kod cozme adimi (Ic cozucu)
    viterbi_decoded = viterbi_decode(channel_output)
    
    # Hamming kod cozme adimi (Dis cozucu)
    final_decoded_bits = []
    for i in range(0, len(viterbi_decoded), 7):
        block = viterbi_decoded[i:i+7]
        decoded_block = hamming_decode(block)
        final_decoded_bits.extend(decoded_block)
        
    return fully_encoded, channel_output, final_decoded_bits

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
    
    # Orijinal mesaj metnini bit dizisine cevirme
    message_bytes = personal_message.encode('utf-8')
    source_bits = []
    for b in message_bytes:
        bits_str = bin(b)[2:].zfill(8)
        source_bits.extend([int(x) for x in bits_str])
        
    # Veri toplama matrislerinin ilklenmesi
    channel_error_matrix = np.zeros((len(seeds), len(channel_bers)))
    system_error_matrix = np.zeros((len(seeds), len(channel_bers)))
    
    # Ana simülasyon dongusunun kurulmasi
    print("\n--- Ana Simulasyon Dongusu Baslatiliyor ---")
    for s_idx, s in enumerate(seeds):
        print(f"\n>> Seed {s} icin veriler toplaniyor:")
        for b_idx, ber in enumerate(channel_bers):
            # Her kombinasyon icin ardisik hattin calistirilmasi
            fully_encoded, channel_output, final_decoded_bits = run_concatenated_pipeline(source_bits, ber, seed=s)
            
            # Pre-decoding (Kanal uzerindeki) hata hesabi
            pre_errors = calculate_bit_errors(fully_encoded, channel_output)
            channel_error_matrix[s_idx, b_idx] = pre_errors / len(fully_encoded)
            
            # Post-decoding (Sistem cikisindaki) hata hesabi
            post_errors = calculate_bit_errors(source_bits, final_decoded_bits)
            system_error_matrix[s_idx, b_idx] = post_errors / len(source_bits)
            
            # Hesaplama ciktilarinin ekrana basilmasi
            print(f"   BER: {ber:<5} | Kanal Hatasi: {channel_error_matrix[s_idx, b_idx]:.5f} | Sistem Hatasi: {system_error_matrix[s_idx, b_idx]:.5f}")

if __name__ == "__main__":
    main()