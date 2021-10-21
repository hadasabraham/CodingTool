//
// Created by amitw on 18/01/2020.
//


#ifndef CLUSTERING_CORRECTING_CODES_PROJECT_FILES_H
#define CLUSTERING_CORRECTING_CODES_PROJECT_FILES_H
#include "strand.h"


/*!
 * check if a char is a binary num.
 * @param element
 * @return
 */
bool isBinaryNum(char element){
    return element == '0' || element == '1';
}

/*!
 * this function is responsible for parsing a binary file and create vector of vectors where every
 * vector is a strand, as well we calculate number of strands, the index and the data length and finally
 * add zero padding to the last vector if needed
 * @param L - length of a strand
 * @param path_to_file - path to the binary file
 * @param strands - the strands that have been parsed
 * @param M - number of strands created
 * @param padding_done - the amount of padding that has been done to the last strand, so we could recounstruct the file
 * we've parsed at the end of the run.
 * */
void readStrandsBinaryFie(
        int L,
        string path_to_file,
        vector<vector<char>>& strands,
        int& M,
        int& padding_done){

        ifstream file(path_to_file, std::ios::binary );
        assert(file.is_open());
        vector<unsigned char> buffer(istreambuf_iterator<char>(file), {});
        /// keep only binary numbers in the data
        auto it = buffer.begin();
        while(it != buffer.end()){
            if(*it != '0' && *it != '1'){
                it = buffer.erase(it);
            }
            else{
                it++;
            }
        }
        // calculating number of strands.
        M = buffer.size() / L + 1;
        int remaining = buffer.size() % L;
        int padding_num = L - remaining - 1;
        padding_done = padding_num;
        for(int i = 0; i < buffer.size(); i+=L) {
            int strand_size = L;
            if (i + strand_size > buffer.size()) {
                strand_size = L - (i + strand_size - buffer.size());
            }
            vector<char> strand;
            for (int j = 0; j < strand_size; j++) {

                strand.push_back(buffer[i + j]);
            }
            strands.push_back(strand);
        }
        /// add the padding to the last vector, in case no padding is needed, we add another strand size of L - 1
        /// denoted as the last strand in the system
        if(padding_num == L - 1){
            padding_done = padding_num;
            vector<char> last_strand;
            while(padding_num--){
                last_strand.push_back('0');
            }
            strands.push_back(last_strand);
        }
        else {
            while (padding_num--) {
                strands.back().push_back('0');
            }
        }
        file.close();

}

/*!
 * function that converting the vector of vectors of type char, where each vector is a strand to a map of strands
 * in the format that the encoding algorithim can handle
 * @param strands_vec - the vector of vectors, each vector is a strand
 * @param strands_map - the output map
 */
void convertToMapOfStrands(
        vector<vector<char>>& strands_vec,
        unordered_map<int, vector<int>>& strands_map){

        for(int i = 0; i < strands_vec.size(); i++){
            vector<int> strand_in_int;
            convertCharVecToIntVec(strands_vec[i], strand_in_int);
            /// insert the new strand to map
            strands_map[i] = strand_in_int;
        }
}
/*!
 * function that parse the strands data file and create input for the encoding algorithim (top level function)
 * @param path_to_file - path to the data binary file
 * @param L - given strand's length.
 * @param strands - the output strands.
 * @param padding - the amount of padding that has been done to the last strand, so we could recounstruct the file
 * we've parsed at the end of the run.
 */
void ParseDataToEncoding(
        string path_to_file,
        int L,
        unordered_map<int, vector<int>>& strands,
        int& padding){

        int M = 0, index_length = 0, data_length = 0;
        vector<vector<char>> strands_vec;
        readStrandsBinaryFie(L, path_to_file, strands_vec, M, padding);
        convertToMapOfStrands(strands_vec, strands);

}

/*!
 * helper function for converting unordered map to ordered map
 * @param encoded_strands - unordered map
 * @param new_map - map
 */
void convertUnorderedMapToMap(
        unordered_map<int, encoded_strand_binary>& encoded_strands,
        map<int, encoded_strand_binary>& new_map
){
    /// insert to sorted map so we can print in the order of the strands's indexes.
    for(auto it = encoded_strands.begin(); it != encoded_strands.end(); it++){
        pair<int, encoded_strand_binary> p(it->first, it->second);
        new_map.insert(p);
    }
}


/*!
 * helper function for converting unordered map to ordered map
 * @param encoded_strands - unordered map
 * @param new_map - map
 */
