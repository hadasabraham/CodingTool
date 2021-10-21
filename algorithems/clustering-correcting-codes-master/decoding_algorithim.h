//
// Created by amitw on 30/12/2019.
//

#ifndef CLUSTERING_CORRECTING_CODES_PROJECT_DECODING_ALGORITHIM_H
#define CLUSTERING_CORRECTING_CODES_PROJECT_DECODING_ALGORITHIM_H

#include <fstream>
#include "encoding_algorithim.h"
//
// Created by Amit Weil on 30/12/2019.
//

/*!
 * this function will recive all the encoded strands and start from the last strand going up the list of encoding order
 * and create a vector that contains the list of encoding order in reverse order, such that it will be the decoding order.
 * @param encoded_strands - the encoded strands in the system
 * @param order_of_decoding - output vector, the indexes s.t we should decode in the vector's order.

 */
void createDecodingOrderList(
        unordered_map<int, encoded_strand_binary>& encoded_strands,
        vector<int>& order_of_decoding){

    int last_strand_index = encoded_strands.size() - 1;
    int current_node_in_list = last_strand_index;
    int index_length = ceil(log2(encoded_strands.size()));

    /// we start to going up in the list untill we reach someone that its last bit is 0
    while(true){
        auto iterator = encoded_strands.find(current_node_in_list);
        // means we found the end of the list.
        if(iterator->second.getLastBit() == 0){
            order_of_decoding.push_back(current_node_in_list);
            break;
        }
        else{
            order_of_decoding.push_back(current_node_in_list);
            current_node_in_list = iterator->second.getNextNodeIndex(index_length);
            continue;
        }
    }
    /// we reverse it because that in the decoding order we start from the end to the beginning.
    reverse(order_of_decoding.begin(), order_of_decoding.end());

}

/*!
 * function for us to know by which strand a given encoded strand was encoded by,
 * we know that by inversing the bits of the given strand in the positions found in
 * delta1 part of the encoded data of the given strand.
 * @param - encoded_strand - the strand we decode.
 * @param encoded_strand_index - the index of the strand we decode.
 * @param strand_num_in_system - the number of strands in the system.
 * @param e - index distance constraint
 * @param t - data distance constraint
 * @param distanceMetric - the distance metric we're using
 * @return - the decoded index as an int.
 */
int DecodeIndex(
        encoded_strand_binary& encoded_strand,
        int encoded_strand_index,
        int strand_num_in_system,
        int e,
        int t,
        int (*distanceMetric)(vector<int>, vector<int>)){


    int index_length = ceil(log2(strand_num_in_system));
    int position_length = ceil(log2(ceil(log2(strand_num_in_system))));
    vector<int> delta_1_binary;
    set<int> positions_as_ints;
    vector<int> encoded_strand_index_binary;
    encoded_strand.getDelta1FromEncodedData(delta_1_binary, strand_num_in_system, e, t, encoded_strand_index, HammingDistance);
    encoded_strand.convertDelta1ToInt(positions_as_ints, delta_1_binary, position_length);
    decToBinaryWithSize(encoded_strand_index, encoded_strand_index_binary, index_length);

    for(auto it = positions_as_ints.begin(); it != positions_as_ints.end(); it++){
        encoded_strand_index_binary[*it] = (encoded_strand_index_binary[*it] + 1) % 2;
    }
    return binaryToDec(encoded_strand_index_binary);

}

/*!
 * function for decoding a given encoded strand data by its delta2 part, just switch the bits in the encoded_by_data,
 * in the positions encoded in delta2 part of the encoded data.
 * @param decode - the strand we decode its data
 * @param encoded_by_data - the data of the strand the given strand was encoded by
 * @param encoded_strand_index - the index of the strand we decode.
 * @param strand_num_in_system - the number of strands in the system.
 * @param strand_data_length - the length of strand's data (L)
 * @param e - index distance constraint
 * @param t - data distance constraint
 * @param distanceMetric - the distance metric we're using
 */
