//
// Created by amitw on 22/11/2019.
//

#ifndef CLUSTERING_CORRECTING_CODES_PROJECT_ENCODING_ALGORITHIM_H
#define CLUSTERING_CORRECTING_CODES_PROJECT_ENCODING_ALGORITHIM_H

#include "encoded_strand_binary.h"
#include "errorCluster.h"



/*!
 * the delta1 function from the article, encodes the diffrence between two indexes (i, j)
 * by saving the positions where they are differ, as well as adding padding if needed
 * @param index_i - the i index
 * @param index_j - the j index
 * @param delta_1_binary - a vector of the positions where the two indexes differ, in binary.
 * @param e the index constraint parameter
 * @param M - number of strands in the system
 *
 */
void create_delta_1(
        vector<int> index_i,
        vector<int> index_j,
        vector<int>& delta_1_binary,
        int e,
        int M){

    /// delta_1 size should be e * log(log(M))
    int delta_1_size = ceil(log2(ceil(log2(M)))) * e;
    int index_position_length = ceil(log2(ceil(log2(M))));
    vector<int> binary_num;
    /// if their size is diffrent then hamming distance is not defined.
    if(index_i.size() != index_j.size()){
        return;
    }
    vector<int> last_position_binary;
    for(int i = 0; i < index_i.size(); i++){
        if(index_i[i] != index_j[i]){
            vector<int> current_position_binary;
            decToBinaryWithSize(i, current_position_binary, index_position_length);
            delta_1_binary.insert(delta_1_binary.end(), current_position_binary.begin(), current_position_binary.end());
            last_position_binary = current_position_binary;
        }
    }
    /// we do padding of the last position untill we get to the size we wanted
    while(delta_1_binary.size() != delta_1_size){
        delta_1_binary.insert(delta_1_binary.end(), last_position_binary.begin(), last_position_binary.end());
    }
}


/*!
 *  The function ∆2(ui,uj ) encodes the difference betweenthe two data fields ui,uj
     of Hamming distance at most t−1 using (t−1) log(LM) bits which mark
t   he positions where they differ, we will represent the positions as base 10 numbers
 * @param data_u_i - the data of u_i
 * @param data_u_j - the data of u_j
 * @param strands_num - number of strands in the system
 * @param strands_length - length of a strand's data (L)
 * @param t - the data constraint.
 * @param delta_2_binary = the output delta2 in binary format.
 */
void create_delta_2(
        vector<int> data_u_i,
        vector<int> data_u_j,
        int strands_num,
        int strands_data_length,
        int t,
        vector<int>& delta_2_binary){

        /// delta_2 size should be log(L - log(M)) * (t - 1)
        int delta_2_size = ceil(log2(strands_data_length)) * (t - 1);
        /// length of each position encoded in binary
        int data_position_length = ceil(log2(strands_data_length));
        vector<int> positions;
        for(int i = 0; i < data_u_i.size(); i++){
            if(data_u_i[i] != data_u_j[i]){
                positions.push_back(i);
            }
        }
        /// convert the positions to binary
        for(int i = 0; i < positions.size(); i++){
            vector<int> current_position_binary;
            decToBinaryWithSize(positions[i], current_position_binary, data_position_length);
            delta_2_binary.insert(delta_2_binary.end(), current_position_binary.begin(), current_position_binary.end());
         }
        /// we do padding of the last position untill we get to the size we wanted
        /// or in case no positions differ (delta2 is empty), we just put unordered numbers

        /// case we do padding with the last position in delta2
        if (!positions.empty()) {
            vector<int> last_position_binary;
            decToBinaryWithSize(positions.back(), last_position_binary, data_position_length);
            while (delta_2_binary.size() != delta_2_size) {
                delta_2_binary.insert(delta_2_binary.end(), last_position_binary.begin(),
                                      last_position_binary.end());
            }
        }
        /// in case the two datas were similar, put unordered numbers
        else{
            while (delta_2_binary.size() != delta_2_size) {
                vector<int> random_number;
                decToBinaryWithSize(strands_data_length - 1, random_number, data_position_length);
                delta_2_binary.insert(delta_2_binary.end(), random_number.begin(), random_number.end());
                strands_data_length--;
            }

        }

    }


