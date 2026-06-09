import numpy as np

def convolutional_encode(message_bits):
    """
    Giris bit dizisini K=3, Rate=1/2 yapisinda konvolusyonel olarak kodlar.
    g1(D) = D^2 + 1 ve g2(D) = D^2 + D + 1 polinomlarini kullanir.
    Sequence sonuna K-1 adet sifir ekleyerek termination saglar.
    """
    input_bits = list(message_bits)
    
    # Encoder'i sifir durumuna dondurmek icin K-1 adet tail bit ekleme
    tail_bits = [0, 0]
    padded_bits = input_bits + tail_bits
    
    # Bellek elemanlarinin ilk durum tanimi
    m1 = 0
    m2 = 0
    
    encoded_sequence = []
    
    # Durum gecis mantiginin kurulmasi
    for bit in padded_bits:
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


def viterbi_decode(received_bits):
    """
    Alinan gurultulu bit dizisini Viterbi algoritmasi kullanarak cozer.
    Kafes yapisi uzerinde en kucuk Hamming mesafesine sahip yolu arar.
    """
    r = np.array(received_bits, dtype=int)
    num_steps = len(r) // 2
    
    # Kafes yapisindaki 4 durum tanimi
    trellis_transitions = {
        0: {0: [0, 0, 0, 0], 1: [1, 1, 1, 1]},
        1: {0: [0, 1, 2, 0], 1: [1, 0, 3, 1]},
        2: {0: [1, 1, 0, 0], 1: [0, 0, 1, 1]},
        3: {0: [1, 0, 2, 0], 1: [0, 1, 3, 1]}
    }
    
    path_metrics = {0: 0, 1: float('inf'), 2: float('inf'), 3: float('inf')}
    history = []
    
    # Tum zaman adimlari boyunca branch metric hesabı
    for step in range(num_steps):
        r1, r2 = r[2*step], r[2*step+1]
        next_path_metrics = {0: float('inf'), 1: float('inf'), 2: float('inf'), 3: float('inf')}
        step_history = {}
        
        for current_state, transitions in trellis_transitions.items():
            if path_metrics[current_state] == float('inf'):
                continue
                
            for input_bit, outputs in transitions.items():
                c1, c2, next_state, _ = outputs
                
                # Branch metric hesabi
                branch_metric = (r1 ^ c1) + (r2 ^ c2)
                
                # Path metric guncellemesi (Add-Compare-Select)
                new_path_metric = path_metrics[current_state] + branch_metric
                
                # En kucuk maliyetli yolu secme
                if new_path_metric < next_path_metrics[next_state]:
                    next_path_metrics[next_state] = new_path_metric
                    step_history[next_state] = (current_state, input_bit)
                    
        path_metrics = next_path_metrics
        history.append(step_history)
        
    # Geriye dogru izleme adimi (Traceback)
    decoded_bits = []
    current_state = 0
    
    for step in reversed(range(num_steps)):
        prev_state, input_bit = history[step][current_state]
        decoded_bits.append(input_bit)
        current_state = prev_state
        
    decoded_bits.reverse()
    
    # Tail bitlerini temizleyerek orijinal mesaji dondur
    return np.array(decoded_bits[:-2], dtype=int)