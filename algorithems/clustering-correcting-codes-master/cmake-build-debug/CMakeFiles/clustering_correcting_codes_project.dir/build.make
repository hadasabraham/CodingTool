# CMAKE generated file: DO NOT EDIT!
# Generated by "MinGW Makefiles" Generator, CMake Version 3.17

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Disable VCS-based implicit rules.
% : %,v


# Disable VCS-based implicit rules.
% : RCS/%


# Disable VCS-based implicit rules.
% : RCS/%,v


# Disable VCS-based implicit rules.
% : SCCS/s.%


# Disable VCS-based implicit rules.
% : s.%


.SUFFIXES: .hpux_make_needs_suffix_list


# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

SHELL = cmd.exe

# The CMake executable.
CMAKE_COMMAND = "C:\Program Files\JetBrains\CLion 2020.3.3\bin\cmake\win\bin\cmake.exe"

# The command to remove a file.
RM = "C:\Program Files\JetBrains\CLion 2020.3.3\bin\cmake\win\bin\cmake.exe" -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = C:\Users\Hadas\Desktop\DNA_gui\algorithems\clustering-correcting-codes-master

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = C:\Users\Hadas\Desktop\DNA_gui\algorithems\clustering-correcting-codes-master\cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/clustering_correcting_codes_project.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/clustering_correcting_codes_project.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/clustering_correcting_codes_project.dir/flags.make

CMakeFiles/clustering_correcting_codes_project.dir/main.cpp.obj: CMakeFiles/clustering_correcting_codes_project.dir/flags.make
CMakeFiles/clustering_correcting_codes_project.dir/main.cpp.obj: ../main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=C:\Users\Hadas\Desktop\DNA_gui\algorithems\clustering-correcting-codes-master\cmake-build-debug\CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/clustering_correcting_codes_project.dir/main.cpp.obj"
	C:\PROGRA~2\MINGW-~1\I686-8~1.0-P\mingw32\bin\G__~1.EXE  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles\clustering_correcting_codes_project.dir\main.cpp.obj -c C:\Users\Hadas\Desktop\DNA_gui\algorithems\clustering-correcting-codes-master\main.cpp

CMakeFiles/clustering_correcting_codes_project.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/clustering_correcting_codes_project.dir/main.cpp.i"
	C:\PROGRA~2\MINGW-~1\I686-8~1.0-P\mingw32\bin\G__~1.EXE $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E C:\Users\Hadas\Desktop\DNA_gui\algorithems\clustering-correcting-codes-master\main.cpp > CMakeFiles\clustering_correcting_codes_project.dir\main.cpp.i

CMakeFiles/clustering_correcting_codes_project.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/clustering_correcting_codes_project.dir/main.cpp.s"
	C:\PROGRA~2\MINGW-~1\I686-8~1.0-P\mingw32\bin\G__~1.EXE $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S C:\Users\Hadas\Desktop\DNA_gui\algorithems\clustering-correcting-codes-master\main.cpp -o CMakeFiles\clustering_correcting_codes_project.dir\main.cpp.s

# Object files for target clustering_correcting_codes_project
clustering_correcting_codes_project_OBJECTS = \
"CMakeFiles/clustering_correcting_codes_project.dir/main.cpp.obj"

# External object files for target clustering_correcting_codes_project
clustering_correcting_codes_project_EXTERNAL_OBJECTS =

clustering_correcting_codes_project.exe: CMakeFiles/clustering_correcting_codes_project.dir/main.cpp.obj
clustering_correcting_codes_project.exe: CMakeFiles/clustering_correcting_codes_project.dir/build.make
clustering_correcting_codes_project.exe: CMakeFiles/clustering_correcting_codes_project.dir/linklibs.rsp
clustering_correcting_codes_project.exe: CMakeFiles/clustering_correcting_codes_project.dir/objects1.rsp
clustering_correcting_codes_project.exe: CMakeFiles/clustering_correcting_codes_project.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=C:\Users\Hadas\Desktop\DNA_gui\algorithems\clustering-correcting-codes-master\cmake-build-debug\CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable clustering_correcting_codes_project.exe"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles\clustering_correcting_codes_project.dir\link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/clustering_correcting_codes_project.dir/build: clustering_correcting_codes_project.exe

.PHONY : CMakeFiles/clustering_correcting_codes_project.dir/build

CMakeFiles/clustering_correcting_codes_project.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles\clustering_correcting_codes_project.dir\cmake_clean.cmake
.PHONY : CMakeFiles/clustering_correcting_codes_project.dir/clean

CMakeFiles/clustering_correcting_codes_project.dir/depend:
	$(CMAKE_COMMAND) -E cmake_depends "MinGW Makefiles" C:\Users\Hadas\Desktop\DNA_gui\algorithems\clustering-correcting-codes-master C:\Users\Hadas\Desktop\DNA_gui\algorithems\clustering-correcting-codes-master C:\Users\Hadas\Desktop\DNA_gui\algorithems\clustering-correcting-codes-master\cmake-build-debug C:\Users\Hadas\Desktop\DNA_gui\algorithems\clustering-correcting-codes-master\cmake-build-debug C:\Users\Hadas\Desktop\DNA_gui\algorithems\clustering-correcting-codes-master\cmake-build-debug\CMakeFiles\clustering_correcting_codes_project.dir\DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/clustering_correcting_codes_project.dir/depend

