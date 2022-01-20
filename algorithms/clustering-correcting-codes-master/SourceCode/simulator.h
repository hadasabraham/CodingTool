
//
// Created by  Elon Grubman on 21/01/2020.
//

#ifndef CLUSTERING_CORRECTING_CODES_SIMULATOR_H
#define CLUSTERING_CORRECTING_CODES_SIMULATOR_H

#include "encoded_strand_binary.h"
#include "clusterAfterSimulation.h"


#define MIN_LIM 100
#define MAX_LIM 1000

using namespace std;

class simulator;
void duplicateStrandAndInsertToVec(simulator* simulator, unordered_map<int,clusterAfterSimulation>& map, vector<int>& encoded_data,
        vector<vector<duplicateStrandWiteErrors>>& strands_duplicates, int orig_index, int encoded_strands_map_size);
void collectAllStrandToClusters(vector<vector<duplicateStrandWiteErrors>>& strands_duplicates, unordered_map<int,clusterAfterSimulation>& map, unordered_map<int,encoded_strand_binary>& _map);
void makeClusterMatchToAssumptiom(clusterAfterSimulation& cluster, unordered_map<int,clusterAfterSimulation>& map, int cluster_index,
        int orig_strands_map_size, string assum, vector<int>& original_strand);



class simulator {
    unordered_map<int,clusterAfterSimulation> map;
    string assumption;
    int tao;
    int ro;
    int e;
    int t;

public:
    simulator(int _tao, int _ro, int _e, int _t, unordered_map<int,encoded_strand_binary>& _map, string _assumption) :
    tao(_tao), ro(_ro), e(_e), t(_t), assumption(_assumption){
        int encoded_strands_map_size = _map.size();
        vector<vector<duplicateStrandWiteErrors>> strands_duplicates;
        for (int i = 0; i < encoded_strands_map_size; ++i) {
            auto it = _map.find(i);
            if(it == _map.end()){
                cout << "Simulator C'tor:: the system can't find the key " << i << " in map" << endl;
            }
            else{
                vector<int> encoded_data = it->second.get_encoded_data();
                /// create duplicates from original encoded strand that received and push them to strands_duplicates vector
                duplicateStrandAndInsertToVec(this, map, encoded_data, strands_duplicates, i, encoded_strands_map_size);
            }
        }

        collectAllStrandToClusters(strands_duplicates, map, _map);

        if( e >= 2*tao){
            for (int i = 0; i < map.size(); ++i) {
                auto clusters_it = map.find(i);
                auto it = _map.find(i);
                vector<int> original_strand = it->second.get_encoded_data();
                makeClusterMatchToAssumptiom(clusters_it->second, map, i, encoded_strands_map_size, "D", original_strand);
            }
        }
        else if(2*tao > e && e >= tao){
            for (int i = 0; i < map.size(); ++i) {
                auto clusters_it = map.find(i);
                auto it = _map.find(i);
                vector<int> original_strand = it->second.get_encoded_data();
                makeClusterMatchToAssumptiom(clusters_it->second, map, i, encoded_strands_map_size, "M", original_strand);
            }
        }
    }

    unordered_map<int,clusterAfterSimulation>& getMap()  {
        return map;
    }

    void setMap(unordered_map<int,clusterAfterSimulation>& map) {
        this->map = map;
    }

    string &getAssumption()  {
        return assumption;
    }

    int getTao()  {
        return tao;
    }

    void setTao(int tao) {
        this->tao = tao;
    }

    int getRo()  {
        return ro;
    }

    void setRo(int ro) {
        this->ro = ro;
    }
};

/*!
 * finction who get original index of strand by integer and convert it to binary vector
 * @param index_vec - binary vector that represent the original integer index
 * @param orig_index - original index of strand by integer
 * @param encoded_strands_map_size - number of original strands. MAX index.
 */
void converOrigIndexToBinaryVector(vector<int>& index_vec, int orig_index, int encoded_strands_map_size){
    decToBinary(orig_index, index_vec);
    if(index_vec.size() < log2(encoded_strands_map_size)){
        int delta = log2(encoded_strands_map_size) - index_vec.size();
        for (int i = 0; i < delta; ++i) {
            auto it = index_vec.begin();
            index_vec.insert(it, 0);
        }
    }
}

