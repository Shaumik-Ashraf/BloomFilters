#bloomfilter.py

from abc import ABC, abstractmethod;      #abstract base class
import hashlib;                  
from bitstring import BitArray;  #requires pip install bitstring
import numpy;

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
    
    #remove string from bloom filter; not possible for all types of bloom filters
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
    def __init__(self, size, array, hash_names = ['md5', 'sha1', 'sha224', 'sha256', 'sha384']):
        self.size = size;
        self.array = array;
        self.hash_names = hash_names;
        self.load = None;
        for s in self.hash_names:
            if( s not in hashlib.algorithms_available ):
                raise Exception("Hash " + s + " not found");
    
    #returns: string representing bloom filter; allows you to do: print( my_bloom_filter );
    def __str__(self):
        if isinstance(self, BitArray):
            return self.array.bin;
        else:
            return str( self.array );
    
    #param k: int corresponding to hash function; k=0 is first hash in hash_names
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
    
    #iterates along each bucket returned by each hash in bloom filter
    #param string: python string, must be convertable to 8 bit encoding
    def each_hashed_bucket_of(self, string):
        """
        #i.e. adding 1 to each bucket for "hello"
        for index in self.each_hashed_bucket_of("hello"):
            self.array[index] = self.array[index] + 1;
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
        super(StandardBloomFilter, self).__init__(size, BitArray(length=size));
    
    def add(self, string):
        # print(f'adding {string}')
        for i in self.each_hashed_bucket_of(string):
            #print(i);
            self.array.set('1', i);
        return;
    
    def has(self, string):
        ret = True;
        tmp = self.array.bin;
        for i in self.each_hashed_bucket_of(string):
            ret = (ret and (tmp[i] == '1'));
            if not ret:
                break;
        return ret;
    
    def remove(self, string):
        raise Exception("Remove cannot be performed by Standard Bloom Filter");

    def reset(self):
        self.array.set(0);



class CountingBloomFilter(AbstractBloomFilter):

    def __init__(self, size):
        super(CountingBloomFilter, self).__init__(size, numpy.zeros(size, dtype='int8'));
    
    def add(self, string):
        for i in self.each_hashed_bucket_of(string):
            self.array[i] += 1;
        return;
    
    def has(self, string):
        ret = True;
        for i in self.each_hashed_bucket_of(string):
            ret = (ret and (self.array[i] > 0));
            if not ret:
                break;
        return ret;
 
    def remove(self, string):
        for i in self.each_hashed_bucket_of(string):
            self.array[i] -= 1;
        return;

    def reset(self):
        self.array[:] = 0;

class ScalingBloomFilter(AbstractBloomFilter):
    # https://gsd.di.uminho.pt/members/cbm/ps/dbloom.pdf
    
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
