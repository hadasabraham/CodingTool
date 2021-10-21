cmake_minimum_required(VERSION 3.10)
project(clustering_correcting_codes_project)

set(CMAKE_CXX_STANDARD 11)

add_executable(clustering_correcting_codes_project
        main.cpp
        strand.h
        encoding_algorithim.h
        encoded_strand_binary.h
        files.h
        includes.h
        decoding_algorithim_tests.h
        decoding_algorithim.h
        encoding_algorithim_tests.h
        clusterAfterSimulation.h
        duplicateStrandWiteErrors.h
        errorCluster.h
        simulator.h)

