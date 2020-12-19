# test.py

import bloomfilter;

print("=========== Testing Standard Bloom Filter =========");

sbf = bloomfilter.StandardBloomFilter(10);

print("BloomFilter: %s" % str(sbf));
print("Number of hash functions: %i" % sbf.num_hashes());
assert type(sbf.num_hashes()) == int, "Test failed! Number of hashes not int."
assert sbf.num_hashes() != 0, "Test failed! No hashes found."

print("\nClearing all hash functions...");
sbf.clear_hashes();
print("Number of hash functions: %i" % sbf.num_hashes());
assert sbf.num_hashes() == 0, "Test failed! Hashes found.";

print("\nAdding hash functions sha1 and sha224...");
sbf.add_hash('sha1');
sbf.add_hash('sha224');
print("Number of hash functions: %i" % sbf.num_hashes());
assert sbf.num_hashes() == 2, "Test failed! Unexpected number of hashes found.";

s = "apple";
print("\nAdding %s to bloomfilter..." % s);
sbf.add(s);
print("BloomFilter: %s" % str(sbf));

print("\nChecking %s in BF..." % s);
e = sbf.has(s);
print("BloomFilter: %s" % str(sbf));
assert e, "Test failed! False Negative.";

s = "banana";
print("\nChecking %s in BF..." % s);
e1 = sbf.has(s);
print("BloomFilter: %s" % str(sbf));
if( e1 ):
    print('False positive!');
    
s = "tower";
print("\nChecking %s in BF..." % s);
e2 = sbf.has(s);
print("BloomFilter: %s" % str(sbf));
if( e2 ):
    print('False positive!');
assert (not e1) and (not e2), "You got 2/2 false positives, which is suspicious but not impossible."

s = "banana";
print("\nAdding %s to bloomfilter..." % s);
sbf.add(s);
print("BloomFilter: %s" % str(sbf));

print("\nChecking %s in BF..." % s);
e = sbf.has(s);
print("BloomFilter: %s" % str(sbf));
assert e, "Test failed! False Negative.";

s = "tower";
print("\nChecking %s in BF..." % s);
e = sbf.has(s);
print("BloomFilter: %s" % str(sbf));
if( e ):
    print('False positive!');

print("\nTrying remove, should raise exception for SBF");
try:
    sbf.remove(s);
    assert False, "Test Failed! Standard BF returned after removing element."
except:
    print("Exception raised successfully")
finally:
    print("Exception should have been raised.");

print("\nReseting BF");
sbf.reset();
print("BloomFilter: %s" % str(sbf));

a = "apple";
print("\nChecking %s in BF..." % s);
e = sbf.has(s);
print("BloomFilter: %s" % str(sbf));
assert not e, "Test Failed! Empty BF returned positive.";

print("\n============= Test Success! =====================");


print("=========== Testing Counting Bloom Filter =========");

cbf = bloomfilter.CountingBloomFilter(10);

print("BloomFilter: %s" % str(cbf));
print("Skipping hash methods test because these are defined in abstract class and are already tested.");

s = "apple";
print("\nAdding %s to bloomfilter..." % s);
cbf.add(s);
print("BloomFilter: %s" % str(cbf));

print("\nChecking %s in BF..." % s);
e = cbf.has(s);
print("BloomFilter: %s" % str(cbf));
assert e, "Test failed! False Negative.";

s = "banana";
print("\nChecking %s in BF..." % s);
e1 = cbf.has(s);
print("BloomFilter: %s" % str(cbf));
if( e1 ):
    print('False positive!');
    
s = "tower";
print("\nChecking %s in BF..." % s);
e2 = cbf.has(s);
print("BloomFilter: %s" % str(cbf));
if( e2 ):
    print('False positive!');
assert (not e1) and (not e2), "You got 2/2 false positives, which is suspicious but not impossible."

s = "banana";
print("\nAdding %s to bloomfilter..." % s);
cbf.add(s);
print("BloomFilter: %s" % str(cbf));

