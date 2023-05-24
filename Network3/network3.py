from collections import Counter
from typing import Dict, List, Tuple


def shannon_fano_encode(text: str) -> Tuple[str, Dict[str, str]]:
    # Частота вхождения каждого символа
    freqs = Counter(text)
    # Сортируем по частоте
    sorted_chars = sorted(freqs.items(), key=lambda x: -x[1])
    # Совокупная частота встречаемости
    com_freq = [0]
    for char, freq in sorted_chars:
        com_freq.append(com_freq[-1] + freq)
    # Средняя точка каждого диапазона встречаемости
    midpoint = {}
    for i in range(len(sorted_chars)):
        char, freq = sorted_chars[i]
        midpoint[char] = com_freq[i] + freq / 2
    # Разбиваем на группы по этому признаку
    group1, group2 = [], []
    for char, freq in sorted_chars:
        if midpoint[char] < com_freq[len(com_freq) - 1] / 2:
            group1.append(char)
        else:
            group2.append(char)
    # Рекурсивно кодируем эти группы символов
    code_map = {}
    if len(group1) > 1:
        group1_code, group1_map = shannon_fano_encode(''.join(group1))
        for char, code in group1_map.items():
            code_map[char] = '0' + code
    elif len(group1) == 1:
        code_map[group1[0]] = '0'
    if len(group2) > 1:
        group2_code, group2_map = shannon_fano_encode(''.join(group2))
        for char, code in group2_map.items():
            code_map[char] = '1' + code
    elif len(group2) == 1:
        code_map[group2[0]] = '1'
    # Кодируем исходный текст
    encoded_text = ''.join([code_map[char] for char in text])
    return encoded_text, code_map


def shannon_fano_decode(encoded_text: str, code_map: Dict[str, str]) -> str:
    # Инвертируем список кодов для букв
    inv_code_map = {v: k for k, v in code_map.items()}
    decoded_text = ''
    current_code = ''
    # Декодируем
    for bit in encoded_text:
        current_code += bit
        if current_code in inv_code_map:
            decoded_text += inv_code_map[current_code]
            current_code = ''
    return decoded_text


text = 'Prince Vasili always spoke languidly, like an actor repeating a stale part. Anna Pavlovna Scherer on the contrary, despite her forty years, overflowed with animation and impulsiveness. To be an enthusiast had become her social vocation and, sometimes even when she did not feel like it, she became enthusiastic in order not to disappoint the expectations of those who knew her. The subdued smile which, though it did not suit her faded features, always played round her lips expressed, as in a spoiled child, a continual consciousness of her charming defect, which she neither wished, nor could, nor considered it necessary, to correct.'
encoded_text, code_map = shannon_fano_encode(text)
print(f'Original text size: {len(text)}')
print(f'Encoded text size: {len(encoded_text)}')
print(f'Encoded text: {encoded_text}')
decoded_text = shannon_fano_decode(encoded_text, code_map)
print(f'Decoded text: {decoded_text}')


print(f'Encoded text size (bytes): {len(encoded_text)/8}')
compression_ratio = len(encoded_text) / (8*len(text))
print(f'Compression ratio: {compression_ratio:.2f}')
