<h1 align="center">Repeat-free Codes - Final Project</h1>

# Project Goals

The goal of this tool is to eliminate identical windows in a given sequence. The input is a length-*(n - 1)* *q*-ary vector
and the output is a length-*n* *q*-ary vector which has no identical windows of size *2 &bull; log_q(n) + 2*.
<!--<img src="https://render.githubusercontent.com/render/math?math={2\log_qn%2B1}">-->

Repeat-free vectors are also called *weak de-Bruijn sequences*.

The encoding algorithm is based on **Algorithm 1** from the article "[Repeat-Free Codes](/article.pdf)" by E. Yaakobi, O. Elishco, R. Gabrys and M. Medard.

This project was done as a final project as part of the course **Coding and Algorithms and Memories** as taught by Prof. E. Yaakobi at the Technion, Winter 2019-2020.

## Table of Contents

* [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
* [Usage](#usage)
    * [Positional Parameters](#positional-parameters)
    * [Optional Flags](#optional-flags)
    * [Examples](#examples)
    * [Running Tests](#running-tests)
* [Encoder](#encoder)
    * [Parameters](#parameters)
    * [Algorithm](#algorithm)
    * [Complexity](#complexity)
* [Decoder](#decoder)
    * [Parameters](#parameters-1)
    * [Algorithm](#algorithm-1)
    * [Complexity](#complexity-1)
* [Better time complexity?](#better-time-complexity)
* [Profiler](#profiler)
* [Authors](#authors)
* [Mentor](#mentor)
* [License](#license)
* [Appendix](#appendix)

## Getting Started

The project was developed in Python.

### Prerequisites

* Python 3.6 or higher

## Usage

The tool can be operated using the command line as follows:
```
usage: ./main [-h] [-i] [-r {1,2}] [-q Q] [-c {time,space}] [-v] [-t] action [sequence]
```

### Positional Parameters

*action* and *sequence* are required parameters, where *action* is either "encode" or "decode" and *sequence* is a *q*-ary word.

```
./main encode 101010
./main decode 0,1,0,1
```

### Optional Flags

There are some optional flags which can affect how the tool works
* **-h** - show help message.
* **-i** - when flag is on input will be supplied via the standard input.
* **-r** - choose the number of redundancy bits (can be 1 or 2). default is 1 redundancy bit.
* **-c** - toggle between 2 implementations options. "time" is for better time complexity (but consumes more space) and "space" is for a better space complexity (but less efficient in time).
* **-v** - when flag is on output verbosity increased and a detailed log is printed.
* **-t** - test mode, make sure that encoded word has no identical windows\ decoded word encoding is equeal to the input word.
* **-q** - determine the size of the alphabet. default is 2 (binary). notice that when q > 2 sequence charecters should be delimited by ','.

### Examples

```
./main.py encode 000000000000000001111111111000000000
output:          1011000100000110010001111111111010000
```
```
./main.py decode 1011000100000110010001111111111010000
output:          000000000000000001111111111000000000
```
```
./main.py decode 1011000100000110010001111111111010000 -v
n      = 37
q      = 2
log_n  = 6
k      = 14
w      = [1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0]
w-0    = [1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
w-2    = [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
w-2    = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
w-2    = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
w-1    = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
dec*   = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
output = 000000000000000001111111111000000000
```
```
./main.py decode 1010 -v
n      = 4
q      = 2
log_n  = 2
k      = 6
w      = [1, 0, 1, 0]
w-0    = [1, 0, 1, 0, 0, 0, 0]
w-2    = [0, 0, 0, 0, 0, 0, 0, 0]
dec*   = [0, 0, 0]
output = 000
```
```
./main.py encode 000 -t
0001
TEST SUCCESS
```
```
./main.py encode 0,1,2,3 -q5
0,1,2,3,1
```

```
./main.py encode 0,1,2,3 -q5 -c time -r2
0,0,1,2,3,1
```

### Running Tests
Random test generation is supplied at [test.py](test.py) and requires the Python `numpy` package.

## Encoder
*File: [encoder.py](encoder.py)*

### Parameters
The encoder accepts four parameters.

1. **alg_type** (either *"time"* or *"space"*): Whether to save time or space.

2. **redundancy** (either *1* or *2*): Whether to use one or two redundancy bits.

3. **verbose_mode** (bool): If set, the resulting word of every step is printed to the standard output.

4. **q** (int): Alphabet size. Alphabet is assumed to be *{0, 1, ..., q - 1}*. Default is 2.

### Algorithm
The algorithm includes two degrees of freedom determined by the *redundancy* and the *alg_type*.

The following description of the algorithm assumes **redundancy = 1**. The other case is described afterward. 

**Input:** *w* of length *n - redundancy*.

**Output:** *E(w)* of length *n*, *k*-repeat-free and *(0, zero_rll)*-run-length-limited, where *zero_rll = log_q(n) + 2*. Note that the latter property is not part of the requirements for the encoder, but is needed to allow decoding.

1. Append *1 &bull; 0^zero_rll* to the end of *w*. Call this appended series of characters the **marker**.

2. **Elimination:** Iteratively handle identical windows and long runs of zeros, until the condition of the output is achieved. The behavior of the algorithm is described in the [article](article.pdf), and so we will not go into further details.

3. **Expansion:** As long as the word length is less than *n*, append to *w* new chunks, each of length log_q(n), such that the output condition remains satisfied.

The first *n* characters of the resulting word are then returned as the codeword *c = E(w)*.

**Notes:**

* While working on the algorithm, another approach emerged which uses two redundancy bits. The only change is this: Prepend a zero to the beginning of *w* and set *zero_rll = log_q(n) + 1*, then run the algorithm identically on the resulting word. Upon decoding, the redundant zero at the beginning is dropped once the main decoder algorithm is done, and *w* is retrieved.

* See the [article](article.pdf) for the algorithm correctness proof and analysis.

### Complexity

Upon each identical window detection, a *k*-long window is deleted from the word and *(k - 1)* new characters are prepended. Therefore, there are *O(k) = O(log_q(n))* newly added windows. Since after each iteration the word length decreases by *1*, there are *O(n)* possible iterations with *O(log_q(n))* possible new windows each time. All in all, there are *O(n &bull; log_q(n))* possibly distinct handled windows throughout the algorithm.

Upon the addition of the new windows, we have to either compare only them to all other windows by hashing the already visited windows in the current iteration (taking *O(log_q(n))* time and *O(n &bull; log_q(n))* space) when *(alg_type == "space")*, or compare again all pairs of windows (taking *O(n)* time and *O(log_q(n))* space) when *(alg_type == "space")*.
**Empirically, the former implementation way outperforms the latter, both in time and space consumption.**

Since each window is possibly compared with all others, there are O(n) comparisons, each taking O(log_q(n)) time and space complexity.

Time complexity can be summarized in the following: 

* *(n &bull; log_q(n))* **iterations**
* *n* OR *log_q(n)* **new windows** need to be compared per iteration
* *n* **comparisons** for each window
* *log_q(n)* **operations** for each comparison

**Total:** *n^3 &bull; log^2_q(n)* (saving space) OR *n^2 &bull; log^3_q(n)* (saving time).


## Decoder
*File: [decoder.py](decoder.py)*

### Parameters
The decoder accepts three parameters.

1. **redundancy** (either *1* or *2*): Whether the encoder used one or two redundancy bits.

2. **verbose_mode** (bool): If set, the resulting word of every step is printed to the standard output.

3. **q** (int): Alphabet size. Alphabet is assumed to be *{0, 1, ..., q - 1}*. Default is 2.


### Algorithm

**Input:** *w* of length *n*, output of the supplied encoder.

**Output:** *D(w)* of length *(n - 1)*.

* (1) Search for a *zero_rll*-long run of zeros - the aforementioned **marker**.
    * (1.1) If found: *w = w' &bull; 1 &bull; 0^(log_n + 1) &bull; w''*.
    * (1.2) Otherwise: *w = w' &bull; 1 &bull; 0^t, where (0 <= t <= log_n)*.
    * (**Note**: Recall that *(1 &bull; 0^zero_rll* was appended. These zeros are never victims of phase 2.)
* (2) Update: *w <- w' * 1 * 0^(log_n + 1)*
* (3) Do until *len(w) == (n + log_n + 1)*:
    * (3.1) If *w[0] == 0*, **undo case 1** on *w*.
    * (3.2) Otherwise, **undo case 2** on *w*.
* (4) Return *w[:(n - 1)]*.

### Complexity
* (1) One way would be to convert the input into a dictionary, so that random-access is *O(log_q(n))*.
    * **Time complexity:** O(iterations * update time per iter) = O((n * log_q(n)) * (log_q(n) * log_q(n))) = O(n * log^3_q(n))
    * **Space complexity:** O(n)
* (2) Another way, maintaining *O(log_q(n)) space complexity, is to insert with *O(n)* time complexity.
    * **Time complexity:** O(iterations * update time per iter) = O((n * log_q(n)) * (n * log_q(n))) = O(n^2 * log^2_q(n))
    * **Space complexity:** O(log_n)

Our decoder implements option 2.

## Better time complexity?
The lower-bound for time complexity is *O(n &bull; log^2_q(n))*: we must go over *O(n &bull; log_q(n))* distinct windows and compare each one at least once in *O(loq_q(n))*.

Is it achievable? We think so. However, considering the amount of data structures we tried to put together and the substantial time we put into stubbornly trying to achieve it, we are led to believe that such a complicated structure would have little practical advantages. Our endeavors still exist in the [rip](rip/) directory, waiting for those bold enough to wander there.

## Profiler

See [README.md](profiler/README.md) under profiler.

## Authors

* [**Antonio Abu Nassar**](https://github.com/antonioan)
* [**Rotem Samuel**](https://github.com/rotemsamuel)

## Mentor
We were very fortunate to have Prof. Yaakobi as our mentor, and are grateful for the thoughts and guidance he's given us during the project.

* [Professor **Eitan Yaakobi**](http://www.cs.technion.ac.il/people/yaakobi/)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Appendix
### Deleted Windows
Say *i* is the index of the **deleted** window in some iteration, and *A = [a, a + k - 1]* is a *k*-long window in *w* **before** the deletion. Then *A* is deleted if one of these cases holds:

1. *a <= i <= a + k - 1*, which is equivalent to *i - k + 1 <= a <= i*
2. *a <= i + k - 1 <= a + k - 1*, which is equivalent to *i <= a <= i + k - 1*

**i.e.** *max(0, i - k + 1) <= a <= min(i + k - 1, n - k)*

**Number of deleted windows:** *1 + min(i + k - 1, n - k) - max(0, i - k + 1) <= 2k - 1*

### Added Windows
Say *i* is the index of the **deleted** window in some iteration, and *A = [a, a + k - 1]* is a *k*-long window in *w* **after** both the deletion and insertion. Then *A* is a new window if one of these cases holds:

1. *0 <= a <= k - 2*
2. *i <= a <= i + k - 2*

**Number of added windows:** *2k - 2 - max(0, k - 2 - i + 1) <= 2k - 2*

### Shifted Windows
Say *i* is the index of the **deleted** window in some iteration, and *A = [a, a + k - 1]* is a *k*-long window in *w* **before** the deletion. Then *A* is a shifted window if one of these cases holds:

1. *0 <= a <= i - k* (shifted by *k - 1*)
2. *i + k <= a <= n - k* (shifted by *-1*)

**Number of shifted windows:** *max(0, i - k + 1) + max(0, n - i - 2k + 1) = O(n)*

### On 1-Bit Redundancy
Our encoder is a one-to-one function *E: [q]^(n - 1) -> [q]^n*. All encoder output vectors (the encoder image) are *(2 &bull; log_q(n) + 2)*-repeat-free. Are there enough of these vectors in *[q]^n* for them to satisfy unique source vectors?

**Proposition.** Denote by A(n, k) the number of vectors of length *n* which are *k*-repeat-free, then for all *k >= 2 &bull; log_q(n)*, it holds that *A(n, k) >= q^(n - 1)*.

*Proof.* We count the number of "bad" vectors. To do so, we count the number of vectors whose *i*-th window is identical to its *j*-th window, for *j > i*. For such *i, j*, the *k* values in the *j*-th window are determined by the *k − max(0, j − i)* values in the *i*-th window. That is, even if the two windows overlap, the number of values that are automatically determined is *k*. (Truly, if they do not overlap, this is clear. Otherwise, they overlap in *j − i* bits. The first *k − (j − i)* bits of the *i*-th window will determine the next *k − (j − i)* bits of the union block of the two windows, which in turn determine the next bits until all the union block is determined.) Thus, the number of “free” choosable bits is *n − k*, in all cases. Then for any *i, j*, the number of non-*k*-repeat-free vectors with such two identical windows is *q^(n - k)*. Clearly, a vector might satisfy this property for two different values for *i, j*, so we are over-counting. Then we have

[Number of bad vectors]
* <= sum of [Number of bad vectors with identical windows at i, j] for *1 <= i < j <= n - k + 1*
* &nbsp;= sum of *(q^(n - k))* for *1 <= i < j <= n - k + 1*
* <= sum of *(q^(n - 2 &bull; log_q(n)))* for *1 <= i < j <= n*
* &nbsp;= *(n choose 2) &bull; q^(n - 2 &bull; log_q(n))*
* &nbsp;= *(n(n - 1) / 2) &bull; q^n / n^2*
* &nbsp;= *((n - 1) / n) &bull; q^(n - 1)*
* <= *q^(n - 1)*

Even with over-counting, we successfully upper-bounded the number of bad vectors by *q^(n - 1)*.
Therefore, the number of “good” *k*-repeat-free vectors is at least *q^n − q^(n − 1) >= q^(n − 1)*, as required to prove. 

