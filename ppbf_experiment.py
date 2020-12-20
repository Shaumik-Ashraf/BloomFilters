# ppbf_experiment.py
# test ppbf only with smaller k values
# otherwise this file is a copy-pase of experiment.py

import bloomfilter;
import benchmark;
import hashlib;
import random;
import numpy;
import pandas;
import matplotlib.pyplot as plt;

m_values = [1, 10, 100, 1000, 10000, 20000, 30000];
k_values = [3, 4, 5, 6, 7, 8, 9, 10,] #11, 12, 13, 14];
dataset_size = 10000;

hash_store = list(hashlib.algorithms_available);
""" hash_store on my computer:
['sha512_256',
 'md5',
 'blake2s',
 'sha3_256',
 'md5-sha1',
 'sm3',
 'shake_256',
 'sha224',
 'sha512',
 'ripemd160',
 'shake_128',
 'sha1',
 'blake2b',
 'mdc2',
 'md4',
 'sha3_224',
 'whirlpool',
 'sha256',
 'sha3_512',
 'sha512_224',
 'sha384',
 'sha3_384']
"""

#returns k random hash names from hash_store
def get_random_hashes(k):
    ret = [];
    
    if( k > len(hash_store) ):
        raise Exception("%i hashes are not available" % k);
    elif( k == len(hash_store) ):
        return hash_store;
    else:
        i = 0;
        while( i < k ):
            s = hash_store[random.randint(0, len(hash_store)-1)];
            if( s not in ret ):
                ret.append(s);
                i += 1;
        
        return(ret);

#runs t trials and averages the false positive rates and runtimes
#param t - int, number of trials to run
#param data - dataset of urls
#param bf - instance of bloom filter
#returns average_false_positive_rate, average_time
def t_trials(t, data, bf):
    fprs = numpy.zeros(t);
    timings = numpy.zeros(t);
    
    for i in range(t):
        bf.reset();
        fpr, timing = benchmark.trial(data, bf);
        fprs[i] = fpr;
        timings[i] = timing;
    
    return(numpy.average(fprs), numpy.average(timings));

def run(bloomfilter_name = 'Standard Bloom Filter'):
    data = benchmark.load_data(dataset_size);
    
    fpr_results = numpy.zeros((len(m_values), len(k_values)));
    time_results = numpy.zeros((len(m_values), len(k_values)));
                                    
    for i in range(len(m_values)):
        for j in range(len(k_values)):
            m = m_values[i];
            k = k_values[j];
            
            print("m=%i, k=%i" % (m, k));
            
            #construct bloom filter
            if( bloomfilter_name == 'Standard Bloom Filter' ):
                bf = bloomfilter.StandardBloomFilter(m);
            elif( bloomfilter_name == 'Counting Bloom Filter' ):
                bf = bloomfilter.CountingBloomFilter(m);
            elif bloomfilter_name == 'Scalable Bloom Filter':
                bf = bloomfilter.ScalableBloomFilter(m)
            elif bloomfilter_name == 'Parallel Partitioned Bloom Filter':
                bf = bloomfilter.ParallelPartitionedBloomFilter(m);
            else:
                raise Exception("%s not implemented" % bloomfilter_name);
            
            hash_names = get_random_hashes(k);
            bf.clear_hashes(); #clear default hashes
            for hash_name in hash_names:
                bf.add_hash(hash_name);
            
            #run trials
            avg_fpr, avg_time = t_trials(3, data, bf);
            fpr_results[i][j] = avg_fpr;
            time_results[i][j] = avg_time;
    
    print(fpr_results);
    print(time_results);
    
    fpr_df = pandas.DataFrame(data = fpr_results, index = m_values, columns = k_values);
    time_df = pandas.DataFrame(data = time_results, index = m_values, columns = k_values);
    
    fpr_df.to_csv("for_heatmap/%s-fpr_results-%i.csv" % (bloomfilter_name, dataset_size));
    time_df.to_csv("for_heatmap/%s-time_results-%i.csv" % (bloomfilter_name, dataset_size));
    
    plt.figure();
    plt.xlabel('k (number of hash functions)');
    plt.ylabel('m (bloom filter size)');
    plt.title("%s Run Times" % bloomfilter_name); 
    plt.xticks(range(len(k_values)), k_values);
    plt.yticks(range(len(m_values)), m_values);
    hm = plt.imshow(time_results, cmap="Blues", interpolation="nearest");
    plt.colorbar(hm);
    
    plt.figure();
    plt.xlabel('k (number of hash functions)');
    plt.ylabel('m (bloom filter size)');
    plt.title("%s False Positive Rates" % bloomfilter_name);
    plt.xticks(range(len(k_values)), k_values);
    plt.yticks(range(len(m_values)), m_values);
    hm = plt.imshow(fpr_results, cmap="Blues", interpolation="nearest");
    plt.colorbar(hm);


run("Parallel Partitioned Bloom Filter");