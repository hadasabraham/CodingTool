//
// Created by amitw on 19/01/2020.
//

#ifndef CLUSTERING_CORRECTING_CODES_PROJECT_DECODING_ALGORITHIM_TESTS_H
#define CLUSTERING_CORRECTING_CODES_PROJECT_DECODING_ALGORITHIM_TESTS_H

#include "decoding_algorithim.h"
#include "encoding_algorithim_tests.h"



void createEncodedStrands(unordered_map<int, encoded_strand_binary>& encoded_strands){
    vector<int> data_0{1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    vector<int> data_1{0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1};
    vector<int> data_2{1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1};
    vector<int> data_3{0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1};
    vector<int> data_4{1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1};
    vector<int> data_5{0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1};
    vector<int> data_6{1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1};
    vector<int> data_7{0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
    encoded_strand_binary zero(data_0, false);
    encoded_strand_binary one(data_1, false);
    encoded_strand_binary two(data_2, false);
    encoded_strand_binary three(data_3, false);
    encoded_strand_binary four(data_4, false);
    encoded_strand_binary five(data_5, false);
    encoded_strand_binary six(data_6, false);
    encoded_strand_binary seven(data_7, false);

    pair<int,encoded_strand_binary> p0(0, zero);
    pair<int,encoded_strand_binary> p1(1, one);
    pair<int,encoded_strand_binary> p2(2, two);
    pair<int,encoded_strand_binary> p3(3, three);
    pair<int,encoded_strand_binary> p4(4, four);
    pair<int,encoded_strand_binary> p5(5, five);
    pair<int,encoded_strand_binary> p6(6, six);
    pair<int,encoded_strand_binary> p7(7, seven);
    encoded_strands.insert(p0);
    encoded_strands.insert(p1);
    encoded_strands.insert(p2);
    encoded_strands.insert(p3);
    encoded_strands.insert(p4);
    encoded_strands.insert(p5);
    encoded_strands.insert(p6);
    encoded_strands.insert(p7);


}

void testCreateDecodingOrderList(){
    unordered_map<int, encoded_strand_binary> encoded_strands;
    vector<int> decoding_order_list;
    createEncodedStrands(encoded_strands);
    createDecodingOrderList(encoded_strands, decoding_order_list);
    printVector(decoding_order_list);
}


void testDecodeIndex(){
    unordered_map<int, encoded_strand_binary> encoded_strands;
    createEncodedStrands(encoded_strands);
    int e = 1;
    int t = 2;
    cout << DecodeIndex(encoded_strands.find(4)->second, 4, 8, e, t, HammingDistance) << endl;

}

void testDecodeData(){
    unordered_map<int, encoded_strand_binary> encoded_strands;
    createEncodedStrands(encoded_strands);
    int e = 1;
    int t = 2;
    DecodeData(encoded_strands.find(4)->second, encoded_strands.find(7)->second.get_encoded_data(),
              4, 8, 16, e, t, HammingDistance);
    printVector(encoded_strands.find(4)->second.get_encoded_data());
}



void testDecodingAlgorithim(){
    unordered_map<int, encoded_strand_binary> encoded_strands;
    createEncodedStrands(encoded_strands);
    int strand_data_length = 16;
    int e = 1;
    int t = 2;
    DecodingAlgorithim(encoded_strands, strand_data_length, e, t, HammingDistance);
    printAllEncoded(encoded_strands);


}




#endif //CLUSTERING_CORRECTING_CODES_PROJECT_DECODING_ALGORITHIM_TESTS_H
