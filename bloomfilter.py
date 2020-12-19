#bloomfilter.py

from abc import ABC, abstractmethod;      #abstract base class
import hashlib;                  
from bitstring import BitArray;  #requires pip install bitstring
import numpy;
import threading;
import time;

class AbstractBloomFilter(ABC):
    "Abstract Bloom Filter Class" #documentation

    ## instance variables
    #array;       #BitArray or anything else for implementation
    #size;        #non-negative int
    #hash_names;  #list of strings

    ## abstract methods
    #add param to bloom filter
    @abstractmethod
    def add(string):
        pass
    
    #returns: True or False
    @abstractmethod
    def has(string):
        pass
    
    #remove string from bloom filter; only for counting bloom filters
    @abstractmethod
    def remove(string):
        pass

    #reset bloom filter
    @abstractmethod
    def reset(s):
        pass

    ## methods
    #param size: size of array
    #param array: initial array, either BitArray of 0s or List of 0s
    #param hash_names: list of strings for hashlib.new(), hash function must be supported
    def __init__(self, hash_names = ['md5', 'sha1', 'sha224', 'sha256', 'sha384']):
        self.hash_names = hash_names;
        self.load = None;
        for s in self.hash_names:
            if( s not in hashlib.algorithms_available ):
                raise Exception("Hash " + s + " not found");
    
    #param k: int corresponding index of hash function; k=0 is first hash in hash_names
    #param string: python string, must be convertable to 8 bit encoding
    #returns: non-negative int within bloomfilter size
    def hash(self, k, string):
        bytestring = string.encode();
        h = hashlib.new(self.hash_names[k]);
        h.update(bytestring);
        if( self.hash_names[k][:5] == 'shake' ):
            digest = h.hexdigest(16);
        else:
            digest = h.hexdigest();
        #print("Hash %s on %s gets %i" % (self.hash_names[k], string, int(digest, 16) % self.size))
        return( int(digest, 16) % self.size );
    
    #iterates along each int (bucket) returned by each hash in bloom filter
    #param string: python string, must be convertable to 8 bit encoding
    def each_hash_of(self, string):
        """
        #example:
        for index_from_hash in self.each_hash_of("hello"):
            bitarray[index_from_hash] = 1;
        """
        if( len(self.hash_names)==0 ):
            raise Exception("No hashes in bloom filter");
        
        for k in range(len(self.hash_names)):
            yield self.hash(k, string);
    
    #adds hash to set of hash functions done by bloom filter; resets bloom filter!
    #param hash_name: (str) name of hash in hashlib
    def add_hash(self, hash_name):
        self.hash_names.append(hash_name);
        self.reset();
    
    #clears all hash functions in bloom filter; resets bloom filter!
    def clear_hashes(self):
        self.hash_names.clear();
        self.reset();
    
    #returns k (number of hash functions in bloom filter)
    def num_hashes(self):
        return len(self.hash_names);
    
    """
    #returns m (length of underlying array; returns -1 if variable)
    def size(self):
        return self.size;
    """
    
class StandardBloomFilter(AbstractBloomFilter):

    def __init__(self, size):
        super(StandardBloomFilter, self).__init__()
        self.size = size
        self.array = BitArray(length=size)
        self.fill_ratio = 0.
    
    #returns: string representing bloom filter; allows you to do: print( my_bloom_filter );
    def __str__(self):
        return self.array.bin
    
    def add(self, string):
        # print(f'adding {string}')
        for i in self.each_hash_of(string):
            #print(i);
            self.array.set('1', i)
        self.fill_ratio = self.array.count(True) / self.size
        return
    
    def has(self, string):
        ret = True;
        tmp = self.array.bin;
        for i in self.each_hash_of(string):
            ret = (ret and (tmp[i] == '1'));
            if not ret:
                break;
        return ret;
    
    def remove(self, string):
        raise Exception("No remove operation in Standard Bloom Filter");

    def reset(self):
        self.array.set(0)
        self.fill_ratio = 0.


class CountingBloomFilter(AbstractBloomFilter):

    def __init__(self, size):
        super(CountingBloomFilter, self).__init__()
        self.size = size
        self.array = numpy.zeros(size, dtype='int8')
    
    #returns: string representing bloom filter; allows you to do: print( my_bloom_filter );
    def __str__(self):
        return str(self.array)
    
    def add(self, string):
        for i in self.each_hash_of(string):
            self.array[i] += 1;
        return;
    
    def has(self, string):
        ret = True;
        for i in self.each_hash_of(string):
            ret = (ret and (self.array[i] > 0));
            if not ret:
                break;
        return ret;
 
    def remove(self, string):
        for i in self.each_hash_of(string):
            self.array[i] -= 1;
        return;

    def reset(self):
        self.array[:] = 0;