/*!
 * function who get some vector and creates another vector with errors according to received vector
 * @param number_of_errors - the number of errors that we confirm to make in the received vector
 * @param indexes - hash table of indexes that helps to function's logic
 * @param orig_vector - original received vector
 * @param generated_vector - created vector with errors
 */
void generateErrorsIntoVector(int number_of_errors, unordered_map<int,int>& indexes, vector<int>& orig_vector, vector<int>& generated_vector){
    while (number_of_errors > 0){
        int num = (rand() % orig_vector.size());
        auto it = indexes.find(num);
        if(it == indexes.end()){
            indexes[num] = 1;
            number_of_errors--;
        }
    }
    for (auto i = 0; i < orig_vector.size() ; ++i) {
        auto it = indexes.find(i);
        if(it != indexes.end()){
            if(orig_vector[i]==1) generated_vector.push_back(0);
            else generated_vector.push_back(1);
        }
        else{
            generated_vector.push_back(orig_vector[i]);
        }
    }
}

/*!
 * function who generate vector with error regarding to encoded_data vector
 * @param encoded_data - the vector that the function generated by him
 * @param encoded_data_with_errors - vector with duplicates strands with errors in index and in data
 * @param number_of_errors_in_index - the number of errors that we confirm to do in the index
 * @param number_of_errors_in_data - the number of errors that we confirm to do in the data
 * @param orig_index - original index of strand by integer
 * @param encoded_strands_map_size - number of original strands. MAX index.
 */
void makeErrors(vector<int>& encoded_data, vector<duplicateStrandWiteErrors>& encoded_data_with_errors, int number_of_errors_in_index,
        int number_of_errors_in_data, int orig_index, int encoded_strands_map_size){

    unordered_map<int,int> indexes;
    vector<int> index_vec;
    converOrigIndexToBinaryVector(index_vec, orig_index, encoded_strands_map_size);

    vector<int> index_with_errors;
    generateErrorsIntoVector(number_of_errors_in_index, indexes, index_vec, index_with_errors);

    int duplicate_strand_index_in_dec = binaryToDec(index_with_errors);
    duplicateStrandWiteErrors strand_with_errors(duplicate_strand_index_in_dec, encoded_data, orig_index, encoded_data);

    indexes.clear();
    vector<int> data_with_errors;
    generateErrorsIntoVector(number_of_errors_in_data, indexes, encoded_data, data_with_errors);
    strand_with_errors.setDataAfterSimulation(data_with_errors);
    encoded_data_with_errors.push_back(strand_with_errors);
}

/*!
 * function who original strand, duplicate him 100-10000 times with errors according to constraints and push the duplicates into vector
 * @param simulator - pointer to simulator type
 * @param map - hash table of clusters
 * @param encoded_data - the original vector the this function duplicates by him
 * @param strands_duplicates - the target vector for all the duplicates strands
 * @param orig_index - original index of strand by integer
 * @param encoded_strand_map_size - number of original strands in the system
 */
void duplicateStrandAndInsertToVec(simulator* simulator, unordered_map<int,clusterAfterSimulation>& map, vector<int>& encoded_data,
     vector<vector<duplicateStrandWiteErrors>>& strands_duplicates, int orig_index, int encoded_strand_map_size){

    int number_of_duplicates = MIN_LIM + (rand()%(MAX_LIM-MIN_LIM));
    vector<duplicateStrandWiteErrors> duplicates_for_current_strand;

    for (int i = 0; i < number_of_duplicates; ++i) {
        int number_of_errors_in_index = rand() % (simulator->getTao()+1);
        int number_of_errors_in_data = rand() % (simulator->getRo()+1);
        makeErrors(encoded_data, duplicates_for_current_strand, number_of_errors_in_index, number_of_errors_in_data, orig_index, encoded_strand_map_size);
    }
    strands_duplicates.push_back(duplicates_for_current_strand);

}

