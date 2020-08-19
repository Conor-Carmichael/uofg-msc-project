if(EXISTS "/home/conor/msc-project/openvslam/build/googletest-download/googletest-download-prefix/src/release-1.10.0.tar.gz")
  file("SHA1" "/home/conor/msc-project/openvslam/build/googletest-download/googletest-download-prefix/src/release-1.10.0.tar.gz" hash_value)
  if("x${hash_value}" STREQUAL "x9c89be7df9c5e8cb0bc20b3c4b39bf7e82686770")
    return()
  endif()
endif()
message(STATUS "downloading...
     src='https://github.com/google/googletest/archive/release-1.10.0.tar.gz'
     dst='/home/conor/msc-project/openvslam/build/googletest-download/googletest-download-prefix/src/release-1.10.0.tar.gz'
     timeout='none'")




file(DOWNLOAD
  "https://github.com/google/googletest/archive/release-1.10.0.tar.gz"
  "/home/conor/msc-project/openvslam/build/googletest-download/googletest-download-prefix/src/release-1.10.0.tar.gz"
  
  # no TIMEOUT
  STATUS status
  LOG log)

list(GET status 0 status_code)
list(GET status 1 status_string)

if(NOT status_code EQUAL 0)
  message(FATAL_ERROR "error: downloading 'https://github.com/google/googletest/archive/release-1.10.0.tar.gz' failed
  status_code: ${status_code}
  status_string: ${status_string}
  log: ${log}
")
endif()

message(STATUS "downloading... done")
