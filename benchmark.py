import random
import time
import bloomfilter

data = []
with open('data.txt', 'r') as f:
    for url in f:
        data.append(url.strip())
L = len(data)

k = 100 # # of selected urls
# random
random_num = set()
while len(random_num) < k:
    random_num.add(random.randint(0, L - 1))
random_data = []
for i in random_num:
    random_data.append(data[i])
# first k
#subdata = data[:k]

class Benchmark():
    def __init__(self):
        self.myset = []
    
    def add(self, s):
        self.myset.append(s)
        # print(f'adding {s}')

    def check(self, s):
        if s not in self.myset:
            self.add(s)
            return False
        else:
            return True

b = Benchmark()
Nbits = 100000
sbf = bloomfilter.StandardBloomFilter(Nbits)
cnt_correct = 0
total_time = 0.
for url in random_data:
    ben = b.check(url)
    t_start = time.time()
    bf = sbf.has(url)
    t_end = time.time()
    total_time += t_end - t_start
    if ben == bf:
        cnt_correct += 1

print("Standard Bloom Filter results:");
print(f'# dataset = {k}, {Nbits} bits, average time {1000 * total_time / k}ms, accuracy {cnt_correct / k}')

b = Benchmark()
Nbits = 100000
cbf = bloomfilter.CountingBloomFilter(Nbits)
cnt_correct = 0
total_time = 0.
for url in random_data:
    ben = b.check(url)
    t_start = time.time()
    bf = cbf.has(url)
    t_end = time.time()
    total_time += t_end - t_start
    if ben == bf:
        cnt_correct += 1

print("\nCounting Bloom Filter results:");
print(f'# dataset = {k}, {Nbits} bits, average time {1000 * total_time / k}ms, accuracy {cnt_correct / k}')