class ParallelPartitionedBloomFilter(AbstractBloomFilter):
    #Like Standard Bloom Filter, but multiple bitarrays
    #are stored, one for each hash function. This allows
    #for multi-threaded inquiries.
    
    def __init__(self, size):
        super(ParallelPartitionedBloomFilter, self).__init__()
        self.size = size
        self.array = list()
        self.flag = True; #shared memory; threads set to false if str not found
        self.flag_lock = threading.Lock();
        self.threads = list();

        for i, s in enumerate(self.hash_names):
            self.array.append(BitArray(length=size));
            #self.array is a list of bitarrays, one bitarray per hash function

    def reset_flag(self):
        while( self.flag_lock.locked() ):
            time.sleep(0.05);
        self.flag_lock.acquire();
        self.flag = True;
        self.flag_lock.release();
    
    def set_flag_false(self):
        while( self.flag_lock.locked() ):
            time.sleep(0.05);
        self.flag_lock.acquire();
        self.flag = False;
        self.flag_lock.release();
    
    #read only shouldn't have to be locked/mutex'd...
    #but I will lock it anyways
    def get_flag(self):
        while( self.flag_lock.locked() ):
            time.sleep(0.05);
            
        self.flag_lock.acquire();
        ret = self.flag;
        self.flag_lock.release();
        
        return(ret);

    def threaded_add(self, i, string):
        print("threaded add called!");
        self.array[i].set('1', self.hash(i,string));
        #for j = hash_i(string), use the bitarray at array[i], and set bitarray[j],
    
    def threaded_has(self, i, string):
        ki = self.hash(i, string);
        if( self.array[i][ki] == '0' ): #bit not set, set flag to false
            self.set_flag_false();
        #else bit set, flag is true by default
        
    def add(self, string):
        print("1");
        for i in range(self.num_hashes()):
            print("2 - %i" % i);
            th = threading.Thread(target=self.threaded_add, args=(self, i, string));
            th.start();
            self.threads.append(th);
        
        print("3");
        
        for th in self.threads:
            print("4 - %s" % str(th));
            th.join();
        
        print("5");
        
        self.threads.clear();
        print("6");
        
    def has(self, string):
        print("7");
        self.reset_flag();
        print("8");
        for i, h in enumerate(self.hash_names):
            th = threading.Thread(target=self.threaded_has, args=(self, i, string));
            th.start();
            self.threads.append(th);
            print("9 - %i" % i);
            
        print("10");
        for th in self.threads:
            print("11 - ", str(th));
            th.join();
            
        print("12");
        self.threads.clear();
        print("13");
        return( self.get_flag() );
        
    def remove(self, string):
        raise Exception("Remove cannot be performed by Parallel Partitioned Bloom Filter");
    
    def reset(self):
        for bitarr in self.array:
            bitarr.set(0);

    #override
    def add_hash(self, hash_name):
        self.hash_names.append(hash_name);
        self.array.append(BitArray(length=self.size));
        self.reset();
    
    #override
    def clear_hashes(self):
        self.hash_names.clear();
        self.array.clear();


class ScalableBloomFilter(AbstractBloomFilter):
    # https://gsd.di.uminho.pt/members/cbm/ps/dbloom.pdf
    
    def __init__(self, initial_size, s=2):
        AbstractBloomFilter.__init__(self)
        self.bf = [StandardBloomFilter(initial_size)]
        self.num_bf = 1
        self.cur_bf = 0
        self.size = initial_size
        # self.error_prob = error_prob # P
        self.p = 0.5 # fill ratio
        self.s = s # filter size growth. sqrt(2), 2, 4
    
    def __str__(self):
        output = ''
        for bf in self.bf:
            output += '\n' + str(bf)
        return output
    
    def add(self, string):
        self.bf[self.cur_bf].add(string)
        if self.bf[self.cur_bf].fill_ratio >= self.p:
            size = self.bf[self.cur_bf].size * self.s
            self.size += size
            self.bf.append(StandardBloomFilter(size))
            self.num_bf += 1
            self.cur_bf += 1
        
    def has(self, string):
        for i in range(self.num_bf):
            if self.bf[i].has(string):
                return True
        return False
        
    def remove(self, string):
        raise Exception('No remove operation in Scalable Bloom Filter')
    
    def reset(self):
        for i in range(1, self.num_bf):
            del self.bf[-1]
        self.bf[0].reset()
        self.num_bf = 1
        self.cur_bf = 0


class SpectralBloomFilter(AbstractBloomFilter):
    # https://whiteblock.io/wp-content/uploads/2019/10/sbf-sigmod-03.pdf
    
    def __init__(self, error_rate):
        pass;
    
    def add(self, string):
        pass;
        
    def has(self, string):
        pass;
        
    def remove(self, string):
        pass;
    
    def reset(self):
        pass;
