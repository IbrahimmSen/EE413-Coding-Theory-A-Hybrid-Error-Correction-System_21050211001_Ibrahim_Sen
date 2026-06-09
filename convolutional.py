import numpy as np

def convolutional_encode(message_bits):
    """
    Giris bit dizisini K=3, Rate=1/2 yapisinda konvolusyonel olarak kodlar.
    g1(D) = D^2 + 1 ve g2(D) = D^2 + D + 1 polinomlarini kullanir.
    Sequence sonuna K-1 adet sifir ekleyerek termination saglar.
    """
    input_bits = list(message_bits)
    
    # Bellek elemanlarinin ilk durum tanimi
    m1 = 0
    m2 = 0
    
    encoded_sequence = []
    
    # Durum gecis mantiginin kurulmasi
    for bit in input_bits:
        m0 = bit
        
        # g1(D) = D^2 + 1
        c1 = m0 ^ m2
        
        # g2(D) = D^2 + D + 1
        c2 = m0 ^ m1 ^ m2
        
        # Cikis ciftini eklenmesi
        encoded_sequence.append(c1)
        encoded_sequence.append(c2)
        
        # Bellek durumlarinin guncellenmesi
        m2 = m1
        m1 = m0
        
    return np.array(encoded_sequence, dtype=int)