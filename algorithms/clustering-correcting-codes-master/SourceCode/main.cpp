#include <iostream>
#include "encoding_algorithim.h"
#include "files.h"
#include "decoding_algorithim_tests.h"
#include "encoding_algorithim_tests.h"

using namespace std;

void testConvertCharVecToIntVec() {
	vector<char> f( { '1', '0', '0', '1' });
	vector<int> t;
	convertCharVecToIntVec(f, t);
	for (int i = 0; i < t.size(); i++) {
		cout << t[i] << endl;
	}
}

void TestsetNextNodeInList(vector<int> index_in_binary) {
	vector<int> encoded_data { 1, 1, 0 };
	encoded_data.insert(encoded_data.begin(), index_in_binary.begin(), index_in_binary.end());
	for (int i = 0; i < encoded_data.size(); i++) {
		cout << encoded_data[i] << endl;
	}

}

void testConvertIntVecToCharVec() {
	vector<char> f;
	vector<int> t { 1, 0, 0, 1 };
	convertIntVecToCharVec(f, t);
	for (int i = 0; i < f.size(); i++) {
		cout << f[i] << endl;
	}
}

/*!
 * sets t and e according to the raw and tao given parameters, the number of strands, their data length and
 * if brute force manner is conducted or not.
 * @param e - index constraint
 * @param t - data constraint
 * @param raw - given parameter
 * @param tao - given paramter
 * @param strands_num - number of strands in the system
 * @param strands_data_length - the length of the data of the strands
 * @param bruteForce - wether we're using bruteforce manner or not.
 */
void set_e_and_t(int* e, int* t, int raw, int tao, int strands_num, int strands_data_length, bool bruteForce) {
	*t = raw * 4 + 1;
	int index_length = ceil(log2(strands_num));
	int delta_2_size = ceil(log2(strands_data_length)) * (*t - 1);
	for (int i = 2 * tao; i >= tao; i--) {
		int delta_1_size = ceil(log2(index_length)) * i;
		if (bruteForce) {
			if (strands_data_length < index_length + 1 + delta_1_size + delta_2_size + 3 * *(t) + 2 * delta_1_size) {
				continue;
			}
			else {
				*e = i;
				return;
			}
		}
		else {
			if (strands_data_length < index_length + 1 + delta_1_size + delta_2_size + *(t) * ceil(log2(strands_num))) {
				continue;
			}
			else {
				*e = i;
				return;
			}
		}
	}
	return;

}

void updateMapWithDuplicatesNumber(vector<duplicateStrandWiteErrors>& duplicate_strands,
		std::map<vector<int>, int>& num_of_duplicates_from_each_strand) {
	for (int i = 0; i < duplicate_strands.size(); ++i) {
		auto it = num_of_duplicates_from_each_strand.find(duplicate_strands[i].getDataAfterSimulation());
		if (it == num_of_duplicates_from_each_strand.end()) {
			pair<vector<int>, int> p(duplicate_strands[i].getDataAfterSimulation(), 1);
			num_of_duplicates_from_each_strand.insert(p);
		}
		else {
			pair<vector<int>, int> p2(it->first, it->second + 1);
			num_of_duplicates_from_each_strand.erase(it);
			num_of_duplicates_from_each_strand.insert(p2);
		}
	}
}

int chackOrigIndex(vector<int>& strand, vector<duplicateStrandWiteErrors> & duplicate_strands) {
	for (int i = 0; i < duplicate_strands.size(); ++i) {
		if (duplicate_strands[i].getDataAfterSimulation() == strand) {
			return duplicate_strands[i].getOrigIndex();
		}
	}
	assert(0);
	return 0;
}

