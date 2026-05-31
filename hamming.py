import numpy as np

# (7,4) Hamming Kodu icin Uretec Matrisi G = [I_4 | P]
G = np.array([
    [1, 0, 0, 0, 1, 0, 1],
    [0, 1, 0, 0, 0, 1, 1],
    [0, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 1, 1, 1, 0]
], dtype=int)

# Parity-Check Matrisi H
H = np.array([
    [1, 0, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 0, 1, 0],
    [1, 1, 1, 0, 0, 0, 1]
], dtype=int)

N_HAMMING = 7
K_HAMMING = 4

def hamming_encode(message_bits):
    u = np.array(message_bits, dtype=int)
    if u.shape[0] != K_HAMMING:
        raise ValueError(f"Hata: Mesaj blogu tam olarak {K_HAMMING} bit olmalidir!")
    raw_multiplication = np.dot(u, G)
    codeword = raw_multiplication % 2
    return codeword

def hamming_decode(received_bits):
    """
    Alinan 7 bitlik r blogunun H^T ile carpimini alarak
    3 bitlik sendrom vektorunu hesaplar.
    """
    r = np.array(received_bits, dtype=int)
    
    if r.shape[0] != N_HAMMING:
        raise ValueError(f"Hata: Alinan blok tam olarak {N_HAMMING} bit olmalidir!")
        
    # H matrisinin transpozunu al (H^T)
    H_transpose = H.T
    
    # Sendrom hesabi: S = r * H^T
    raw_syndrome = np.dot(r, H_transpose)
    
    # GF(2) aritmetigi icin mod 2 islemi
    syndrome = raw_syndrome % 2
    
    # Eger sendrom tamamen 0 ise hata yoktur
    if np.all(syndrome == 0):
        return r[0:K_HAMMING]
        
    # Sendrom sifirdan farkliysa hatali biti bul
    error_index = -1
    for i in range(N_HAMMING):
        if np.array_equal(H[:, i], syndrome):
            error_index = i
            break
            
    # Hatali bit bulunduysa ters cevir
    if error_index != -1:
        r[error_index] = 1 - r[error_index]
        
    return r[0:K_HAMMING]