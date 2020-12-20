# BloomFilters

Comparisons and Analysis of Various Bloom Filters

## Results Highlight

![Image failed to render; see figure/ScBF-FPR-10000.png](https://github.com/Shaumik-Ashraf/BloomFilters/blob/main/figure/ScBF-FPR-10000.png?raw=true)

![Image failed to render; see figure/PPBF-runtime-10000-k10.png](https://github.com/Shaumik-Ashraf/BloomFilters/blob/main/figure/PPBF-runtime-10000-k10.png?raw=true)

## File Spec
 - bloomfilter.py -> modular implementation of various Bloom Filter classes
 - test.py -> test code to verify that Bloom Filter implementation works
 - benchmark.py -> defines Benchmark class to verify accuracy of Bloom Filter classes
 - experiment.py -> experiment script
 - figure/* -> results from experimentation
 - for_heatmap/* -> subset of results exported to CSV

## Dependencies
 - Python 3
 - bitstring library (`pip install bitstring`)
 - numpy
 - pandas
 - matplotlib

## Contributors
 - Shaumik Ashraf
 - Emily Tao

This project was completed in partial fulfillment of CS5112, Cornell Tech