void DecodeData(
        encoded_strand_binary& decode,
        vector<int> encoded_by_data,
        int encoded_strand_index,
        int strand_num_in_system,
        int strand_data_length,
        int e,
        int t,
        int (*distanceMetric)(vector<int>, vector<int>)){

    int position_length = ceil(log2(strand_data_length));
    vector<int> delta_2_binary;
    set<int> positions_as_ints;

    decode.getDelta2FromEncodedData(delta_2_binary, strand_num_in_system, e, t, encoded_strand_index, HammingDistance);
    decode.convertDelta2ToInt(positions_as_ints, delta_2_binary, position_length);
    if(positions_as_ints.empty()) {
        /// denoting that decode's data and encoded by data are identical, so we just assign the data
        decode.setEncodedData(encoded_by_data);
        return;
    }
    decode.setEncodedData(encoded_by_data);
    /// switch bits in the positions encoded in delta2.
    for(auto it = positions_as_ints.begin(); it != positions_as_ints.end(); it++){
        decode.get_encoded_data()[*it] = (encoded_by_data[*it] + 1) % 2;
    }

}






/*!
 * the decoding algorithim, we go through the decoding order list and decode each strand by its delta1 and delta2.
 * @param encoded_strands - the encoded strands, in the end of the algorithim this data structure will hold all the
 * decoded strands
 * @param strand_data_length - length of strand's data (L).
 * @param e - index distance constraint
 * @param t - data distance constraint
 * @param distanceMetric - the distance metric we're using
 */

void DecodingAlgorithim(
        unordered_map<int, encoded_strand_binary>& encoded_strands,
        int strand_data_length,
        int e,
        int t,
        int (*distanceMetric)(vector<int>, vector<int>)){

    /// for test manners:
    if(encoded_strands.empty()){
        return;
    }
    int index_legnth = ceil(log2(encoded_strands.size()));
    int strand_num_in_system = encoded_strands.size();
    /**in case no strand has been encoded no decoding need to be done, and the last bit of the last strand
     * denotes that, just return
    **/
    if(encoded_strands.find(strand_num_in_system - 1)->second.getLastBit() == 0){
        /// pop the last bit of the last strand (redundancy bit)
        encoded_strands.find(encoded_strands.size() - 1)->second.get_encoded_data().pop_back();
        return;
    }

    /// create the decoding order list
    vector<int> decoding_order_list;
    createDecodingOrderList(encoded_strands, decoding_order_list);

    /// first we take the first LogM bits of the last strand in the list and put it as the first LogM bits of the last strand.
    vector<int> last_strand_first_logM_bits;
    auto current_encoded_strand = encoded_strands.find(decoding_order_list[0]);
    current_encoded_strand->second.getFirstLogMBits(last_strand_first_logM_bits, index_legnth);
    auto last_strand = encoded_strands.find(strand_num_in_system - 1);
    last_strand->second.setfirstLogMBits(last_strand_first_logM_bits);

    /// start encoding the strands in the order denoted in the decoding orderl ist.
    for(int i = 0; i < decoding_order_list.size() - 1; i++){
        /// if we're not in the first  node in the decoding order list
            auto current_encoded_strand = encoded_strands.find(decoding_order_list[i]);
            // 1. we find out by which strand the current encoded strand was encoded by, by inversing its index in the delta1 positions
            int encoded_by_index = DecodeIndex(current_encoded_strand->second,
                    current_encoded_strand->first, strand_num_in_system, e, t, HammingDistance);
            // 2. we decode the current strand data by the data of the strand we just found its index.
            auto encoded_by_strand = encoded_strands.find(encoded_by_index);
            DecodeData(current_encoded_strand->second, encoded_by_strand->second.get_encoded_data(),
                    current_encoded_strand->first, strand_num_in_system, strand_data_length, e, t, HammingDistance);
            vector<int> decoded_data;

    }
    /// pop the last bit of the last strand (redundancy bit)
    encoded_strands.find(encoded_strands.size() - 1)->second.get_encoded_data().pop_back();
}



#endif //CLUSTERING_CORRECTING_CODES_PROJECT_DECODING_ALGORITHIM_H


