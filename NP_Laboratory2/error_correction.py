import math


def is_power_of_two(n):
    m = math.log(n, 2)
    return m == int(m)


def power_2_below(n):
    return 2 ** int(math.log(n, 2))


def covers(i, j):
    return (j >> int(math.log(i, 2))) % 2 == 1


def sum_bits(bits, i, j):
    if j > len(bits):
        return 0
    else:
        rest_answer = sum_bits(bits, i, j + 1)
        if covers(i, j):
            return bits[j - 1] + rest_answer
        else:
            return rest_answer


def has_odd_parity(bits, i):
    return sum_bits(bits, i, i) % 2 == 1


def has_even_parity(bits, i):
    return not (has_odd_parity(bits, i))


def bits_to_number(bits):
    if bits == []:
        return 0
    else:
        n = bits[0] * (2 ** (len(bits) - 1))
        return n + bits_to_number(bits[1:])


def prepare(bits, i):
    if bits == []:
        return []
    else:
        if is_power_of_two(i):
            return [0] + prepare(bits, i + 1)
        else:
            return [bits[0]] + prepare(bits[1:], i + 1)


def set_parity_bits(bits, i):
    if i > len(bits):
        return []
    else:
        rest_answer = set_parity_bits(bits, i + 1)
        if is_power_of_two(i):
            if has_odd_parity(bits, i):
                return [0] + rest_answer
            else:
                return [1] + rest_answer
        else:
            return [bits[i - 1]] + rest_answer


def encode(string):
    bits = [int(i) for i in text_to_bits(string)]
    paritys_are_zero = prepare(bits, 1)
    result = ''.join(str(e) for e in set_parity_bits(paritys_are_zero, 1))
    return result


def decode(string):
    bits = [int(i) for i in string]
    parity_results = check_parity(bits, power_2_below(len(bits)))
    n = bits_to_number(parity_results)

    if n != 0:
        print("NB: bit ", n, " is bad. Flipping.")
        bits[n - 1] = 1 - bits[n - 1]

    return text_from_bits(extract_data(bits, 1))


def extract_data(bits, i):
    if i > len(bits):
        return []
    else:
        rest_answer = extract_data(bits, i + 1)
        if is_power_of_two(i):
            return rest_answer
        else:
            return [bits[i - 1]] + rest_answer


def check_parity(bits, i):
    if i == 1:
        return [0] if has_odd_parity(bits, i) else [1]
    else:
        bit = 0 if has_odd_parity(bits, i) else 1
        return [bit] + check_parity(bits, power_2_below(i - 1))


def text_to_bits(text, encoding='utf-8'):
    bits = bin(int.from_bytes(text.encode(encoding), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def text_from_bits(bits):
    n = int(''.join(map(str, bits)), 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

# if __name__ == "__main__":
#     string = 'Test message1sads'
#     print('string>>>', string)
#     print('string length>>>', len(string))
#
#     f = encode(string)
#     print('encoded>>>', f)
#     d = decode(f)
#     print(d)
#     print('Decoded>>>', d)
