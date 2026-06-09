import numpy as np

def binary_symmetric_channel(bits, ber):
    """
    Giris bit dizisini verilen BER degerine gore Binary Symmetric Channel uzerinden gecirir.
    Hattan gecen her bitin olasiliksal olarak yonunu tersine cevirir.
    """
    transmitted_bits = np.array(bits, dtype=int)
    num_bits = len(transmitted_bits)
    
    # Verilen BER olasiligina gore rastgele hata maskesi olusturma
    error_mask = np.random.rand(num_bits) < ber
    
    # Hata maskesindeki True olan bitleri XOR ile ters cevirme
    received_bits = transmitted_bits ^ error_mask.astype(int)
    
    return received_bits