/*!
 * this two functions will create all the binary strings of a given length and insert it to the binary_Strings vector
 * @param binary_strings - output vector of vectors, where each element will represent a binary number
 * @param length - the length of the binary strings we want to generate
 *
 */
void CreateAllBinaryStringsAux(
        vector<vector<int>>& binary_strings,
        vector<int> current,
        int length){

    if(current.size() == length){
        binary_strings.push_back(current);
    }
    else{
        current.push_back(0);
        CreateAllBinaryStringsAux(binary_strings, current, length);
        current.pop_back();
        current.push_back(1);
        CreateAllBinaryStringsAux(binary_strings, current, length);
    }
}

void CreateAllBinaryStrings(
        vector<vector<int>>& binary_strings,
        int length){

    vector<int> current;
    CreateAllBinaryStringsAux(binary_strings, current, length);
}


/*!
 * this function is getting a 3*t + 2Log(N) size window from a given strand data starting from logM index.
 * @param strand_data - data of the strand
 * @param output - the window
 * @param t - the distance constraint
 * @param N - the number of strands we're calculating w_l w.r.t them
 * @param index_length - the length of an index of a strand (ceil(logM))
 */
void GetBruteForceWindowFromStrandData(
        vector<int>& strand_data,
        vector<int>& output,
        int t,
        int N,
        int index_length){

    int window_size = 3 * t + 2 * ceil(log2(N+1));
    for(int i = index_length; i < window_size + index_length; i++){
        output.push_back(strand_data[i]);
    }
}



/*!
 * this function is for creating the set : S(e,i) = {Uj | d(hamming, edit) (ind_i, ind_j) <= e}
 * means returning all the data of the strands which their hamming or edit distance between their indexes and the given
 * index is smaller than e
 * @param strands - the strands in the DNA system
 * @param e - the parameter for the distance
 * @param i - a number representing the i'th strand we're checknig by its index.
 * @param distanceMetric- a pointer to a function of distance metric (hamming or edit)
 * @param output_data - the output strands data
 * @param encoded_strands - the encoded strands data structure.
 * @param index_length - length of the binary representation of an index.
 * @param N - number of binary strings that are from from the given index (i) by e indexes at most. (they dont have to be
 * in the system, this parameter will be later used from calculating w_l
 */

void S_e_i(
        unordered_map<int, vector<int>>& strands,
        const int e,
        const int i,
        int (*distanceMetric)(vector<int>, vector<int>),
        vector<vector<int>>& output_data,
        unordered_map<int,encoded_strand_binary>& encoded_strands,
        int index_length,
        int& N) {

    vector<int> index_binary_representation;
    decToBinaryWithSize(i, index_binary_representation, index_length);
    /// we're going to create a set of all the indexes such that each one of them is diffrent from i in at most e bits,
    /// and its not i.
    int count_till_e = 1;
    set<vector<int>> relevant_indexes;
    set<vector<int>> output_indexes;
    set<vector<int>> union_of_all;
    distanceByOne(index_binary_representation, relevant_indexes, distanceMetric);
    union_of_all = relevant_indexes;
    count_till_e++;
    while(count_till_e <= e){
        distanceByOneFromSet(relevant_indexes, output_indexes, distanceMetric);
        relevant_indexes = output_indexes;
        union_of_all.insert(output_indexes.begin(), output_indexes.end());
        count_till_e++;
    }
    vector<int> dec_indexes;
    /// deleting i from the set.
    for(auto it = union_of_all.begin(); it != union_of_all.end(); it++){
        if(*it == index_binary_representation){
            union_of_all.erase(it);
        }
    }
    N = union_of_all.size();
    /// inserting the data of the relevant indexes.
    for(auto it = union_of_all.begin(); it != union_of_all.end(); it++){
        int check = binaryToDec(*it);
        if(check == i) {
            continue;
        }
        /// you check if the strand has been encoded already, if it was then we retrive its data from the encoded strand's data structure
        auto encoded_data = encoded_strands.find(check);
        if(encoded_data != encoded_strands.end()) {
            output_data.push_back(encoded_data->second.get_encoded_data());
        }
        /// in case the strand hasent been encoded yet, we look for its data in the strands's data structure
        else{
            auto data = strands.find(check);
            if(data != strands.end()){
                output_data.push_back(data->second);

            }
        }

    }
}