void printClusters(errorIdentificationInCluster& clusters, unordered_map<int, encoded_strand_binary>& map) {
	std::map<vector<int>, int> num_of_duplicates_from_each_strand;

	for (int j = 0; j < clusters.getMap().size(); ++j) {
		int counter_good_strand = 0, counter_bad_strand = 0;
		auto map_it = map.find(j);
		encoded_strand_binary the_orig_strand = map_it->second;
		auto it = clusters.getMap().find(j);
		if (it == clusters.getMap().end()) {
			cout << "printClusters:: Can't find the Key " << j << " in the clusters's hash" << endl;
		}
		else {
			cout << "cluster with index " << j << " : the original strand to this cluster is ";
			for (int l = 0; l < the_orig_strand.get_encoded_data().size(); ++l) {
				cout << the_orig_strand.get_encoded_data()[l] << " ";
			}
			cout << endl;

			updateMapWithDuplicatesNumber(it->second.getDuplicateStrands(), num_of_duplicates_from_each_strand);

			for (auto it_map = num_of_duplicates_from_each_strand.begin();
					it_map != num_of_duplicates_from_each_strand.end(); ++it_map) {
				vector<int> vec = it_map->first;
				if (chackOrigIndex(vec, it->second.getDuplicateStrands()) == j)
					counter_good_strand += it_map->second;
				else
					counter_bad_strand += it_map->second;
				int strand_in_map_size = it_map->first.size();
				for (int k = 0; k < strand_in_map_size; ++k) {
					cout << it_map->first[k] << " ";
				}
				cout << "::: " << it_map->second << " duplicates";
				cout << " ::: orig index is " << chackOrigIndex(vec, it->second.getDuplicateStrands()) << endl;
			}
		}
		cout << "The number of strands under this cluster is : " << it->second.getDuplicateStrands().size() << endl;
		cout << "The number of CORRECT strands under this cluster is : " << counter_good_strand << endl;
		cout << "The number of WRONG strands under this cluster is : " << counter_bad_strand << endl;

		cout << "##  The estimated original strand is : ";
		if (it->second.getEstimatedOrigStrand().size() == 0)
			cout << " --- " << endl << endl;
		else {
			for (int m = 0; m < it->second.getEstimatedOrigStrand().size(); ++m) {
				cout << it->second.getEstimatedOrigStrand()[m] << " ";
			}
			cout << endl << endl;
		}
		num_of_duplicates_from_each_strand.clear();
	}
}

void printDataToFile(errorIdentificationInCluster& clusters, unordered_map<int, encoded_strand_binary>& map,
		string fileName) {
	std::ofstream myfile;
	myfile.open(fileName);

	std::map<vector<int>, int> num_of_duplicates_from_each_strand;

	for (int j = 0; j < clusters.getMap().size(); ++j) {
		int counter_good_strand = 0, counter_bad_strand = 0;
		auto map_it = map.find(j);
		encoded_strand_binary the_orig_strand = map_it->second;
		auto it = clusters.getMap().find(j);
		if (it == clusters.getMap().end()) {
			myfile << "printDataToFile:: Can't find the Key " << j << " in the clusters's hash" << endl;
		}
		else {
			myfile << "cluster with index " << j << " : the original strand to this cluster is ";
			for (int l = 0; l < the_orig_strand.get_encoded_data().size(); ++l) {
				myfile << the_orig_strand.get_encoded_data()[l] << " ";
			}
			myfile << endl;

			updateMapWithDuplicatesNumber(it->second.getDuplicateStrands(), num_of_duplicates_from_each_strand);

			for (auto it_map = num_of_duplicates_from_each_strand.begin();
					it_map != num_of_duplicates_from_each_strand.end(); ++it_map) {
				vector<int> vec = it_map->first;
				if (chackOrigIndex(vec, it->second.getDuplicateStrands()) == j)
					counter_good_strand += it_map->second;
				else
					counter_bad_strand += it_map->second;
				int strand_in_map_size = it_map->first.size();
				for (int k = 0; k < strand_in_map_size; ++k) {
					myfile << it_map->first[k] << " ";
				}
				myfile << "::: " << it_map->second << " duplicates";
				myfile << " ::: orig index is " << chackOrigIndex(vec, it->second.getDuplicateStrands()) << endl;
			}
		}
		myfile << "The number of strands under this cluster is : " << it->second.getDuplicateStrands().size() << endl;
		myfile << "The number of CORRECT strands under this cluster is : " << counter_good_strand << endl;
		myfile << "The number of WRONG strands under this cluster is : " << counter_bad_strand << endl;

		myfile << "##  The estimated original strand is : ";
		if (it->second.getEstimatedOrigStrand().size() == 0)
			myfile << " --- " << endl << endl;
		else {
			for (int m = 0; m < it->second.getEstimatedOrigStrand().size(); ++m) {
				myfile << it->second.getEstimatedOrigStrand()[m] << " ";
			}
			myfile << endl << endl;
		}
		num_of_duplicates_from_each_strand.clear();
	}
}

