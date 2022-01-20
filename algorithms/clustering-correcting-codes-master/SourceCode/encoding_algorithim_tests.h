//
// Created by amitw on 19/01/2020.
//

#ifndef CLUSTERING_CORRECTING_CODES_PROJECT_ENCODING_ALGORITHIM_TESTS_H
#define CLUSTERING_CORRECTING_CODES_PROJECT_ENCODING_ALGORITHIM_TESTS_H

#include "encoding_algorithim.h"


void creatingStrands(
        unordered_map<int, vector<int>>& strands,
        unordered_map<int, encoded_strand_binary>& encoded_strands) {

    int zero = 0;
    int one = 1;
    int two = 2;
    int three = 3;
    int four = 4;
    int five = 5;
    int six = 6;
    int seven = 7;




    vector<int> data_0{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    vector<int> data_1{0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1};
    vector<int> data_2{0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0};
    vector<int> data_3{1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0};
    vector<int> data_4{1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0};
    vector<int> data_5{1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0};
    vector<int> data_6{0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1};
    vector<int> data_7{1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};



    /// inserting strands;
    strands[zero] = data_0;
    strands[one] = data_1;
    strands[two] = data_2;
    strands[three] = data_3;
    strands[four] = data_4;
    strands[five] = data_5;
    strands[six] = data_6;
    strands[seven] = data_7;
//    encoded_strand_binary encoded(output_fourthy_one, false);
//    pair<int, encoded_strand_binary> p(seven, encoded);
//    encoded_strands.insert(p);
}


void creatingStrandsForEncoding(
        unordered_map<int, vector<int>>& strands,
        unordered_map<int, encoded_strand_binary>& encoded_strands) {

    int zero = 0;
    int one = 1;
    int two = 2;
    int three = 3;
    int four = 4;
    int five = 5;
    int six = 6;
    int seven = 7;
    vector<int> data_0{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    vector<int> data_1{0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1};
    vector<int> data_2{0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0};
    vector<int> data_3{1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0};
    vector<int> data_4{1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1};
    vector<int> data_5{0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1};
    vector<int> data_6{0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1};
    vector<int> data_7{1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
    /// inserting strands;
    strands[zero] = data_0;
    strands[one] = data_1;
    strands[two] = data_2;
    strands[three] = data_3;
    strands[four] = data_4;
    strands[five] = data_5;
    strands[six] = data_6;
    strands[seven] = data_7;
//    encoded_strand_binary encoded(output_fourthy_one, false);
//    pair<int, encoded_strand_binary> p(seven, encoded);
//    encoded_strands.insert(p);
}


void printVector(vector<int> vec){
    for(int i = 0; i < vec.size(); i++){
        cout << vec[i];
    }
    cout << endl;
}

void printVectorOfVecotrs(vector<vector<int>>& print){
    for(int i = 0; i < print.size(); i++){
        printVector(print[i]);
    }
}

void testCreateDelta1(){
    vector<int> index_i{1, 0, 0, 0};
    vector<int> index_j{1, 1, 1, 1};
    vector<int> test_padding{1, 0, 0, 1};
    vector<int> delta_1_binary;
    int M = 8;
    int e = 3;
    create_delta_1(index_i, index_j, delta_1_binary, e, M);
    printVector(delta_1_binary);
    delta_1_binary.clear();
    // test padding
    create_delta_1(index_i, test_padding, delta_1_binary, e, M);
    printVector(delta_1_binary);

}


void testCreateDelta2(){
    vector<int> data_i{1, 0, 0, 0, 1, 0, 0, 0};
    vector<int> data_j{1, 1, 1, 1, 1, 0, 0, 0};
    vector<int> test_padding{1, 0, 0, 0, 1, 1, 0, 0};
    vector<int> test_identical_padding{1, 0, 0, 0, 1, 0, 0, 0};
    int M = 8;
    int strand_data_length = 8;
    int t = 4;
    vector<int> delta_2_binary;
    create_delta_2(data_i, data_j, M, 8, t, delta_2_binary);
    printVector(delta_2_binary);
    delta_2_binary.clear();
    create_delta_2(data_i, test_padding, M, 8, t, delta_2_binary);
    printVector(delta_2_binary);
    delta_2_binary.clear();
    create_delta_2(data_i, test_identical_padding, M, 8, t, delta_2_binary);
    printVector(delta_2_binary);

}

void createVectorsForTests(vector<vector<int>> & strands_data){
    vector<int> one{1, 0, 0, 0, 1, 0, 0, 0, 0, 1 ,0 ,1, 1, 0, 1, 0, 1};
    vector<int> two{1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1};
    vector<int> three{1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1};
    vector<int> four{1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1};
    vector<int> zeros{0, 0, 0, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1};
    strands_data.push_back(one);
    strands_data.push_back(two);
    strands_data.push_back(three);
    strands_data.push_back(four);
    strands_data.push_back(zeros);

}

void testW_lBruteForce(){
    vector<vector<int>> strands_data;
    int t = 1;
    vector<int> w_output;
    int N = 5;
    createVectorsForTests(strands_data);
    W_l_S_t_BruteForce(strands_data, t, w_output, HammingDistance, N, 3);
    printVector(w_output);
}


void testW_lNoBruteForce(){
    vector<vector<int>> strands_data;
    int t = 4;
    vector<int> w_output;
    int N = 5;
    createVectorsForTests(strands_data);
    W_l_S_t_NoBruteForce(strands_data, t, w_output, HammingDistance, N, 3);
    printVector(w_output);

}



void testCreateS_e_i(){
    unordered_map<int, vector<int>>strands;
    int e = 3;
    int i = 5;
    vector<vector<int>> output_data;
    unordered_map<int,encoded_strand_binary> encoded_strands;
    creatingStrands(strands, encoded_strands);
    int N = 0;
    /// test1
    S_e_i(strands, e, i, HammingDistance, output_data, encoded_strands, 3, N);
    vector<int> output_in_ints;
    for(int i = 0; i < output_data.size(); i++){
        output_in_ints.push_back(binaryToDec(output_data[i]));
    }
    printVector(output_in_ints);
    output_in_ints.clear();
    output_data.clear();
    /// test2
    e = 1;
    S_e_i(strands, e, i, HammingDistance, output_data, encoded_strands, 3, N);
    for(int i = 0; i < output_data.size(); i++){
        output_in_ints.push_back(binaryToDec(output_data[i]));
    }
    printVector(output_in_ints);

}

void testCreateReplVector(){
    vector<int> delta_1{1, 0, 0, };
    vector<int> delta_2{1, 1, 1,};
    vector<int> w_l{1, 0, 0,};
    vector<int> repl;
    int index_length = 6;
    int L = 15;
    // no padding
    createReplVector(w_l, delta_1, delta_2, repl, L, index_length);
    printVector(repl);
    // padding
    repl.clear();
    L = 20;
    createReplVector(w_l, delta_1, delta_2, repl, L, index_length);
    printVector(repl);

}

void testAddEncodedVersion(){
    vector<int> repl_vector{1, 0, 0, 1, 1, 1, 1, 1, 1};
    vector<int> original_strand_data{1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0 , 0, 1, 1};
    int i = 5;
    int index_length = 3;
    unordered_map<int, encoded_strand_binary> encoded_strands;
    bool BruteForce = true;
    addEncodedVersion(repl_vector, original_strand_data, i, 3, encoded_strands, true);
    printVector(encoded_strands.find(i)->second.get_encoded_data());
}

void printAllEncoded(unordered_map<int, encoded_strand_binary>& encoded_strands){
    for(auto it = encoded_strands.begin(); it != encoded_strands.end(); it++){
        printVector(it->second.get_encoded_data());
    }
}
void testEncodingAlgorithim(){
    unordered_map<int, vector<int>>strands;
    int e = 1;
    int t = 2;
    int strands_data_length = 16;
    unordered_map<int, encoded_strand_binary> encoded_strands;
    bool BruteForceOrNot = false;
    creatingStrands(strands, encoded_strands);
    /// not brute force, no strand need to be encoded
    encoding_algorithm(strands, e, t, strands_data_length, HammingDistance, encoded_strands, false);
    cout << "********* TEST 1 ***********" << endl;
    printAllEncoded(encoded_strands);
    /// not brute force, strands need to be encoded
    strands.clear();
    encoded_strands.clear();
    cout << "********* TEST 2 ***********" << endl;
    creatingStrandsForEncoding(strands, encoded_strands);
    encoding_algorithm(strands, e, t, strands_data_length, HammingDistance, encoded_strands, false);
    printAllEncoded(encoded_strands);
    /// brute force, strands need to be encoded
    strands.clear();
    encoded_strands.clear();
    cout << "********* TEST 3 ***********" << endl;
    creatingStrandsForEncoding(strands, encoded_strands);
    encoding_algorithm(strands, e, t, strands_data_length, HammingDistance, encoded_strands, true);
    printAllEncoded(encoded_strands);





}



#endif //CLUSTERING_CORRECTING_CODES_PROJECT_ENCODING_ALGORITHIM_TESTS_H
