from heapq import heappush, heappop, heapify
from collections import defaultdict


def huffman_encoding(text):
    # Считаем частоту каждого символа
    freq = defaultdict(int)
    for char in text:
        freq[char] += 1
    #Создаем кучу, выше находяться символы с высокой частотой
    heap = [[weight, [symbol, '']] for symbol, weight in freq.items()]
    heapify(heap)

    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    huffman_code = sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))
    code_dict = dict(huffman_code)
    encoded_text = ''.join([code_dict[char] for char in text])
    return encoded_text, code_dict
   # return dict(huffman_code)


def huffman_decoding(encoded_text, code_dict):
    rev_dict = {v: k for k, v in code_dict.items()}
    current_code = ''
    decoded_text = ''
    for bit in encoded_text:
        current_code += bit
        if current_code in rev_dict:
            decoded_text += rev_dict[current_code]
            current_code = ''
    return decoded_text


#def compress(text):
#    code_dict = huffman_encoding(text)
#    encoded_text = ''.join([code_dict[char] for char in text])
#    return encoded_text, code_dict


def decompress(encoded_text, code_dict):
    return huffman_decoding(encoded_text, code_dict)


original_text = 'Prince Vasili always spoke languidly, like an actor repeating a stale part. Anna Pavlovna Scherer on the contrary, despite her forty years, overflowed with animation and impulsiveness. To be an enthusiast had become her social vocation and, sometimes even when she did not feel like it, she became enthusiastic in order not to disappoint the expectations of those who knew her. The subdued smile which, though it did not suit her faded features, always played round her lips expressed, as in a spoiled child, a continual consciousness of her charming defect, which she neither wished, nor could, nor considered it necessary, to correct.'
encoded_text, code_dict = huffman_encoding(original_text)
decoded_text = decompress(encoded_text, code_dict)

print(f'Original text: {original_text}')
print(f'Encoded text: {encoded_text}')
print(f'Decoded text: {decoded_text}')
print(f'Original size: {len(original_text)}')
print(f'Encoded size: {len(encoded_text)/8}')
print(f'Compression ratio:{(len(encoded_text) / (8*len(original_text))):.2f}')
