//
// Created by  Elon Grubman on 28/01/2020.
//

#ifndef CLUSTERING_CORRECTING_CODES_DUPLICATESTRANDWITEERRORS_H
#define CLUSTERING_CORRECTING_CODES_DUPLICATESTRANDWITEERRORS_H

#include "includes.h"
using namespace std;

class duplicateStrandWiteErrors {

    int index_after_simulation;
    vector<int> data_after_simulation;
    int orig_index;
    vector<int> orig_data;

public:

    duplicateStrandWiteErrors(int indexAfterSimulation, vector<int> &dataAfterSimulation, int origIndex, vector<int> &origData) :
    index_after_simulation(indexAfterSimulation), data_after_simulation(dataAfterSimulation), orig_index(origIndex), orig_data(origData) {}

    int getIndexAfterSimulation(){
        return index_after_simulation;
    }

    void setIndexAfterSimulation(int indexAfterSimulation) {
        index_after_simulation = indexAfterSimulation;
    }

    vector<int> getDataAfterSimulation() const{
        return data_after_simulation;
    }


    void setDataAfterSimulation(vector<int> &dataAfterSimulation)  {
        data_after_simulation = dataAfterSimulation;
    }

    int getOrigIndex() const {
        return orig_index;
    }

    void setOrigIndex(int origIndex) {
        orig_index = origIndex;
    }

    vector<int> &getOrigData(){
        return orig_data;
    }

    void setOrigData(vector<int> &origData) {
        orig_data = origData;
    }
};


#endif //CLUSTERING_CORRECTING_CODES_DUPLICATESTRANDWITEERRORS_H