/*!
 * this function checks for a given distance metric if a is far from b in more then t (according to the given distance metric)
 * @param a - vector of ints
 * @param b - vector of ints
 * @param t - the given number we want the distance to be greater then
 * @param distanceMetric - the given distance metric we're checking the distance by.
 * @return - true or false according if they holds the constraint.
 */

bool checkConstraint(
        vector<int> a,
        vector<int> b,
        int t,
        int (*distanceMetric)(vector<int>, vector<int>)){

    if(distanceMetric(a, b) >= t){
        return true;
    }
    else return false;
}

/*!
 * the function Wl(S,t) , returns a vector w which satisfies the following condition:
 *  For all v ∈ S, d(w, v[log(M),l]) > t. (the distance in the data part is at least t)
 *  we will find the suitable vector in a brute force manner.
 * @param strands - the strands in the system
 * @param t - the  distance parameter
 * @param w_output - the output vector that satisfies the condition
 * @param strands_num - the number of the strands in the system.
 * @param N - number of strands that our window need to be diffrent from their data in at least t bits
 * @param index_legnth - the length of an index of a strand (which is logM).
 */
void W_l_S_t_BruteForce(
        vector<vector<int>>& strands_data,
        int t,
        vector<int>& w_output,
        int (*distanceMetric)(vector<int>, vector<int>),
        int N,
        int index_legnth){

    /// first we create all the binary strings from length t.
    vector<vector<int>> binary_strings;
    CreateAllBinaryStrings(binary_strings, 3 * t +  2 * ceil(log2(N + 1)));
    /// flag denoting if a binary string holds the constraint w.r.t all the strands we're checking (N).
    int constraint_approved_fo_all = 1;
    for(int i = 0; i < binary_strings.size(); i++){
        for(int j = 0; j < strands_data.size(); j++){
            vector<int> relevant_part_of_data;
            GetBruteForceWindowFromStrandData(strands_data[j], relevant_part_of_data, t, N, index_legnth);
            if(!checkConstraint(binary_strings[i], relevant_part_of_data, t,  distanceMetric)){
                constraint_approved_fo_all = 0;
            }
        }
        if(constraint_approved_fo_all == 1){
            w_output = binary_strings[i];
            return;
        }
        else{
            constraint_approved_fo_all = 1;
        }
    }


}
/*!
 * this function is a helper function, it gets two vectors and it checks if the binary string distance is at least one
 * from the strand data vector[start_index - start_index + Log(N+1)], it helps us in w_l_s_T function (the one without the brute force)
 * @param binary_string - the binary string we check if the constraint applies.
 * @param strand_data - the strand's data, as a vector
 * @param start_index - the starting index we're checking from
 * @param N - number of strands in the system (this is for Log(N+1)
 * @param distanceMetric - the distance metric we're checking by.
 * @return - true - the constraint applies, otherwise false.
 */
bool checkConstraintFromStrtTillLogN(
        vector<int>& binary_string,
        vector<int>& strand_data,
        int start_index,
        int N,
        int (*distanceMetric)(vector<int>, vector<int>)){

        vector<int> relevant_part_of_data(strand_data.begin() + start_index, strand_data.begin() + start_index + ceil(log2(N + 1)));
        return checkConstraint(binary_string, relevant_part_of_data, 1, distanceMetric);
}

/*!
 * the second function for finding Wl(S,t) , returns a vector w which satisfies the following condition:
 *  For all v ∈ S, d(w, v[log(M),l]) > t. (the distance in the data part is at least t)
 *  this time we look every time on a Log(N+1) size window, finding a binary string that are diffrent from all the strand's data
 *  in this window by at least one bit (we check that in a brture force manner, for each window), then we do it t times
 *  and at the end we combine the t binary strings and that will be our output vector.
 * @param strands_data - the strand's data
 * @param t - the number of bits we want our vector to be diffrent at.
 * @param w_output - the output vector
 * @param distanceMetric - the distance metric we're checking with.
 * @param strands_num - number of strands in the system
 * @param N - number of strands that our window need to be diffrent from their data in at least t bits
 * @param index_legnth - the length of an index of a strand (which is logM).

 */
