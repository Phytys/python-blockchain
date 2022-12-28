from backend.util.crypto_hash import crypto_hash



HEX_TO_BINARY_TABLE = {
"0": "0000",
"1": "0001",
"2": "0010",
"3": "0011",
"4": "0100",
"5": "0101",
"6": "0110",
"7": "0111",
"8": "1000",
"9": "1001",
"a": "1010",
"b": "1011",
"c": "1100",
"d": "1101",
"e": "1110",
"f": "1111"
}
# print(HEX_TO_BINARY_TABLE)

def hex_to_binary(hex_string):
    binary_string = ""

    for c in hex_string:
        binary_string += HEX_TO_BINARY_TABLE[c]

    return binary_string


def main():

    number = 123456789
    hex_number = hex(number)[2:] # remove 0x
    print(f"hex number is: {hex_number}")

    binary_number = hex_to_binary(hex_number)
    print(f"Binary number is: {binary_number}")

    original_number = int(binary_number, 2)
    print(f"Original number is: {original_number}")

    hex_to_binary_crypto_hash = hex_to_binary(crypto_hash("test-data"))
    print(f"hex to binary crypto hash: {hex_to_binary_crypto_hash}")

if __name__ == "__main__":
    main()