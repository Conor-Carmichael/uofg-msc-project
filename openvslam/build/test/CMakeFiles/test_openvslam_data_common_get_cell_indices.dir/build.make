# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.5

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/conor/msc-project/openvslam

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/conor/msc-project/openvslam/build

# Include any dependencies generated for this target.
include test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/depend.make

# Include the progress variables for this target.
include test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/progress.make

# Include the compile flags for this target's objects.
include test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/flags.make

test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.o: test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/flags.make
test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.o: ../test/openvslam/data/common_get_cell_indices.cc
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/conor/msc-project/openvslam/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.o"
	cd /home/conor/msc-project/openvslam/build/test && /usr/bin/c++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.o -c /home/conor/msc-project/openvslam/test/openvslam/data/common_get_cell_indices.cc

test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.i"
	cd /home/conor/msc-project/openvslam/build/test && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/conor/msc-project/openvslam/test/openvslam/data/common_get_cell_indices.cc > CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.i

test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.s"
	cd /home/conor/msc-project/openvslam/build/test && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/conor/msc-project/openvslam/test/openvslam/data/common_get_cell_indices.cc -o CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.s

test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.o.requires:

.PHONY : test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.o.requires

test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.o.provides: test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.o.requires
	$(MAKE) -f test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/build.make test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.o.provides.build
.PHONY : test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.o.provides

test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.o.provides.build: test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.o


# Object files for target test_openvslam_data_common_get_cell_indices
test_openvslam_data_common_get_cell_indices_OBJECTS = \
"CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.o"

# External object files for target test_openvslam_data_common_get_cell_indices
test_openvslam_data_common_get_cell_indices_EXTERNAL_OBJECTS =

test/test_openvslam_data_common_get_cell_indices: test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.o
test/test_openvslam_data_common_get_cell_indices: test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/build.make
test/test_openvslam_data_common_get_cell_indices: lib/libopenvslam.so
test/test_openvslam_data_common_get_cell_indices: test/helper/libtest_helper.so
test/test_openvslam_data_common_get_cell_indices: lib/libgtest_main.a
test/test_openvslam_data_common_get_cell_indices: /usr/lib/x86_64-linux-gnu/libyaml-cpp.so.0.5.2
test/test_openvslam_data_common_get_cell_indices: /usr/local/lib/libopencv_calib3d.so.3.4.0
test/test_openvslam_data_common_get_cell_indices: /usr/local/lib/libopencv_features2d.so.3.4.0
test/test_openvslam_data_common_get_cell_indices: /usr/local/lib/libopencv_highgui.so.3.4.0
test/test_openvslam_data_common_get_cell_indices: /usr/local/lib/libopencv_videoio.so.3.4.0
test/test_openvslam_data_common_get_cell_indices: /usr/local/lib/libopencv_imgcodecs.so.3.4.0
test/test_openvslam_data_common_get_cell_indices: /usr/local/lib/libopencv_imgproc.so.3.4.0
test/test_openvslam_data_common_get_cell_indices: /usr/local/lib/libopencv_flann.so.3.4.0
test/test_openvslam_data_common_get_cell_indices: /usr/local/lib/libg2o_types_sim3.so
test/test_openvslam_data_common_get_cell_indices: /usr/local/lib/libg2o_types_sba.so
test/test_openvslam_data_common_get_cell_indices: /usr/local/lib/libg2o_types_slam3d.so
test/test_openvslam_data_common_get_cell_indices: /usr/local/lib/libg2o_solver_dense.so
test/test_openvslam_data_common_get_cell_indices: /usr/local/lib/libg2o_solver_eigen.so
test/test_openvslam_data_common_get_cell_indices: /usr/local/lib/libg2o_solver_csparse.so
test/test_openvslam_data_common_get_cell_indices: /usr/local/lib/libg2o_core.so
test/test_openvslam_data_common_get_cell_indices: /usr/local/lib/libg2o_stuff.so
test/test_openvslam_data_common_get_cell_indices: /usr/local/lib/libg2o_csparse_extension.so
test/test_openvslam_data_common_get_cell_indices: /usr/lib/x86_64-linux-gnu/libcxsparse.so
test/test_openvslam_data_common_get_cell_indices: /usr/lib/x86_64-linux-gnu/libccolamd.so
test/test_openvslam_data_common_get_cell_indices: /usr/lib/x86_64-linux-gnu/libcamd.so
test/test_openvslam_data_common_get_cell_indices: /usr/lib/x86_64-linux-gnu/libcolamd.so
test/test_openvslam_data_common_get_cell_indices: /usr/lib/x86_64-linux-gnu/libamd.so
test/test_openvslam_data_common_get_cell_indices: /usr/lib/liblapack.so
test/test_openvslam_data_common_get_cell_indices: /usr/lib/libf77blas.so
test/test_openvslam_data_common_get_cell_indices: /usr/lib/libatlas.so
test/test_openvslam_data_common_get_cell_indices: /usr/lib/libf77blas.so
test/test_openvslam_data_common_get_cell_indices: /usr/lib/libatlas.so
test/test_openvslam_data_common_get_cell_indices: /usr/lib/x86_64-linux-gnu/libsuitesparseconfig.so
test/test_openvslam_data_common_get_cell_indices: /usr/lib/x86_64-linux-gnu/librt.so
test/test_openvslam_data_common_get_cell_indices: /usr/local/lib/libdbow2.so
test/test_openvslam_data_common_get_cell_indices: /usr/local/lib/libopencv_core.so.3.4.0
test/test_openvslam_data_common_get_cell_indices: lib/libgtest.a
test/test_openvslam_data_common_get_cell_indices: test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/conor/msc-project/openvslam/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable test_openvslam_data_common_get_cell_indices"
	cd /home/conor/msc-project/openvslam/build/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/build: test/test_openvslam_data_common_get_cell_indices

.PHONY : test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/build

test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/requires: test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/openvslam/data/common_get_cell_indices.cc.o.requires

.PHONY : test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/requires

test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/clean:
	cd /home/conor/msc-project/openvslam/build/test && $(CMAKE_COMMAND) -P CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/cmake_clean.cmake
.PHONY : test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/clean

test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/depend:
	cd /home/conor/msc-project/openvslam/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/conor/msc-project/openvslam /home/conor/msc-project/openvslam/test /home/conor/msc-project/openvslam/build /home/conor/msc-project/openvslam/build/test /home/conor/msc-project/openvslam/build/test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : test/CMakeFiles/test_openvslam_data_common_get_cell_indices.dir/depend
