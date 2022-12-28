from backend.util.hex_to_binary import hex_to_binary

def test_hex_to_binary():
    original_number = 123456789
    hex_number = hex(original_number)[2:] # strip 0x
    binary_number = hex_to_binary(hex_number)

    assert int(binary_number, 2) == original_number