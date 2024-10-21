def hex_to_int(hex_ip):
    return int(hex_ip.replace('.', ''), 16)

def int_to_hex_ip(int_ip):
    return '.'.join([f"{(int_ip >> i) & 0xFF:02X}" for i in (24, 16, 8, 0)])

def cidr_match(ip, network, subnet_mask):
    ip_int = hex_to_int(ip)
    network_int = hex_to_int(network)
    mask_int = hex_to_int(subnet_mask)
    return (ip_int & mask_int) == (network_int & mask_int)

def forward_ip(ip_address):
    matches = []
    best_match = None
    longest_prefix = -1

    for entry in routing_table:
        network, prefix_length = entry[0].split('/')
        subnet_mask = entry[1]
        
        if cidr_match(ip_address, network, subnet_mask):
            matches.append(entry)
            if int(prefix_length) > longest_prefix:
                longest_prefix = int(prefix_length)
                best_match = entry

    if best_match:
        return matches, best_match
    else:
        return [default_route], default_route

def print_routing_table():
    print("Routing Table:")
    print("Network ID      Subnet Mask     Interface")
    print("-" * 45)
    for entry in routing_table:
        print(f"{entry[0]:<15} {entry[1]:<15} {entry[2]}")
    
    # Print default route
    print(f"{default_route[0]:<15} {default_route[1]:<15} {default_route[2]}")

def calculate_subnet_mask(prefix_length):
    mask = (0xFFFFFFFF << (32 - prefix_length)) & 0xFFFFFFFF
    return '.'.join([f"{(mask >> i) & 0xFF:02X}" for i in (24, 16, 8, 0)])

# Global routing table
routing_table = [
    ("C4.5E.02.00/23", calculate_subnet_mask(23), "Interface_A"),
    ("C4.5E.04.00/22", calculate_subnet_mask(22), "Interface_B"),
    ("C4.5E.C0.00/19", calculate_subnet_mask(19), "Interface_C"),
    ("C4.5E.40.00/18", calculate_subnet_mask(18), "Interface_D"),
    ("C4.4C.00.00/14", calculate_subnet_mask(14), "Interface_E"),
    ("C0.00.00.00/2", calculate_subnet_mask(2), "Interface_F"),
    ("80.00.00.00/1", calculate_subnet_mask(1), "Interface_G")
]

# Default route
default_route = ("00.00.00.00/0", "00.00.00.00", "Default_Interface")

# Print the routing table
print_routing_table()

# Test the function
test_ips = [
    "C4.5E.41.01"
    "C4.4B.31.2E",
    "C4.5E.05.09",
    "C4.4D.31.2E",
    "C4.5E.03.87",
    "C4.5E.7F.12",
    "C4.5E.D1.02"
    # "A1.B2.C3.D4", # This IP will use the default route
    # "C4.6A.3B.4F",
    # "C4.5E.12.8C",
    # "04.7D.45.9A",
    # "C4.3F.22.B1",
    # "C4.5E.BF.00",
    # "C4.5B.04.01",
    # "12.00.FF.FF",
    # "12.00.00.00",j
    # "C0.00.00.00",
    # "FF.FF.FF.FF"
# "C4.5E.EA.07"
# C4.49.B1.3C
]

print("\nTesting IP Forwarding:")
for ip in test_ips:
    matching_entries, best_match = forward_ip(ip)
    print(f"IP: {ip}")
    if len(matching_entries) > 1:
        print("  Matching entries:")
        for entry in matching_entries:
            print(f"    Network ID: {entry[0]:<15} Subnet Mask: {entry[1]:<15} Interface: {entry[2]}")
    print(f"  Best match (longest prefix):")
    print(f"    Network ID: {best_match[0]:<15} Subnet Mask: {best_match[1]:<15} Interface: {best_match[2]}")
    print(f"  Forwarding to: {best_match[2]}\n")