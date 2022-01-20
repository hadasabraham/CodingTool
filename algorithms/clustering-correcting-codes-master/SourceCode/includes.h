//
// Created by amitw on 18/01/2020.
//

#ifndef CLUSTERING_CORRECTING_CODES_PROJECT_INCLUDES_H
#define CLUSTERING_CORRECTING_CODES_PROJECT_INCLUDES_H
#include <math.h>
#include <algorithm>
#include <tuple>
#include <set>
#include <map>
#include <unordered_map>
#include <assert.h>
#include <iostream>
#include <vector>
#include <fstream>
#include <string>
//#endif //CLUSTERING_CORRECTING_CODES_PROJECT_INCLUDES_H

using namespace std;

/*!
 * function that convert binary number represented as a vector to its decimal representation
 * @param input - the binary number as a vector
 * @param
 * @return output - the output decimal number as an int.
 */
int binaryToDec(vector<int> input){
    int decimal = 0;
    int length = input.size();
    for(int i = 0; i < input.size(); i++){
        if(input[i] == 1){
            decimal += pow(2, length - 1 - i);
        }
    }
    return decimal;
}


int HammingDistance(
        vector<int> one,
        vector<int> two){

    if(one.size() != two.size()){
        cout << "Hamming distance is defined only for vectors from the same size" << endl;
        return -1;
    }
    int distance = 0;
    for(int i = 0; i < one.size(); i++){
        if(one[i] != two[i]){
            distance++;
        }
    }
    return distance;

}



/*!
 * function to convert decimal to binary
 * @param n - the decimal number to be converted
 * @param output - an output vector containing the binary representation of the number
 */
void decToBinary(int n, vector<int>& output) {
    int i = 0;
    if(n == 0){
        output.push_back(0);
        return;
    }
    while (n > 0) {

        // storing remainder in binary array
        output.push_back(n % 2);
        n = n / 2;
        i++;
    }
    reverse(output.begin(), output.end());
}

/*!
 * function to convert decimal to binary
 * @param n - the decimal number to be converted
 * @param output - an output vector containing the binary representation of the number
 */
void decToBinaryWithSize(int n, vector<int>& output, int size) {
    int i = 0;
    if(n == 0){
        output.push_back(0);
        size--;
    }
    while (n > 0) {
        size--;
        // storing remainder in binary array
        output.push_back(n % 2);
        n = n / 2;
        i++;
    }
    //
    while(size > 0){
        output.push_back(0);
        size--;
    }
    reverse(output.begin(), output.end());
}

/*!
 * function for converting a char vec into int vec so '1001' will become 1001.
 * @param char_vec - char vec
 * @param int_vec - output int vec.
 */
void convertCharVecToIntVec(
        vector<char>& char_vec,
        vector<int>& int_vec){

        for(int i = 0; i < char_vec.size(); i++){
            int_vec.push_back(char_vec[i] - '0');
        }
}

/*!
 * function for converting a int vec into char vec so 1001 will become '1001'.
 * @param char_vec - char vec
 * @param int_vec - output int vec.
 */
void convertIntVecToCharVec(
        vector<char>& char_vec,
        vector<int>& int_vec){

    for(int i = 0; i < int_vec.size(); i++){
        char_vec.push_back(int_vec[i] + '0');
    }
}


/*!
 * this function is calculating all the binary numbers that are far from a given number by one in a given distance
 * metric (hamming or edit)
 * @param num - the given number
 * @param numbers - the output set of all the numbers that are far in one bit.
 * @param distanceMetric - pointer to the distance function
 */
void distanceByOne(
        vector<int> num,
        set<vector<int>>& numbers,
        int (*distanceMetric)(vector<int>, vector<int>)){

    for(int i = 0; i < num.size(); i++){
        vector<int> index_j;
        index_j = num;
        if(num[i] == 0){
            index_j[i] = 1;
        }
        else{
            index_j[i] = 0;
        }
        numbers.insert(index_j);
    }
//    num.insert(num.begin(), 1);
//    numbers.insert(num);
}



/*!
 * this function will helps us calculating S(e,i),  for each number in the given input_number set
 * we're calculating all the binary numbers that are far from him in one bit (hamming distance) and
 * inserting it into the output_numbers set (which eventually will contain all the numbers).
 * @param numbers - the set of the input binary numbers
 * @param output_numbers - the output set containing all the numbers that are far in one bit from a number
 * in the input set.
 * @param distanceMetric - pointer to the distance function

 */
void distanceByOneFromSet(
        set<vector<int>>& input_numbers,
        set<vector<int>>& output_numbers,
        int (*distanceMetric)(vector<int>, vector<int>)){

    for(auto it = input_numbers.begin(); it != input_numbers.end(); it++){
        distanceByOne(*it, output_numbers, distanceMetric);
    }
}

#endif