void printFixErrorsOutputs(errorIdentificationInCluster& clusters, string fileName) {
	std::ofstream myfile;
	myfile.open(fileName);

	for (int j = 0; j < clusters.getMap().size(); ++j) {

		auto it = clusters.getMap().find(j);
		if (it == clusters.getMap().end()) {
			myfile << "printFixErrorsOutputs:: Can't find the Key " << j << " in the clusters's hash" << endl;
		}
		else {
			for (int i = 0; i < it->second.getEstimatedOrigStrand().size(); ++i) {
				myfile << it->second.getEstimatedOrigStrand()[i];
			}
			myfile << endl;
		}
	}
}

void makeMapFromFixErrorsOutput(errorIdentificationInCluster& clusters,
		unordered_map<int, encoded_strand_binary>& strands_after_fix_errors) {
	for (int j = 0; j < clusters.getMap().size(); ++j) {

		auto it = clusters.getMap().find(j);
		if (it == clusters.getMap().end()) {
			cout << "makeMapFromFixErrorsOutput:: Can't find the Key " << j << " in the clusters's hash" << endl;
		}
		else {
			vector<int> int_strand;
			convertCharVecToIntVec(it->second.getEstimatedOrigStrand(), int_strand);
			encoded_strand_binary output_strand(int_strand, false);
			pair<int, encoded_strand_binary> pair(j, output_strand);
			strands_after_fix_errors.insert(pair);
		}
	}
}
// *** untouched module ***
// "U" and rest of parameters the same
// raw
// tao
// strands data length
// assumption
// brute force
// input file

// *** Encoding module ***
// "E"
// raw
// tao
// strands data length
// brute force
// input file
// output file

// *** Decoding module ***
// "D"
// raw
// tao
// strands data length
// brute force
// input file
// output file

// example parameters
// U 1 3 100 D false test_file_updated.txt
// E 1 3 100 false encoder_input.txt encoder_output.txt
// D 1 3 100 false decoder_input.txt decoder_output.txt

