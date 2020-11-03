#bloom_filter.py

import abc; #abstract base class
import hashlib;
from bitstring import BitArray;  #requires pip install bitstring

class AbstractBloomFilter(metaclass=abc.ABCMeta):
	"Abstract Bloom Filter Class" #documentation

	## instance variables
	array;  	#either BitArray or Linked List
	size;		#non-negative int
	hash_names; #list of strings

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
	def __init__(self, size, array, hash_names = ['sha1', 'sha224', 'sha256']);
		self.size = size;
		self.array = array;
		self.hash_names = hash_names;
		self.load = None;
		for s in hash_names():
			if( s not in hashlib.algorithms_available() ):
				raise Exception("Hash " + s + " not found");
	
	#returns: string representing bloom filter; allows you to do: print( my_bloom_filter );
	def __str__(self):
		if isinstance(self, BitArray):
			return array.bin;
		else:
			return str( array );
	
	#param k: int corresponding to hash function; k=0 is first hash in hash_names
	#param string: python string, must be convertable to 8 bit encoding
	#returns: non-negative int within bloomfilter size
	def hash(k, string):
		bytestring = string.encode();
		hash = hashlib.new(hash_names[k]);
		digest = hash.update(bytestring);
		return( int(digest) % self.size );
	
	#iterates along each bucket returned by each hash in bloom filter
	#param string: python string, must be convertable to 8 bit encoding
	def each_hashed_bucket_of(string):
		"""
		#i.e. adding 1 to each bucket for "hello"
		for index in each_hashed_bucket_of("hello"):
			array[index] = array[index] + 1;
		"""
		for k in range(len(hash_names)):
			yield hash(k, string);
		

class StandardBloomFilter(AbstractBloomFilter):

	def __init__(self, size):
		super(StandardBloomFilter, self).__init__(size, BitArray(length=size));
	
	def add(string):
		for i in each_hashed_bucket_of(string):
			array.set('1', i);
		return;
	
	def has(string):
		ret = True;
		tmp = array.bin;
		for i in each_hashed_bucket_of(string):
			ret = (ret and (tmp[i] == '1'));
		return(ret);
	
	def remove(string):
		raise Exception("Remove cannot be performed by Standard Bloom Filter");

	def reset():
		array.clear();
	