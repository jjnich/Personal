def solution(N):
    binary = bin(N)[2:]  # Convert to binary string without '0b' prefix
    
    max_gap = 0
    current_gap = 0
    found_one = False
    
    for bit in binary:
        if bit == '1':
            if found_one:
                max_gap = max(max_gap, current_gap)
            found_one = True
            current_gap = 0
        else:  # bit == '0'
            if found_one:
                current_gap += 1
    
    return max_gap

def main():
    # Test cases from the problem
    test_cases = [
        (9, 2),      # 1001 -> gap of 2
        (529, 4),    # 1000010001 -> gaps of 4 and 3, max is 4
        (20, 1),     # 10100 -> gap of 1
        (15, 0),     # 1111 -> no gaps
        (32, 0),     # 100000 -> no gaps (trailing zeros don't count)
        (1041, 5),   # 10000010001 -> gap of 5
        (1, 0),      # 1 -> no gaps
        (5, 1),      # 101 -> gap of 1
    ]
    
    for n, expected in test_cases:
        result = solution(n)
        status = "PASS" if result == expected else "FAIL"
        print(f"{status} N={n}, binary={bin(n)[2:]}, expected={expected}, got={result}")

if __name__ == "__main__":
    main()