//
// Created by  Elon Grubman on 28/01/2020.
//

#ifndef CLUSTERING_CORRECTING_CODES_CLUSTERAFTERSIMULATION_H
#define CLUSTERING_CORRECTING_CODES_CLUSTERAFTERSIMULATION_H

#include "duplicateStrandWiteErrors.h"

using namespace std;

class clusterAfterSimulation {

    vector<duplicateStrandWiteErrors> duplicate_strands;
    vector<char> estimated_orig_strand;
    unordered_map<int,int> origIndexesAmount;

public:

    clusterAfterSimulation(vector<duplicateStrandWiteErrors> &duplicateStrands, vector<char> &estimatedOrigStrand) :
    duplicate_strands(duplicateStrands), estimated_orig_strand(estimatedOrigStrand) {
        for (int i = 0; i < duplicate_strands.size(); ++i) {
            int orig_index = duplicate_strands[i].getOrigIndex();
            auto it = origIndexesAmount.find(orig_index);
            if(it == origIndexesAmount.end()){
                origIndexesAmount[orig_index] = 1;
            }
            else{
                int old_amount = it->second;
                int new_amount = old_amount + 1;
                origIndexesAmount[orig_index] = new_amount;
            }
        }
    }

    vector<duplicateStrandWiteErrors> &getDuplicateStrands(){
        return duplicate_strands;
    }

    void setDuplicateStrands(vector<duplicateStrandWiteErrors> &duplicateStrands) {
        duplicate_strands = duplicateStrands;
    }

    vector<char> &getEstimatedOrigStrand(){
        return estimated_orig_strand;
    }

    void setEstimatedOrigStrand(vector<char> &estimatedOrigStrand) {
        estimated_orig_strand = estimatedOrigStrand;
    }

    unordered_map<int,int> &getOrigIndexesAmount() {
        return origIndexesAmount;
    }
};


#endif //CLUSTERING_CORRECTING_CODES_CLUSTERAFTERSIMULATION_H