/*!
 * function who collect strands by them simulated index from all the strands duplicate and make clusters from strands with same simulated index
 * @param strands_duplicates - all the duplications strands from all the original strands
 * @param map - hash table that contain the clusters
 * @param _map - hash table that contain the original strands
 */
void collectAllStrandToClusters(vector<vector<duplicateStrandWiteErrors>>& strands_duplicates, unordered_map<int,clusterAfterSimulation>& map,
        unordered_map<int,encoded_strand_binary>& _map){

    int number_of_clusters = _map.size();
    for (int i = 0; i < number_of_clusters; ++i) {
        vector<duplicateStrandWiteErrors> strands_to_current_cluster;
        for (int j = 0; j < strands_duplicates.size(); ++j) {
            for (int k = 0; k < strands_duplicates[j].size(); ++k) {
                if( strands_duplicates[j][k].getIndexAfterSimulation() == i ){
                    strands_to_current_cluster.push_back(strands_duplicates[j][k]);
                }
            }
        }
        vector<char> empty_vec;
        clusterAfterSimulation currentCluster(strands_to_current_cluster, empty_vec);
        pair<int,clusterAfterSimulation> cluster_to_insert(i, currentCluster);
        map.insert(cluster_to_insert);
    }
}

/*!
 * function who take some cluster and make him match to the assumption on the strands in all clusters
 * @param cluster - the cluster that the function fixed now
 * @param map - hash table of clusters
 * @param cluster_index - the index of current cluster
 * @param orig_strands_map_size - the number of original strands in the system
 * @param assum - the assumptiom to fix by
 * @param original_strand - the original strand that match to the current cluster befor the simularion
 */
void makeClusterMatchToAssumptiom(clusterAfterSimulation& cluster, unordered_map<int,clusterAfterSimulation>& map,
        int cluster_index, int orig_strands_map_size, string assum, vector<int>& original_strand){
    if(assum == "D"){
        int max_orig_index = 0;
        int size_of_orig_strand_to_this_cluster = 0;
        for (int i = 0; i < orig_strands_map_size; ++i) {
            auto origIndexesAmount_it = cluster.getOrigIndexesAmount().find(i);
            if( origIndexesAmount_it != cluster.getOrigIndexesAmount().end()){
                if( max_orig_index < origIndexesAmount_it->second) max_orig_index = origIndexesAmount_it->second;
                if( origIndexesAmount_it->first == cluster_index ) size_of_orig_strand_to_this_cluster = origIndexesAmount_it->second;
            }
        }
        int delta = max_orig_index - size_of_orig_strand_to_this_cluster;
        vector<duplicateStrandWiteErrors> current_cluster_strands = cluster.getDuplicateStrands();

        for (int j = 0; j < delta+1; ++j) {
            duplicateStrandWiteErrors duplicate_to_insert(cluster_index, original_strand, cluster_index, original_strand);
            current_cluster_strands.push_back(duplicate_to_insert);
        }
        cluster.setDuplicateStrands(current_cluster_strands);
    }
    else if(assum == "M"){
        int size_of_orig_strand_to_this_cluster = 0;
        auto it = cluster.getOrigIndexesAmount().find(cluster_index);
        if( it != cluster.getOrigIndexesAmount().end()){
            size_of_orig_strand_to_this_cluster = it->second;
        }
        int halfAmount = cluster.getDuplicateStrands().size();
        if (halfAmount % 2 == 0 ) halfAmount /= 2;
        else halfAmount = (halfAmount/2)+1;
        if ( size_of_orig_strand_to_this_cluster <= halfAmount ){
            int delta = halfAmount - size_of_orig_strand_to_this_cluster;
            vector<duplicateStrandWiteErrors> current_cluster_strands = cluster.getDuplicateStrands();

            for (int j = 0; j < delta+1; ++j) {
                duplicateStrandWiteErrors duplicate_to_insert(cluster_index, original_strand, cluster_index, original_strand);
                current_cluster_strands.push_back(duplicate_to_insert);
            }
            cluster.setDuplicateStrands(current_cluster_strands);
        }
    }
    else{

    }
}


#endif //CLUSTERING_CORRECTING_CODES_SIMULATOR_H
