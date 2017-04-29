### Brown Clustering

Brown clustering (or IBM clustering) is a form of hierarchical clustering of words based on the contexts in which they occur, proposed by Peter Brown, Vincent Della Pietra, Peter deSouza, Jennifer Lai, and Robert Mercer of IBM in the context of language modeling. The intuition behind the method is that a class-based language model (also called cluster n-gram model), i.e. one where probabilities of words are based on the classes (clusters) of previous words, is used to address the data sparsity problem inherent in language modeling.

This is an Python implementation for creating hierarchical word clusters based on syntactic context ("Brown clusters").  This is based on the following papers.

* Peter F. Brown; Peter V. deSouza; Robert L. Mercer; T. J. Watson; Vincent J.
  Della Pietra; Jenifer C. Lai. 1992.  Class-Based n-gram Models of Natural
  Language.  Computational Linguistics, Volume 18, Number 4.
  http://acl.ldc.upenn.edu/J/J92/J92-4003.pdf
* Percy Liang. 2005.  Semi-supervised learning for natural language.  MIT.
  http://cs.stanford.edu/~pliang/papers/meng-thesis.pdf

Some additional references:
* See http://www.cs.columbia.edu/~cs4705/lectures/brown.pdf for a high-level
  overview of Brown clustering.
* Here are two other implementation of Brown clustering:
  - https://github.com/percyliang/brown-cluster
  - https://github.com/mheilman/tan-clustering/blob/master/class_lm_cluster.py

The parser.py cleans words from brown corpus, removing word with frequency < 10.

Run printBicodes.py and printClusters.py to see generated clusters.

Run cluster.py to re-run and re-generate the clusters.

To run brown clustering on other corpus, simply change directory variable in parser.py will do the trick.