void W_l_S_t_NoBruteForce(
        vector<vector<int>>& strands,
        int t,
        vector<int>& w_output,
        int (*distanceMetric)(vector<int>, vector<int>),
        int N,
        int index_length) {

        // create potential logN+1 size windows
        vector<vector<int>> binary_strings;
        CreateAllBinaryStrings(binary_strings, ceil(log2(N + 1)));

        // flag to check wether a window is valid (holds constraint for all N strands)
        int constraint_approved_fo_all = 1;

        // moving window loop
        for (int i = 0, j = index_length; i < t && j < t * log2(N + 1) + index_length; i++, j += ceil(log2(N + 1))) {

            for (int index = 0; index < binary_strings.size(); index++) {
                // check the binary string holds the constraint with all of the strands
                for (int data_index = 0; data_index < strands.size(); data_index++) {
                    if (!checkConstraintFromStrtTillLogN(binary_strings[index], strands[data_index], j, strands.size(),
                                                         distanceMetric)) {
                        constraint_approved_fo_all = 0;
                        break;
                    }
                }
                /// if the constraint is approved we concatenate the vectors.
                if (constraint_approved_fo_all == 1) {
                    w_output.insert(w_output.end(), binary_strings[index].begin(), binary_strings[index].end());
                    break;
                }
                constraint_approved_fo_all = 1;
            }
        }
    }





/*!
 * function that gets an index for strand i, and find a strand j such that i < j && d(index_i,index_j) <= e &&
 * d(data_i, data_j) < t, means that i need to be fixed by.
 * if no strand j is found, means i dosent need to be fixed, so we create an encoded version of him without changing its data
 * @param strands - the strands in the system
 * @param i - the index of the i'th strand
 * @param t - the distance in data constraint
 * @param e - the distance in index constraint
 * @param BruteForce - wether we're using brute force manner for creating w_l or not in the algorithim
 * @param distanceMetric - the distance metric we're checking by
 * @param B - the vector that will hold the output (tuple i, j)
 * @param encoded_strands - the strands that have been encoded already
 */
void find_pair_to_be_fixed(
        unordered_map<int, vector<int>>& strands,
        int i,
        int t,
        int e,
        bool BruteForce,
        int (*distanceMetric)(vector<int>, vector<int>),
        vector<tuple<int, int>>& B,
        unordered_map<int, encoded_strand_binary>& encoded_strands){

    int index_length = ceil(log2(strands.size()));
    vector<int> index_i;
    decToBinaryWithSize(i, index_i, index_length);
    auto i_data = strands.find(i)->second;
    for (int j = i; j < strands.size(); j++) {
        if (j <= i) {
            continue;
        }
        vector<int> index_j_binary;
        decToBinaryWithSize(j, index_j_binary, index_length);
        if (distanceMetric(index_i, index_j_binary) <= e ){
            auto encoded_version = encoded_strands.find(j);
            if(encoded_version == encoded_strands.end()){
                if(distanceMetric(i_data, strands.find(j)->second) < t){
                    tuple<int, int> pair(i, j);
                    B.push_back(pair);
                    /// in case we found one j that dosent hold the constraint for a given i
                    /// we dont have to look for other j's, so we break
                    return;
                }
            }
            else{
                /// we search in the encoded part only because of the last strand, (cause besides him all the encoded strands must
                /// hold the constraint).
                if(distanceMetric(i_data, encoded_version->second.get_encoded_data()) < t){
                    tuple<int, int> pair(i, j);
                    B.push_back(pair);
                    /// in case we found one j that dosent hold the constraint for a given i
                    /// we dont have to look for other j's, so we break
                    return;
                }
            }
        }
    }
    /// in case the strand dosent need to be encoded, we add encoded strand with the index of the strand
    /// in the strand data structure, so we could find it later in the decode part.
    encoded_strand_binary current(i_data, BruteForce);
    pair<int, encoded_strand_binary> new_strand(i, current);
    encoded_strands.insert(new_strand);
}



