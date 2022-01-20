//
// Created by  Elon Grubman on 21/01/2020.
//

#ifndef CLUSTERING_CORRECTING_CODES_ERRORIDENTIFICATIONINCLUSTER_H
#define CLUSTERING_CORRECTING_CODES_ERRORIDENTIFICATIONINCLUSTER_H


#include "simulator.h"


class errorIdentificationInCluster {

    unordered_map<int,clusterAfterSimulation> map;
    unordered_map<int, vector<duplicateStrandWiteErrors>> encoded_strand_in_wrong_place;
    string assumption;
    int tao;
    int ro;
    int e;
    int t;
    bool fixedErrorsAbility;

public:

    errorIdentificationInCluster(int _tao, int _ro, int _e, int _t, unordered_map<int,encoded_strand_binary>& _map, string _assumption) :
    tao(_tao), ro(_ro), e(_e), t(_t), assumption(_assumption){
        simulator s(tao, ro, e, t, _map, assumption);
        map = s.getMap();
        if( e >= 2*tao) fixedErrorsAbility = true;
        else fixedErrorsAbility = false;
    }

    unordered_map<int,vector<duplicateStrandWiteErrors>>& getMapOfWronfStrands()  {
        return encoded_strand_in_wrong_place;
    }

    unordered_map<int,clusterAfterSimulation>& getMap()  {
        return map;
    }