print("\nChecking %s in BF..." % s);
e = cbf.has(s);
print("BloomFilter: %s" % str(cbf));
assert e, "Test failed! False Negative.";

s = "tower";
print("\nChecking %s in BF..." % s);
e = cbf.has(s);
print("BloomFilter: %s" % str(cbf));
if( e ):
    print('False positive!');

s = 'apple';
print("\nRemoving %s..." % s);
cbf.remove(s);
print("BloomFilter: %s" % str(cbf));

print("\nChecking %s in BF..." % s);
e = cbf.has(s);
print("BloomFilter: %s" % str(cbf));
if( e ):
    print('False positive!');


print("\nReseting BF");
cbf.reset();
print("BloomFilter: %s" % str(cbf));

a = "apple";
print("\nChecking %s in BF..." % s);
e = cbf.has(s);
print("BloomFilter: %s" % str(cbf));
assert not e, "Test Failed! Empty BF returned positive.";

print("\n============= Test Success! =====================");

print("=========== Testing Parallel Partitioned Bloom Filter =========");

ppbf = bloomfilter.ParallelPartitionedBloomFilter(7);

print("BloomFilter: %s" % str(ppbf));
print("Number of hash functions: %i" % ppbf.num_hashes());
assert type(ppbf.num_hashes()) == int, "Test failed! Number of hashes not int."
assert ppbf.num_hashes() != 0, "Test failed! No hashes found."

print("\nClearing all hash functions...");
ppbf.clear_hashes();
print("Number of hash functions: %i" % ppbf.num_hashes());
assert ppbf.num_hashes() == 0, "Test failed! Hashes found.";

print("\nAdding hash functions sha1, sha224, & sha384...");
ppbf.add_hash('sha1');
ppbf.add_hash('sha224');
ppbf.add_hash('sha384');
print("Number of hash functions: %i" % ppbf.num_hashes());
assert ppbf.num_hashes() == 3, "Test failed! Unexpected number of hashes found.";

s = "apple";
print("\nAdding %s to bloomfilter..." % s);
ppbf.add(s);
print("BloomFilter: %s" % str(ppbf));

print("\nChecking %s in BF..." % s);
e = ppbf.has(s);
print("BloomFilter: %s" % str(ppbf));
assert e, "Test failed! False Negative.";

s = "banana";
print("\nChecking %s in BF..." % s);
e1 = ppbf.has(s);
print("BloomFilter: %s" % str(ppbf));
if( e1 ):
    print('False positive!');
    
s = "tower";
print("\nChecking %s in BF..." % s);
e2 = ppbf.has(s);
print("BloomFilter: %s" % str(ppbf));
if( e2 ):
    print('False positive!');
assert (not e1) and (not e2), "You got 2/2 false positives, which is suspicious but not impossible."

s = "banana";
print("\nAdding %s to bloomfilter..." % s);
ppbf.add(s);
print("BloomFilter: %s" % str(ppbf));

print("\nChecking %s in BF..." % s);
e = ppbf.has(s);
print("BloomFilter: %s" % str(ppbf));
assert e, "Test failed! False Negative.";

s = "tower";
print("\nChecking %s in BF..." % s);
e = ppbf.has(s);
print("BloomFilter: %s" % str(ppbf));
if( e ):
    print('False positive!');

print("\nTrying remove, should raise exception for PPBF");
try:
    ppbf.remove(s);
    assert False, "Test Failed! Standard BF returned after removing element."
except:
    print("Exception raised successfully");
finally:
    print("Exception should have been raised.");

print("\nReseting BF");
ppbf.reset();
print("BloomFilter: %s" % str(ppbf));

a = "apple";
print("\nChecking %s in BF..." % s);
e = ppbf.has(s);
print("BloomFilter: %s" % str(ppbf));
assert not e, "Test Failed! Empty BF returned positive.";

print("\n============= Test Success! =====================");