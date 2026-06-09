import numpy as np

def binary_symmetric_channel(bits, ber, seed=None):
    """
    Giris bit dizisini verilen BER degerine gore Binary Symmetric Channel uzerinden gecirir.
    Hattan gecen her bitin olasiliksal olarak yonunu tersine cevirir.
    """
    if seed is not None:
        np.random.seed(seed)
        
    transmitted_bits = np.array(bits, dtype=int)
    num_bits = len(transmitted_bits)
    
    # Verilen BER olasiligina gore rastgele hata maskesi olusturma
    error_mask = np.random.rand(num_bits) < ber
    
    # Hata maskesindeki True olan bitleri XOR ile ters cevirme
    received_bits = transmitted_bits ^ error_mask.astype(int)
    
    return received_bits

def calculate_bit_errors(original_bits, decoded_bits):
    """
    Orijinal bit dizisi ile cozulmus bit dizisi arasindaki farkli bit sayisini hesaplar.
    """
    orig = np.array(original_bits, dtype=int)
    dec = np.array(decoded_bits, dtype=int)
    
    if len(orig) != len(dec):
        raise ValueError("Hata: Karsilastirilacak bit dizilerinin boyutlari esit olmalidir!")
        
    # Farkli olan bitlerin toplam sayisini bulma
    error_count = np.sum(orig != dec)
    
    return error_count