    void setMap( unordered_map<int,clusterAfterSimulation>& map) {
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

    int getE(){
        return e;
    }

    void setE(int e) {
        e = e;
    }

    int getT(){
        return t;
    }

    void setT(int t) {
        t = t;
    }

    /*!
     * function who add the wrong strands to dedicted map before they delete from the cluster
     * @param cluster_index - the key in the dedicted map of wrong strands. suitable to the cluster index.
     * @param strands - the wrong strands to add.
     */
    void addStrandsToMapOfWrongPlace(int cluster_index, vector<duplicateStrandWiteErrors> strands){
        auto wrong_strands_it = encoded_strand_in_wrong_place.find(cluster_index);
        if(wrong_strands_it == encoded_strand_in_wrong_place.end()){
            pair<int,vector<duplicateStrandWiteErrors>> strands_to_insert(cluster_index,strands);
            encoded_strand_in_wrong_place.insert(strands_to_insert);
        }
        else{
            vector<duplicateStrandWiteErrors> vec_to_union = wrong_strands_it->second;
            vector<duplicateStrandWiteErrors> concatenate_vector;
            concatenate_vector.reserve( vec_to_union.size() + strands.size() );
            concatenate_vector.insert( concatenate_vector.end(), vec_to_union.begin(), vec_to_union.end() );
            concatenate_vector.insert( concatenate_vector.end(), strands.begin(), strands.end() );
            pair<int,vector<duplicateStrandWiteErrors>> strands_to_insert(cluster_index,concatenate_vector);
            encoded_strand_in_wrong_place.insert(strands_to_insert);
        }
    }

    /*!
     * function who received vector of strands and convert him to vector of vectors of strand while the strands ordered by their original index
     * @param subsets - the target vector of vectors of strands
     * @param cluster - vector of strands
     */
    void convertVecOFStrandsToVecOfSubsetsStrands(vector<vector<duplicateStrandWiteErrors>>& subsets, vector<duplicateStrandWiteErrors>& cluster){
        bool already_insert;
        for (auto strands_it = cluster.begin(); strands_it != cluster.end(); ++strands_it) {
            already_insert = false;
            for (int i = 0; i < subsets.size(); ++i) {
                duplicateStrandWiteErrors strande_to_compare = subsets[i][0];
                if (HammingDistance(strands_it->getDataAfterSimulation(), strande_to_compare.getDataAfterSimulation()) <= 2 * ro) {
                    subsets[i].push_back(*strands_it);
                    cluster.erase(strands_it);
                    strands_it--;
                    already_insert = true;
                    break;
                }
            }
            if (!already_insert) {
                vector<duplicateStrandWiteErrors> new_subset;
                new_subset.push_back(*strands_it);
                subsets.push_back(new_subset);
                cluster.erase(strands_it);
                strands_it--;
            }
        }
        assert(cluster.size() == 0);
    }

    /*!
     * function who get specipic cluster and clean him from wrong strands
     * @param cluster - the cluster who fixed
     * @param cluster_index - cluster's index
     */
    void cleanErrorsFromCluster(vector<duplicateStrandWiteErrors>& cluster, int cluster_index){
        /// in case that 2ro > e >= ro , we need to fix according to majority assumption
        if( !fixedErrorsAbility ) {
            vector<duplicateStrandWiteErrors> F = cluster;
            while (F.size() > cluster.size() / 2) {
                int randomic_index = rand() % cluster.size();
                duplicateStrandWiteErrors compare_strands_by = cluster[randomic_index];
                F.clear();
                int cluster_size_befor_delete = cluster.size();
                for (auto strands_it = cluster.begin(); strands_it != cluster.end(); ++strands_it) {
                    if (HammingDistance(compare_strands_by.getDataAfterSimulation(), strands_it->getDataAfterSimulation()) > 2 * ro) {
                        F.push_back(*strands_it);
                        cluster.erase(strands_it);
                        strands_it--;
                    }
                }
                if (F.size() <= cluster_size_befor_delete / 2) {
                    addStrandsToMapOfWrongPlace(cluster_index, F);
                } else {
                    addStrandsToMapOfWrongPlace(cluster_index, cluster);
                    cluster.clear();
                    cluster = F;
                }
            }
        }
        /// in case that e >= 2ro , we any way chose to fix according to dominance assumption regardless the assumption
        else if ( fixedErrorsAbility ) {
            vector<vector<duplicateStrandWiteErrors>> subsets;

            convertVecOFStrandsToVecOfSubsetsStrands(subsets, cluster);

            auto max_subsets_index_it = subsets.begin();
            for (auto subsets_it = subsets.begin(); subsets_it != subsets.end(); ++subsets_it) {
                if (subsets_it->size() > max_subsets_index_it->size()) max_subsets_index_it = subsets_it;
            }
            cluster = *max_subsets_index_it;
            subsets.erase(max_subsets_index_it);
            vector<duplicateStrandWiteErrors> all_the_rest_strands;
            for (auto subsets_it = subsets.begin(); subsets_it != subsets.end(); ++subsets_it) {
                for (int i = 0; i < subsets_it->size(); ++i) {
                    all_the_rest_strands.push_back((*subsets_it)[i]);
                }
            }
            addStrandsToMapOfWrongPlace(cluster_index, all_the_rest_strands);
        }
        /// in case that e >= 4ro , not to implement meanwhile
        else{

        }
    }

    /*!
     * function that make union between vector of strands to another vector of strands that placed in some cluster
     * @param strands_to_fix - vector of strands that placed in wrong place and now transfer to correct place
     * @param correct_cluster_index - the index of correct cluster
     */
    void insertTheWrongStrandsToTheirCorrectCluster(vector<duplicateStrandWiteErrors>& strands_to_fix, int correct_cluster_index){
        auto clusters_it = map.find(correct_cluster_index);
        vector<duplicateStrandWiteErrors> strands_from_correct_cluster = clusters_it->second.getDuplicateStrands();
        vector<duplicateStrandWiteErrors> concatenate_vector;
        concatenate_vector.reserve( strands_from_correct_cluster.size() + strands_to_fix.size() );
        concatenate_vector.insert( concatenate_vector.end(), strands_from_correct_cluster.begin(), strands_from_correct_cluster.end() );
        concatenate_vector.insert( concatenate_vector.end(), strands_to_fix.begin(), strands_to_fix.end() );
        vector<char> empty_vec;
        clusterAfterSimulation cluster_to_fix(concatenate_vector,empty_vec);
        pair<int,clusterAfterSimulation> cluster_to_insert(correct_cluster_index,cluster_to_fix);
        map.erase(clusters_it);
        map.insert(cluster_to_insert);
    }


    /*!
     * function that received wrong strands and put them in thier correct cluster
     * @param wrong_strands - vector of strands to fix
     */
    void putWrongStrandsInTheCorrectClusters(vector<duplicateStrandWiteErrors>& wrong_strands){

        vector<vector<duplicateStrandWiteErrors>> subsets;
        convertVecOFStrandsToVecOfSubsetsStrands(subsets, wrong_strands);
        for (int i = 0; i < subsets.size(); ++i) {
            vector<int> current_strand = subsets[i][0].getDataAfterSimulation();
            for (int j = 0; j < map.size(); ++j) {
                auto clusters_it = map.find(j);
                vector<int> strand_from_cluster_to_compare = clusters_it->second.getDuplicateStrands()[0].getDataAfterSimulation();
                if(HammingDistance(current_strand, strand_from_cluster_to_compare) <= 2 * ro){
                    insertTheWrongStrandsToTheirCorrectCluster(subsets[i], clusters_it->first);
                    break;
                }
            }
        }
    }

    /*!
     * function that calculate for specific cluster his estimated orig strand
     * @param strands_from_current_cluster - the strands that belong to the current cluster
     */
    void calcEstimateOrigStrandForSpecificCluster(vector<duplicateStrandWiteErrors>& strands_from_current_cluster, vector<char>& estimate_orig_strand){

        int strand_data_size = strands_from_current_cluster[0].getDataAfterSimulation().size();
        for (int j = 0; j < strand_data_size; ++j) {

            int bit_counter = 0;
            for (int i = 0; i < strands_from_current_cluster.size(); ++i) {

                if(strands_from_current_cluster[i].getDataAfterSimulation()[j] == 1) bit_counter++;
                else bit_counter--;

            }

            if(bit_counter > 0) estimate_orig_strand.push_back('1');
            else if(bit_counter == 0) estimate_orig_strand.push_back('?');
            else estimate_orig_strand.push_back('0');

        }
    }


    /*!
     * function that calculate for each cluster his estimated orig strand
     * @param map - the clusters in the system after they fixed
     */
    void calcEstimateOrigStrandForEachCluster(unordered_map<int,clusterAfterSimulation>& map){

        for (int i = 0; i < map.size(); ++i) {
            auto it = map.find(i);
            if(it == map.end()){
                cout << "calcEstimateOrigStrandForEachCluster:: can't find the Key " << i << " in map" << endl;
            }
            else{
                calcEstimateOrigStrandForSpecificCluster(it->second.getDuplicateStrands(), it->second.getEstimatedOrigStrand());
            }
        }

    }


    /*!
     * function who go trough cluster after cluster and clean the wrong encoded strands to dedicted map
     */
    void algorithmToIdentifyErrors(){
        for (int i = 0; i < map.size(); ++i) {
            auto it = map.find(i);
            if(it == map.end()){
                cout << "algorithmToIdentifyErrors:: can't find the Key " << i << " in map" << endl;
            }
            else{
                cleanErrorsFromCluster(it->second.getDuplicateStrands(), i);
            }
        }
    }

    /*!
     * function who go trough map of wrong strands and put the wrong strands in their correct clusters
     */
    void algorithmToFixErrors(){
        for (int i = 0; i < encoded_strand_in_wrong_place.size(); ++i) {
            auto it = encoded_strand_in_wrong_place.find(i);
            if(it == encoded_strand_in_wrong_place.end()){
                cout << "algorithmToFixErrors:: can't find the Key " << i << " in map of wrong strands" << endl;
            }
            else{
                vector<duplicateStrandWiteErrors> wrong_strands = it->second;
                putWrongStrandsInTheCorrectClusters(wrong_strands);
            }
        }

        /// after we put the wrong strands in their correct cluster we calculate for each cluster his estimated orig strand
        calcEstimateOrigStrandForEachCluster(map);

    }


};


#endif //CLUSTERING_CORRECTING_CODES_ERRORIDENTIFICATIONINCLUSTER_H