int main(int argc, char** argv) {

	if (argc != 8) {
		cout << "wrong number of parameters in the command line" << endl;
		return 0;
	}

	string UEDchoice = argv[1];
	if (UEDchoice != "U" && UEDchoice != "E" && UEDchoice != "D") {
		cout << "Illegal parameter!" << endl;
		return 0;
	}

	// 	extracting raw, tao, len. same parameters and locations for all options.
	string raw_str = argv[2];
	string tao_str = argv[3];
	string strand_data_length_str = argv[4];
	int raw = stoi(raw_str);
	int tao = stoi(tao_str);
	int strand_data_length = stoi(strand_data_length_str);

	if (UEDchoice == "U") { // original code as is
		string assumption = argv[5];
		string check_bruteForce = argv[6];
		string file_to_parse = argv[7];
		bool bruteForce = false;
		if (check_bruteForce == "true") {
			bruteForce = true;
		}
		/**** combined test ****/

		unordered_map<int, vector<int>> strands;
		map<int, vector<int>> strands_map;
		int padding = 0;

		ParseDataToEncoding(file_to_parse, strand_data_length, strands, padding);

		int e = -1;
		int t = -1;
		unordered_map<int, encoded_strand_binary> encoded_strands;
		map<int, encoded_strand_binary> encoded_strands_map;

		convertUnorderedMapBeforeEncodingToMap(strands, strands_map);

		exportStrandsBeforeEncodingToFile("results_before_encoding.txt", strands_map, padding);

		set_e_and_t(&e, &t, raw, tao, strands.size(), strand_data_length, bruteForce);

		if (e == -1) {
			cout << "the given strands data length is not holding the encoding constraints" << endl;
			return 0;
		}

		encoding_algorithm(strands, e, t, strand_data_length, HammingDistance, encoded_strands, bruteForce);

		convertUnorderedMapToMap(encoded_strands, encoded_strands_map);

		exportStrandsToFile("results_after_encoding.txt", encoded_strands_map, padding);

		unordered_map<int, encoded_strand_binary> encoded_strands_to_elon = encoded_strands;

		errorIdentificationInCluster clusters(tao, raw, e, t, encoded_strands_to_elon, assumption);

		printDataToFile(clusters, encoded_strands_to_elon, "status_after_errors_simulations.txt");

		clusters.algorithmToIdentifyErrors();

		clusters.algorithmToFixErrors();

		printDataToFile(clusters, encoded_strands_to_elon, "status_after_fix_errors.txt");

		printFixErrorsOutputs(clusters, "status_to_fix_errors_output.txt");

		unordered_map<int, encoded_strand_binary> strands_after_fix_errors; /// <----- use it for decoding!

		makeMapFromFixErrorsOutput(clusters, strands_after_fix_errors);

		DecodingAlgorithim(strands_after_fix_errors, strand_data_length, e, t, HammingDistance);

		encoded_strands_map.clear();

		convertUnorderedMapToMap(strands_after_fix_errors, encoded_strands_map);

		exportStrandsToFile("decoding_results_after_clustring.txt", encoded_strands_map, padding);

		DecodingAlgorithim(encoded_strands, strand_data_length, e, t, HammingDistance);

		encoded_strands_map.clear();

		convertUnorderedMapToMap(encoded_strands, encoded_strands_map);

		exportStrandsToFile("results_after_decoding.txt", encoded_strands_map, padding);
	}
	else { // encode or decode

		string check_bruteForce = argv[5];
		string input_file = argv[6];
		string output_file = argv[7];
		bool bruteForce = false;
		if (check_bruteForce == "true") {
			bruteForce = true;
		}

		if (UEDchoice == "E") {
			unordered_map<int, vector<int>> strands;
			map<int, vector<int>> strands_map;
			int padding = 0;

			ParseDataToEncoding(input_file, strand_data_length, strands, padding);

			int e = -1;
			int t = -1;

			convertUnorderedMapBeforeEncodingToMap(strands, strands_map);

			set_e_and_t(&e, &t, raw, tao, strands.size(), strand_data_length, bruteForce);

			if (e == -1) {
				cout << "the given strands data length is not holding the encoding constraints" << endl;
				return 0;
			}

			unordered_map<int, encoded_strand_binary> encoded_strands;
			map<int, encoded_strand_binary> encoded_strands_map;

			encoding_algorithm(strands, e, t, strand_data_length, HammingDistance, encoded_strands, bruteForce);

			convertUnorderedMapToMap(encoded_strands, encoded_strands_map);

			exportStrandsToFile(output_file, encoded_strands_map, padding);

		}
		else { // UEDchoice == "D" - decode only
			   // **** data parsing for decoding ****

			unordered_map<int, encoded_strand_binary> encoded_strands_from_file;
			EncodedStrandsFromFile(input_file, strand_data_length, bruteForce, encoded_strands_from_file);

			int e = -1;
			int t = -1;
			set_e_and_t(&e, &t, raw, tao, encoded_strands_from_file.size(), strand_data_length, bruteForce);

			if (e == -1) {
				cout << "the given strands data length is not holding the encoding constraints" << endl;
				return 0;
			}

			DecodingAlgorithim(encoded_strands_from_file, strand_data_length, e, t, HammingDistance);
			map<int, encoded_strand_binary> encoded_strands_from_file_map;
			convertUnorderedMapToMap(encoded_strands_from_file, encoded_strands_from_file_map);
			exportStrandsToFile(output_file, encoded_strands_from_file_map, 0); // last parameter in this function doesn't matter because it is not used

		}
	}

}

//    testDecToBinary();
//    testingDeltaOne();
//    testS_e_i();
//    testW_l_S_t();
//    testCreateBSet();
//    testCreateReplVector();
//    testBinaryToDec();
//    vector<string> DP[K][K];
//    findBitCombinations(4,DP,2);
//    testDistanceByOne();
//    testS_e_i();
//    testW_l_S_t_BruteForce();
//    testW_l_S_t_NoBruteForce();
//    testCreateBinaryFromDelta1();
//    testCreateBinaryFromDelta2();
//    testCreateOneBinaryVectorFromEncodedData();
//    testFindPairToBeFixed();
//    unordered_map<int, encoded_strand> encoded_strands;
//    testEncodingAlgorithim(encoded_strands);
//    unordered_map<int, vector<int>> strands;
//    ParseDataToEncoding("test_file.txt", 10, strands);
//    testEncodingAlgorithim();
//    testcreateDecodingOrderList();

/******* encoding algorithim tests ********/

/**
 testCreateDelta1();
 testCreateDelta2();
 testW_lBruteForce();
 testW_lNoBruteForce();
 testCreateReplVector();
 testCreateS_e_i();
 testAddEncodedVersion();
 testEncodingAlgorithim();
 **/

/******** deocding algorithim tests ********/

/**
 testCreateDecodingOrderList();
 testDecodeIndex();
 testDecodeData();
 testDecodingAlgorithim();
 **/

