import numpy as np

# (7,4) Hamming Kodu için Sistematik Üreteç Matrisi G = [I_4 | P] 
G = np.array([
    [1, 0, 0, 0, 1, 0, 1],
    [0, 1, 0, 0, 0, 1, 1],
    [0, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 1, 1, 1, 0]
], dtype=int)

N_HAMMING = 7
K_HAMMING = 4

def hamming_encode(message_bits):
    """
    4 bitlik bir u mesaj bloğunu alır ve c = u * G (mod 2) 
    formülüyle 7 bitlik Hamming kod sözcüğüne dönüştürür.
    """
    # Gelen girdiyi bir NumPy dizisine dönüştür
    u = np.array(message_bits, dtype=int)
    
    # Boyut kontrolü 
    if u.shape[0] != K_HAMMING:
        raise ValueError(f"Hata: Mesaj bloğu tam olarak {K_HAMMING} bit olmalıdır!")
        
    # Standart matris çarpımı gerçekleştir (u * G)
    raw_multiplication = np.dot(u, G)
    
    # GF(2) aritmetiği için mod 2 işlemini uygula
    codeword = raw_multiplication % 2
    
    return codeword

def hamming_decode(received_bits):
    # Daha sonra içi doldurulacaktır
    pass