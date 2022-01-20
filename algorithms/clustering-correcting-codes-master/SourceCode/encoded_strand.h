//
// Created by amitw on 06/12/2019.
//

#ifndef CLUSTERING_CORRECTING_CODES_PROJECT_ENCODED_STRAND_H
#define CLUSTERING_CORRECTING_CODES_PROJECT_ENCODED_STRAND_H

#include "strand.h"


using namespace std;







/*!
 * this class is representing the encoded strand's data containing all the relevant parts of the the encoded data
 * encoded_related_to_index - the index of the strand that the encoding was done in relation to.
 * delta_1 - the positions  that the indexes differ, (base 10).
 * delta_2 - the positions that the data differ, (base 10).
 * w_l - same as explained in the paper (the vector that make sure we hold the constraint).
 * last_bit - the last bit of the strand.
 * if_not_encoded - in case the strand is not suppose to be encoded, this field will contain the uncoded strand.
 */
class encoded_strand{
    vector<int> index_of_next_node_in_list;
    vector<int> delta_1;
    vector<int> delta_2;
    vector<int> w_l;
    vector<int> delta_1_padding;
    vector<int> delta_2_padding;
    vector<int> out_of_repl_padding;
    int last_bit;
    bool is_encoded;
    int my_index;
    vector<int> data_if_not_encoded;


public:
    encoded_strand(
            int index,
            vector<int> data){

        last_bit = -1;
        is_encoded = false;
        my_index = index;
        data_if_not_encoded = data;



    }
    encoded_strand(
            vector<int>& delta_one,
            vector<int>& delta_two,
            vector<int>& w_L,
            int index):

    delta_1(delta_one), delta_2(delta_two), w_l(w_L){
        last_bit =1;
        is_encoded = true;
        my_index = index;


    }

    const vector<int> &getNextNodeInList() const {
        return index_of_next_node_in_list;
    }

    void setNextNodeInList(const vector<int> &encodedRelatedToIndex) {
        index_of_next_node_in_list = encodedRelatedToIndex;
    }

    const vector<int> &getDelta1() const {
        return delta_1;
    }

    void setDelta1(const vector<int> &delta1) {
        delta_1 = delta1;
    }

    int getIndex(){
        return my_index;
    }


    const vector<int> &getDelta2() const {
        return delta_2;
    }

    void setDelta2(const vector<int> &delta2) {
        delta_2 = delta2;
    }

    const vector<int> &getWL() const {
        return w_l;
    }

    void setWL(const vector<int> &wL) {
        w_l = wL;
    }

    int getLastBit() const {
        return last_bit;
    }

    void setLastBit(int lastBit) {
        last_bit = lastBit;
    }

    int getIsEncoded()  {
        return is_encoded;
    }

    void setIsEncoded(bool ifNotEncoded_index) {
        is_encoded = ifNotEncoded_index;
    }
    vector<int> getDataIfNotEncoded(){
        return data_if_not_encoded;
    }


/*!
 * function that creates a binary vector from the given delta_1 vector which holds the positions the index differ
 * but in ints and not in binary representation, also we create padding if needed in the delta_1_binary vector, and as well
 * fill the given padding vector
 * @param delta_1 - the given int vector
 * @param strands_num - number of strands in the system
 * @param e - the distance constraintin the index
 * @param padding - the output padding vector
 * @param delta_1_binary - the output delta_1 in binary
 */
    void createBinaryVectorFromDelta1(
            vector<int>& delta_1,
            int strands_num,
            int e,
            vector<int>& padding,
            vector<int>& delta_1_binary){

        /// delta_1 size should be e * log(log(M))
        int delta_1_size = ceil(log2(ceil(log2(strands_num)))) * e;
        int index_position_length = ceil(log2(ceil(log2(strands_num))));
        for(int i = 0; i < delta_1.size(); i++){
            vector<int> current_position_binary;
            decToBinaryWithSize(delta_1[i], current_position_binary, index_position_length);
            delta_1_binary.insert(delta_1_binary.end(), current_position_binary.begin(), current_position_binary.end());
        }
        /// we do padding of the last position untill we get to the size we wanted
        while(delta_1_binary.size() != delta_1_size){
            vector<int> last_position_binary;
            decToBinaryWithSize(delta_1.back(), last_position_binary, index_position_length);
            delta_1_binary.insert(delta_1_binary.end(), last_position_binary.begin(), last_position_binary.end());
            padding.insert(padding.end(), last_position_binary.begin(), last_position_binary.end());

        }
    }

/*!
 * function that creates a binary vector from the given delta_2 vector which holds the positions the data differ
 * but in ints and not in binary representation, also we create padding if needed in the delta_2_binary vector, and as well
 * fill the given padding vector (just remember there are two options for padding in delta2).
 * @param delta_2 - the given int vector
 * @param strands_num - number of strands in the system
 * @param t - the distance constraintin the data
 * @param padding - the output padding vector
 * @param strands_length - the length of the strands in the system (L).
 * @param delta_2_binary - the output delta_1 in binary
 */
    void createBinaryVectorFromDelta2(vector<int> delta_2,
            int strands_num,
            int strands_length,
            int t,
            vector<int>& padding,
            vector<int>& delta_2_binary){




    /*!
     * function for creating one binary vector from the encoded vector, adding padding if needed (repl and out of repl)
     * if the strand is the last strand in the system the mechanisim is diffrent, as well if he hasent been fixed.
     * @param binary_vector - the output vector
     * @param strands_num - number of strands in the system
     * @param strands_length - length of strands in the system
     * @param e - distance constraint in the index
     * @param t - distance constraint in the data
     */
    void createOneBinaryVectorFromEncodedData(
            vector<int>& binary_vector,
            int strands_num,
            int strand_data_length,
            int e,
            int t) {

        /// if its the last strand
        if(my_index == strands_num - 1){
           binary_vector = data_if_not_encoded;
           if(index_of_next_node_in_list.empty()){
               return;
           }
           for(int i = 0; i < ceil(log2(strands_num)); i++){
               binary_vector[i] = index_of_next_node_in_list[i];
           }
           return;
        }
        /// if the strand hasent been fixed its encoded data is the original data
        if(is_encoded == false){
            binary_vector = data_if_not_encoded;
            return;
        }
         vector<int> delta_1_binary;
         vector<int> delta_2_binary;
         createBinaryVectorFromDelta1(delta_1, strands_num,  e, delta_1_padding, delta_1_binary);
         createBinaryVectorFromDelta2( delta_2, strands_num, strand_data_length, t, delta_2_padding, delta_2_binary);
         /// concatinating the data : next_node, w_l, delta1, delta2, out_of_repl_padding, last_bit
         binary_vector.insert(binary_vector.end(), index_of_next_node_in_list.begin(), index_of_next_node_in_list.end());
         binary_vector.insert(binary_vector.end(), w_l.begin(), w_l.end());
         binary_vector.insert(binary_vector.end(), delta_1_binary.begin(), delta_1_binary.end());
         binary_vector.insert(binary_vector.end(), delta_2_binary.begin(), delta_2_binary.end());
         /// add out of repl padding
         while(binary_vector.size() != strand_data_length - 1){
             binary_vector.push_back(0);
             out_of_repl_padding.push_back(0);
         }
        binary_vector.push_back(last_bit);


    }

};




#endif //CLUSTERING_CORRECTING_CODES_PROJECT_ENCODED_STRAND_H
