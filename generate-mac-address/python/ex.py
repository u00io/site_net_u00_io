
import random
from typing import List


def normalize_first_byte(byte: int, locally_administered: bool) -> int:
    # Clear I/G bit (bit 0) → unicast
    byte &= 0b11111110

    # Set or clear U/L bit (bit 1)
    if locally_administered:
        byte |= 0b00000010
    else:
        byte &= 0b11111101

    return byte


def generate_mac_addresses(
    prefix: str = "",
    locally_administered: bool = True,
    count: int = 1
) -> List[str]:
    """
    Generate MAC addresses.

    :param prefix: Optional hex prefix (e.g. '02:AB:CD' or '02ABCD')
    :param locally_administered: Set U/L bit if True
    :param count: Number of MAC addresses to generate
    :return: List of MAC address strings
    """

    # Normalize prefix
    hex_prefix = "".join(c for c in prefix if c.isalnum()).upper()
    if len(hex_prefix) % 2 != 0 or len(hex_prefix) > 10:
        raise ValueError("Prefix must contain 0–5 bytes")

    prefix_bytes = [
        int(hex_prefix[i:i + 2], 16)
        for i in range(0, len(hex_prefix), 2)
    ]

    macs = []

    for _ in range(count):
        bytes_ = prefix_bytes.copy()

        # Generate remaining bytes
        while len(bytes_) < 6:
            bytes_.append(random.randint(0, 255))

        # Normalize first byte
        bytes_[0] = normalize_first_byte(bytes_[0], locally_administered)

        mac = ":".join(f"{b:02X}" for b in bytes_)
        macs.append(mac)

    return macs


# Example usage
if __name__ == "__main__":
    macs = generate_mac_addresses(
        prefix="02:AB",
        locally_administered=True,
        count=3
    )

    for mac in macs:
        print(mac)