/*!
 * function for creating repl vector  repl = {wl, delta_1, delta_2}, in case repl vector
 * length is less than L - index_length (which is L - ceil(LogM)), we padd it with zeros at the end.
 * we add padding of zeros
 * @param w_l - w_l vector
 * @param delta_1 - delta1 vector
 * @param delta_2 - delta2 vector
 * @param L - strand total length
 * @param next_index_length - the length of the binary representation of the next strand's index in the encoding list.

 */
void createReplVector(
        vector<int>& w_l,
        vector<int>& delta_1,
        vector<int>& delta_2,
        vector<int>& repl,
        int L,
        int next_index_length){

        repl.insert(repl.end(), w_l.begin(), w_l.end());
        repl.insert(repl.end(), delta_1.begin(), delta_1.end());
        repl.insert(repl.end(), delta_2.begin(), delta_2.end());
        /// add padding
        while(repl.size() != L - next_index_length){
            repl.push_back(0);
        }
}

/*!
 * function for creating the encoded version of a strand, before its 0-LogM bits
 * being updated to hold the next node in the encoding list, therefore the version should be
 * 0 - LogM of the original non encoded version + repl vector.
 * @param repl_vector - the repl vector that was created by the encoding algorithim for the strand
 * @param original_strand_data - the data of the non encoded version of the strand.
 * @param i - the index of the strand
 * @param index_length - length of the index (ceil(logM))
 * @param encoded_strands - the encoded strands data structure, we add the encoded version to.
 * @param BruteForce - wether we used brute force manner for creating w_l or not.
 */
void addEncodedVersion(
        vector<int>& repl_vector,
        vector<int>& original_strand_data,
        int i,
        int index_length,
        unordered_map<int, encoded_strand_binary>& encoded_strands,
        bool BruteForce)
{

        /// first we take the 0-LogM bits of the original vector
        vector<int> first_LogM_bits{original_strand_data.begin(), original_strand_data.begin() + index_length};
        /// add repl
        first_LogM_bits.insert(first_LogM_bits.end(), repl_vector.begin(), repl_vector.end());
        encoded_strand_binary encoded_strand(first_LogM_bits, BruteForce);
        pair<int, encoded_strand_binary> pair(i, encoded_strand);
        encoded_strands.insert(pair);
}

/*!
 * the encoding algorithim as it was described in psuedo code in the papaer.
 * @param strands - the strands inthe system
 * @param e - the distance constraint of the indexes
 * @param t - the distance constraint of the data of the strands
 * @param strands_data_length - L, the length of strand's data.
 * @param distanceMetric - the distance metric we're using (hamming \ edit)
 * @param encoded_strands - data structure that will hold all of the encoded strands.
 * @param BruteForceOrNot - a flag that tells us if we should find w_l in brute force manner or not
 */
