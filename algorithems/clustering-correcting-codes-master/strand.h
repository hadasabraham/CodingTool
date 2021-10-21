//
// Created by amitw on 22/11/2019.
//

#ifndef CLUSTERING_CORRECTING_CODES_PROJECT_STRAND_H
#define CLUSTERING_CORRECTING_CODES_PROJECT_STRAND_H

#include "includes.h"

using namespace std;

/*!
 * class representing a single strand.
 * data - representing the data part of the strand
 * index - representing the index part of the strand.
 */
class strand {
    int index;
    vector<int> data;
public:
    strand(int initial_index, const vector<int> &initial_data): index(initial_index), data(initial_data){};

     int getIndex()  {
        return index;
    }

     vector<int>& getData()  {
         return data;
    }

    void setIndex(int &index) {
        strand::index = index;
    }

    void setData(const vector<int> &data) {
        strand::data = data;
    }


};


#endif //CLUSTERING_CORRECTING_CODES_PROJECT_STRAND_H
