# generated from input
def run(a):
    out = []
    while True:
        b = a%8
        b ^= 1
        c = a // 2 ** b
        b ^= 4
        a //= 2**3
        b = b ^ c
        out.append(b % 8)
        if a == 0:
            break
    return ",".join(map(str, out))

def gen(nums: list[int], i: int = 0, curr_a = 0) -> int:
    if i >= len(nums):
        return curr_a
    expected_suffix = ",".join(map(str, nums[-(i+1):]))
    n_unknown_bits = 3*(len(nums)-i-1)

    ans = 10**1000
    for x in range(8):
        new_a = curr_a * 8 + x
        s = run(new_a << n_unknown_bits)
        if s.endswith(expected_suffix):
            ans = min(ans, gen(nums, i+1, new_a))
    return ans

print(gen([2,4,1,1,7,5,1,4,0,3,4,5,5,5,3,0]))