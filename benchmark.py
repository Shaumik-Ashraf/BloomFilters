import random
import time
import bloomfilter

#param n is size of dataset
#returns random_data - randomized linked list of strings 
def load_data(n=1000):
    data = []
    with open('data.txt', 'r') as f:
        for url in f:
            data.append(url.strip())
    L = len(data)
    
    k = n # # of selected urls
    # random
    random_num = set()
    while len(random_num) < k:
        random_num.add(random.randint(0, L - 1))
    random_data = []
    for i in random_num:
        random_data.append(data[i])

    return(random_data);

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

""" # Old Code
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
"""

#param data - dataset of urls
#param abf - instance of abstract bloom filter
#returns false_positive_rate, average_time
def trial(data, abf, verbose = False):
    b = Benchmark()
    cnt_correct = 0
    total_time = 0.
    for url in data:
        ben = b.check(url)
        t_start = time.time()
        bf = abf.has(url)
        t_end = time.time()
        total_time += t_end - t_start
        if ben == bf:
            cnt_correct += 1
    
    n = len(data);
    k = abf.num_hashes();
    m = abf.size;
    false_positive_rate = 1.0 - cnt_correct / len(data);
    average_time = 1000 * total_time / len(data); #ms
    
    if( verbose ):
        print("Trial results: (%i datapoints, %i hash functions, %i array size)" % (n, k, m));
        print(f'false positive rate: {false_positive_rate}, average time: {average_time}ms\n');
    
    return( false_positive_rate, average_time );



# test run - success!
#data = load_data();
#x, y = trial(data, bloomfilter.StandardBloomFilter(1000))