void encoding_algorithm(
        unordered_map<int, vector<int>>& strands,
        int e,
        int t,
        int strands_data_length,
        int (*distanceMetric)(vector<int>, vector<int>),
        unordered_map<int, encoded_strand_binary>& encoded_strands,
        bool BruteForceOrNot) {


    /// initilize p
    int M = strands.size();
    int p = M - 1;
    vector<tuple<int, int>> B;
    int index_length = ceil(log2(M));
    int delta_1_size = ceil(log2(index_length)) * e;
    int delta_2_size = ceil(log2(strands_data_length)) * (t - 1);

    /** check the constraint  data_length > LogM + 1 + e*LogLogM + (t-1)* log(L-LogM) + w
        where w is the number of bits needed for encoding w_l (which its length depends wether we find it
        on brute force manner or not  NEED TO BE FIXED.
     **/
//    int len = index_length + 1 + delta_1_size + delta_2_size + t * ceil(log2(M));
//    int len2 = index_length + 1 + delta_1_size + delta_2_size + 3*t + 2 * delta_1_size;
    if(BruteForceOrNot){
        if(strands_data_length < index_length + 1 + delta_1_size + delta_2_size + 3*t + 2 * delta_1_size){
            cout << "strand length dosent hold the constraint" << endl;
            return;
        }
    }

    else if(strands_data_length < index_length + 1 + delta_1_size + delta_2_size + t * ceil(log2(M))){
        cout << "strand length dosent hold the constraint" << endl;
        return;
    }

    /// add the last strand to the encoded_strand map
    encoded_strand_binary last_strand(strands.find(p)->second, BruteForceOrNot);
    pair<int, encoded_strand_binary> last_strand_pair(p, last_strand);
    encoded_strands.insert(last_strand_pair);
    /// add last bit as 1 from the last strand
    encoded_strands.find(p)->second.insertLastBit();

    ///  while we go through all the indexes
    for(int i = 0; i < strands.size(); i++){
        if(i == 34){
            int stop = 1;
        }
        /// (up)LM−1 = 1
        encoded_strands.find(p)->second.setLastBit(1);
        vector<tuple<int,int>> B;
        find_pair_to_be_fixed(strands, i, t, e, BruteForceOrNot, distanceMetric, B, encoded_strands);
        /// if the i'th strand dosent need to be fixed, B will be empty, and we go on to the next strand (we already encoded it
        /// with its original data indside find_pair_to_be_fixed function
        if(B.empty()){
            continue;
        }
        /// case the strand need to be fixed.
        tuple<int, int> current_i_j = B.front();
        vector<int> index_i_in_binary;
        vector<int> index_j_in_binary;
        int current_i = get<0>(current_i_j);
        int current_j = get<1>(current_i_j);

        /// crreate binary representation of the strand's indexes.
        decToBinaryWithSize(current_i, index_i_in_binary, index_length);
        decToBinaryWithSize(current_j, index_j_in_binary, index_length);

        /// this is for  (up)[0,log(M)] = ind_i
        encoded_strands.find(p)->second.setNextNodeInList(index_i_in_binary);
        p = i;

        vector<vector<int>> data_of_potential_strands;
        vector<int> w_l;
        vector<int> delta_1_binary;
        vector<int> delta_2_binary;
        int N = 0;
        /// calc s_e_i
        S_e_i(
                strands, e, current_i, distanceMetric, data_of_potential_strands,
                encoded_strands, index_length, N);

        if (BruteForceOrNot) {

            W_l_S_t_BruteForce(data_of_potential_strands, t, w_l, distanceMetric,
                    N, index_length);
        }
        else {
            W_l_S_t_NoBruteForce(data_of_potential_strands, t, w_l, distanceMetric,
                    N, index_length);
        }

        /// creating delta1
        create_delta_1(index_i_in_binary, index_j_in_binary, delta_1_binary, e, M );
        /// in case j has been encoded already (that actually applies only if j is the last strand),
        /// because otherwise he should maintain the constraint with every strand i.
        /// we need to retrive its data from the encoded strands and call delta2 with its encoded version
        /// other wise we will call it with its original version.
        auto encoded_version = encoded_strands.find(current_j);
        if(encoded_version != encoded_strands.end()){
            create_delta_2(strands.find(current_i)->second, encoded_strands.find(current_j)->second.get_encoded_data(),
                            M, strands_data_length, t, delta_2_binary);
        }
        /// case j'th strand hasent been encoded yet
        else {
            create_delta_2(strands.find(current_i)->second, strands.find(current_j)->second,
                           M, strands_data_length, t, delta_2_binary);
        }
        /// creating the encoded strand a.k.a repl vector
        vector<int> repl_vector;
        createReplVector(w_l, delta_1_binary, delta_2_binary, repl_vector, strands_data_length, index_length);
        /** insert the encoded version to the encoded strands data structure
         just to notify, only on next iteration it will be fully encoded, since its first LogM bits
         will be updated to be the index of the next strand that need to be fixed. **/
         addEncodedVersion(repl_vector, strands.find(i)->second, current_i, index_length, encoded_strands, BruteForceOrNot);
    }
    /// last bit of last node in the list is 0
    encoded_strands.find(p)->second.setLastBit(0);

    /// the first logM bits of the last node in the list holds the first logM bits of the last strand in the system
    vector<int> first_logM_bits_of_last_strand{strands.find(M - 1)->second.begin(),
                                               strands.find(M - 1)->second.begin() + index_length};
    encoded_strands.find(p)->second.setNextNodeInList(first_logM_bits_of_last_strand);

}








#endif //CLUSTERING_CORRECTING_CODES_PROJECT_ENCODING_ALGORITHIM_H



