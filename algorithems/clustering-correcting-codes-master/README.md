# clustering-correcting-codes
the implementation of the algorithms specified in the article https://arxiv.org/pdf/1903.04122.pdf

Abstract— "A new family of codes, called clustering-correcting
codes, is presented in this paper. This family of codes is motivated
by the special structure of data that is stored in DNA-based storage systems. The data stored in these systems has the form of
unordered sequences, also called strands, and every strand is synthesized thousands to millions of times, where some of these copies
are read back during sequencing. Due to the unordered structure
of the strands, an important task in the decoding process is to
place them in their correct order. This is usually accomplished by
allocating a part of the strand for an index. However, in the presence of errors in the index field, important information on the
order of the strands may be lost.
Clustering-correcting codes ensure that if the distance between
the index fields of two strands is small, then there will be a large
distance between their data fields. It is shown how this property
enables to place the strands together in their correct clusters even
in the presence of errors. We present lower and upper bounds on
the size of clustering-correcting codes and an explicit construction
of these codes which uses only a single bit of redundancy".

____________________________________________________________________________________

# in order to use the code:

1. to compile you need to use 'g++ -std=c++14 -o main main.cpp' command.

2. you can run the generate_test script, it generates a txt file with 100 random strands of length 100 under the name "test_file_updated.txt", or you can create your own test and keep it in the project directory (it should be name test_file_updated.txt).

3. in order to run the code, you need to run it from CMD with the following command:
'./main raw tao strands_data_length Majority\Dominance true\false test_file_updated.txt'

        arg 1 - raw, an integer denoting raw parameter (further explanation below and in the article).

        arg 2 - tao, an integer denoting raw parameter (further explanation below and in the article).

        arg 3 - strands data length, an integer denoting the data length of the strands.

        arg 4 - assumption (majority/dominance) - a string, should be 'M' for majority or 'D' for dominance, other then that would be an        error.

        arg 5 - boolean denoting wether we're using brute force manner in the encoding algorithim (further explanation regarding this is        in the paper).

        arg 6 - the test input file (should be located within the project, and the name should be test_file_updated.txt).

4. the algorithims's output files will be located in the project directory (below is the explanation regarding the output files).
____________________________________________________________________________________

# further explanation regarding the system arguments:

raw & tao - a system parameters which are used to make assumptions about output strands (the strands that we pull out from the DNA compound). from the article: "Each output strand in the set G is a copy of one of the input strands in S, however with some potential errors. A DNA-based storage system is called a (tao,raw)-DNA system if it satisfies the following property: If the output strand (ind',u') ∈ G is a noisy copy of the input strand (ind,u) ∈ S, then dH(ind, ind') <= tao and
dH(u,u') <= raw. That is, the index field has at most tao Hamming errors while the data field has at most raw Hamming errors."

assumptions (majority/dominance) - from the article: "Another assumption taken in this model, will be referred to 
as the majority assumption. Let the cluster C(i) be the group of all strands read with index ind(i) (with potential errors in the index). The majority assumption assume that in every cluster the majority of the strands have the correct index, i.e., they have no error in the index. since the number of strands is very large this assumption holds with high probability if not in all cases. Alternatively, we will use a weaker assumption, which will be referred as the dominance assumption. assume we assign a color to each strand in C(i) base on the index this strand originated from, so strands originated with the same index receive the same color. the dominance assumption assume that the dominante color in the cluster identifies the strands that their index is correct, which is ind(i). That is, if a cluster could be partitioned into subset based on the correct origin of each strand (their true index), the largest subset in the cluster contains the strands with the correct index field and therefore, are clustered correctly."

____________________________________________________________________________________


# output files:

1. results_before_encoding.txt - the strands before the encoding algorithim (sorted by the index of the strand).

2. results_after_encoding.txt - the strands after the encoding algorithim (sorted by the index of the strand).

3. results_after_decoding.txt - the strands after the activating decoding algorithim straight after encoding (without error simulation, clustering, and error correction).

4. status_after_errors_simulations.txt - after encoding algorithim, we perform error simulations on the strands (duplicate each strands, insert diffrent error to each copy).

5. status_after_fix_errors.txt - the clusters situation after we've performed the idetification algorithim and the error correction algorithm.

6. status_to_fix_errors_output.txt - the majority vector from each cluster. (we go through all the vectors in a cluster, bit by bit, and we create a majority vector whom its bits are the most common bits from all the vecotrs in the cluster) e.g :

cluster 1 1000, 1011, 1000

cluster 2 1111, 1001, 1100

majority vector for cluster 1 : 1000
majority vector for cluster 2 : 1101  

** under certain circumstances we aspire that status_to_fix_errors_output.txt would be equal to results_after_decoding.txt, though its
not certain for it to happen and it depends on the data the program recives.
     
        