void convertUnorderedMapBeforeEncodingToMap(
        unordered_map<int, vector<int>>& encoded_strands,
        map<int, vector<int>>& new_map
){
    /// insert to sorted map so we can print in the order of the strands's indexes.
    for(auto it = encoded_strands.begin(); it != encoded_strands.end(); it++){
        pair<int, vector<int>> p(it->first, it->second);
        new_map.insert(p);
    }
}


/*!
 * function that take all the  strands, convert them to vector of chars and write them into a binary file.
 * @param path_to_file - path to file we're writing to
 * @param encoded_strands - the encoded strands we will export
 * @param padding - the amount of padding that has been done when reading the file for encoding
 */
void exportStrandsToFile(
        string path_to_file,
        map<int, encoded_strand_binary> encoded_strands,
        int padding)
{
        ofstream file(path_to_file, ios::binary);


        for(auto it = encoded_strands.begin(); it != encoded_strands.end(); it++){
            vector<char> strand_in_char;
            vector<int> strand_data = it->second.get_encoded_data();
            // convert it to char
            convertIntVecToCharVec(strand_in_char, strand_data);
            // write it into a file
            for(int i = 0; i < strand_in_char.size(); i++){
                file << strand_in_char[i];
            }
            file << '\n';
        }
//        while(padding--){
//           file << '0';
//        }
        file.close();
}

/*!
 * function that take all the  strands, convert them to vector of chars and write them into a binary file.
 * @param path_to_file - path to file we're writing to
 * @param encoded_strands - the encoded strands we will export
 * @param padding - the amount of padding that has been done when reading the file for encoding
 */
void exportStrandsBeforeEncodingToFile(
        string path_to_file,
        map<int, vector<int>> strands,
        int padding)
{
    ofstream file(path_to_file, ios::binary);


    for(auto it = strands.begin(); it != strands.end(); it++){
        vector<char> strand_in_char;
        vector<int> strand_data = it->second;
        // convert it to char
        convertIntVecToCharVec(strand_in_char, strand_data);
        // write it into a file
        for(int i = 0; i < strand_in_char.size(); i++){
            file << strand_in_char[i];
        }
        file << '\n';
    }
//        while(padding--){
//           file << '0';
//        }
    file.close();
}


void readEncodedStrandsBinaryFie(
        string path_to_file,
        vector<vector<char>>& strands,
        int L)
{
    ifstream file(path_to_file, std::ios::binary );
    assert(file.is_open());
    vector<unsigned char> buffer(istreambuf_iterator<char>(file), {});
    for(int i = 0; i < buffer.size(); i+=L) {
        int strand_size = L;
        vector<char> strand;
        for (int j = 0; j < strand_size; j++) {

            strand.push_back(buffer[i + j]);
        }
        strands.push_back(strand);
    }

}

/*!
 * function that converting the vector of vectors of type char, where each vector is a strand to a map of encoded
 * in the format that the encoding algorithim can handle
 * @param strands_vec - the vector of vectors, each vector is a strand
 * @param strands_map - the output encoded strands map
 * @param bruteForce - boolean denoting wether the w_l part of the encoded data was determined via brute force manner.
 */
void convertToMapOfEncodedStrands(
        vector<vector<char>>& strands_vec,
        unordered_map<int, encoded_strand_binary>& strands_map,
        bool bruteForce){

    for(int i = 0; i < strands_vec.size(); i++){
        vector<int> strand_in_int;
        convertCharVecToIntVec(strands_vec[i], strand_in_int);
        /// insert the new strand to map
        encoded_strand_binary encoded_strand(strand_in_int, bruteForce);
        pair<int, encoded_strand_binary> pair(i, encoded_strand);
        strands_map.insert(pair);
    }
}



/*!
 * function that parse the strands data file and create input for the Decoding algorithim (top level function)
 * @param path_to_file - path to the data binary file
 * @param L - given strand's length.
 * @param encoeded_strands - the output strands.
 * @param bruteForce -  boolean denoting wether the w_l part of the encoded data was determined via brute force manner.
 */
void ParseDataToDecoding(
        string path_to_file,
        int L,
        unordered_map<int, encoded_strand_binary>& encoeded_strands,
        bool bruteForce){

    vector<vector<char>> strands_vec;
    readEncodedStrandsBinaryFie(path_to_file, strands_vec, L);
    convertToMapOfEncodedStrands(strands_vec, encoeded_strands, bruteForce);


}



#endif //CLUSTERING_CORRECTING_CODES_PROJECT_FILES_H
