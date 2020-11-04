# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 16:16:58 2020

@author: ShaumikAshraf
"""

import bloomfilter;

print("======= Testing Standard Bloom Filter =========");
#added = [];
sbf = bloomfilter.StandardBloomFilter(10);

print("BloomFilter: %s" % str(sbf));

s = "apple";
#added.append(s);
sbf.add(s);
print("BloomFilter: %s" % str(sbf));

print("\nChecking %s in BF..." % s);
print( sbf.has(s) );
print("BloomFilter: %s" % str(sbf));

s = "banana";
print("\nChecking %s in BF..." % s);
print( sbf.has(s) );
print("BloomFilter: %s" % str(sbf));

s = "tower";
print("\nChecking %s in BF..." % s);
print( sbf.has(s) );
print("BloomFilter: %s" % str(sbf));

s = "banana";
sbf.add(s);
print("BloomFilter: %s" % str(sbf));

s = "tower";
print("\nChecking %s in BF..." % s);
print( sbf.has(s) );
print("BloomFilter: %s" % str(sbf));

print("\nTrying remove, should raise exception for SBF");
try:
    sbf.remove(s);
except:
    print("Exception raised successfully")
finally:
    print("Exception should have been raised.");

print("\nReseting BF");
sbf.reset();
print("BloomFilter: %s" % str(sbf));

a = "apple";
print("\nChecking %s in BF..." % s);
print( sbf.has(s) );
print("BloomFilter: %s" % str(sbf));

print("\n===================== Done =====================");

