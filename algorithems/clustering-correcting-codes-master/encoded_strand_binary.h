//
// Created by amitw on 18/01/2020.
//

#ifndef CLUSTERING_CORRECTING_CODES_PROJECT_ENCODED_STRAND_BINARY_H
#define CLUSTERING_CORRECTING_CODES_PROJECT_ENCODED_STRAND_BINARY_H
#include "strand.h"
class encoded_strand_binary {
    vector<int> encoded_data;
    bool brute_force;
public:
    encoded_strand_binary(vector<int> data, bool brute): encoded_data(data), brute_force(brute){};

    vector<int>& get_encoded_data(){
        return encoded_data;
    }

    /// sets the last bit of the encoded data to 1.
    void setLastBit(int val){
        encoded_data.back() = val;
    }

    /// assign the first LogM bits of the encoded data to be the next node in the list of encoding.
    void setNextNodeInList(vector<int> index_in_binary){
        for(int i = 0; i < index_in_binary.size(); i++){
            encoded_data[i] = index_in_binary[i];
        }
    }

    /// gets last bit of the encoded data
    int getLastBit(){
        return encoded_data.back();
    }

    /*!
     * get the first logM bits of the data
     * @param first_LogM_bits - output
     * @param index_length - length of the index in binary (ceil(LogM))
     */
    void getFirstLogMBits(
            vector<int>& first_LogM_bits,
            int index_length){

            first_LogM_bits.insert(first_LogM_bits.begin(), encoded_data.begin(), encoded_data.begin() + index_length);
    }
    /*!
     * sets the given vector as the first logM bits of the encoded data
     * @param first_logM_bits - the vector we set as the first logM bits
     */
    void setfirstLogMBits(vector<int>& first_logM_bits){
        for(int i = 0; i < first_logM_bits.size(); i++){
            encoded_data[i] = first_logM_bits[i];
        }
    }
    void insertLastBit(){
        encoded_data.push_back(1);
    }

    /*!
     * set new encoded data
     * @param new_encoded_data - new encoded data to be set.
     */
    void setEncodedData(vector<int> new_encoded_data){
        encoded_data = new_encoded_data;
    }

    /*!
     * takes the first logM bits, convert it to int and returns it.
     * @param index_length - length of the index in binary (ceil(LogM))
     * @return - the index of the next strand in the encoding list.
     */
    int getNextNodeIndex(int index_length){
        vector<int> first_LogM_bits;
        getFirstLogMBits(first_LogM_bits, index_length);
        return binaryToDec(first_LogM_bits);
    }




/*!
 * function for calculating for a given encoded strand its w_l size, it depends if he was encoded in brute force manner
 * or not, 3t * 2ceil(log(N+1)) for brute, and t * ceil(log(N+1)) without brute force.
 * we will calculate N w.r.t the given e,t and M . (N = | { x is a binary number | dH(x, index) <= e} | )
 * @param M - number of strands in the system
 * @param e - index distance constraint
 * @param t - data distance constraint
 * @param index - index of the strand we're calculating its w_l size.
 * @param distanceMetric - the distance metric we're using
 * @return integer representing w_l's size.
 */
    int calculate_wl_size(
            int M,
            int e,
            int t,
            int index,
            int (*distanceMetric)(vector<int>, vector<int>)){

        // calculate N
        int index_length = ceil(log2(M));
        vector<int> index_binary_representation;
        decToBinaryWithSize(index, index_binary_representation, index_length);
        set<vector<int>> relevant_indexes;
        set<vector<int>> output_indexes;
        set<vector<int>> union_of_all;
        distanceByOne(index_binary_representation, relevant_indexes, distanceMetric);
        union_of_all = relevant_indexes;
        int count_till_e = 1;
        count_till_e++;
        while(count_till_e <= e){
            distanceByOneFromSet(relevant_indexes, output_indexes, distanceMetric);
            relevant_indexes = output_indexes;
            union_of_all.insert(output_indexes.begin(), output_indexes.end());
            count_till_e++;
        }
        for(auto it = union_of_all.begin(); it != union_of_all.end(); it++){
            if(*it == index_binary_representation){
                union_of_all.erase(it);
            }
        }
        int N = union_of_all.size();
        // brute force
        if(brute_force){
            return 3 * t +  2 * ceil(log2(N + 1));
        }
        // no brute force
        else return t * ceil(log2(N + 1));

    }

    /*!
    * function for extracting delta1 part from the encoded strand (delta_1 size = e * ceil(log(log(M)))
    * @param delta_1_from_encoded_data - the output delta1 part
    * @param M - number of strands in the system
    * @param e - index distance constraint
    * @param t - data distance constraint
    * @param index - index of the strand we're calculating its w_l size.
    * @param distanceMetric - the distance metric we're using
     */
    void getDelta1FromEncodedData(
            vector<int>& delta_1_from_encoded_data,
            int M,
            int e,
            int t,
            int index,
            int (*distanceMetric)(vector<int>, vector<int>)){
        /// in case brute force == true, w_l = 3t + 2*log(N+1)
        int w_l_size = calculate_wl_size(M, e, t, index, distanceMetric);
        int index_length = ceil(log2(M));
        int delta_1_size = ceil(log2(index_length)) * e;
        vector<int> output{encoded_data.begin() + w_l_size + index_length,
                           encoded_data.begin() + w_l_size + index_length + delta_1_size};
        delta_1_from_encoded_data = output;
    }
    /*!
     * function that recives delta 1 in binary representation, and convert it to a vector of positions as ints
     * @param positions_as_ints - the output set, each element represent a position encoded in delta1,
     * i made it a set because of the padding, i dont want the same position repeat in the output.
     * @param delta1 - the given delta 1 binary vector
     * @param position_length - length of one position's binary representation.
     */
    void convertDelta1ToInt(
            set<int>& positions_as_ints,
            vector<int>& delta1,
            int position_length){

        for(int i = 0; i < delta1.size(); i += position_length){
            vector<int> curr_binary_position{delta1.begin() + i, delta1.begin() + i + position_length};
            int curr_position = binaryToDec(curr_binary_position);
            positions_as_ints.insert(curr_position);
        }
    }

    /*!
      * function for extracting delta2 part from the encoded strand (delta_1 size = (t-1) * ceil(log(L - M)))
      * @param delta_2_from_encoded_data - the output delta1 part
      * @param M - number of strands in the system
      * @param e - index distance constraint
      * @param t - data distance constraint
      * @param index - index of the strand we're calculating its w_l size.
      * @param distanceMetric - the distance metric we're using
       */
    void getDelta2FromEncodedData(
            vector<int>& delta_2_from_encoded_data,
            int M,
            int e,
            int t,
            int index,
            int (*distanceMetric)(vector<int>, vector<int>)){

        /// in case brute force == true, w_l = 3t + 2*logN
        int w_l_size = calculate_wl_size(M, e, t, index, distanceMetric);
        int index_length = ceil(log2(M));
        int delta_1_size = ceil(log2(index_length)) * e;
        int delta_2_size = ceil(log2(encoded_data.size())) * (t - 1);
        vector<int> output{encoded_data.begin() + w_l_size + index_length + delta_1_size
                           ,encoded_data.begin() + w_l_size + index_length + delta_1_size + delta_2_size};
        delta_2_from_encoded_data = output;
    }

    /*!
  * function that recives delta 2 in binary representation, and convert it to a vector of positions as ints
    in case delta2 holds position in unordered way, means the data of the instance strand is identical to the data
     of the strand the intstance strand was encoded by, therefore positions_as_ints will be empty to denote that.
  * @param positions_as_ints - the output set, each element represent a position encoded in delta1,
  * i made it a set because of the padding, i dont want the same position repeat in the output.
  * @param delta1 - the given delta 1 binary vector
  * @param position_length - length of one position's binary representation.
  */
    void convertDelta2ToInt(
            set<int>& positions_as_ints,
            vector<int>& delta2,
            int position_length){

        int last_position = -1; // helper val to detect padding
        for(int i = 0; i < delta2.size(); i += position_length){
            vector<int> curr_binary_position{delta2.begin() + i, delta2.begin() + i + position_length};
            int curr_position = binaryToDec(curr_binary_position);
            /// unordered delta2 = identical
            if(curr_position < last_position){
                positions_as_ints.clear();
                return;
            }
            positions_as_ints.insert(curr_position);
            last_position = curr_position;
        }
    }

    bool getIfBruteForce(){
        return brute_force;
    }


};


#endif //CLUSTERING_CORRECTING_CODES_PROJECT_ENCODED_STRAND_BINARY_H
