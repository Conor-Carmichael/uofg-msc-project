set(file "/home/conor/msc-project/openvslam/build/googletest-download/googletest-download-prefix/src/release-1.10.0.tar.gz")
message(STATUS "verifying file...
     file='${file}'")
set(expect_value "9c89be7df9c5e8cb0bc20b3c4b39bf7e82686770")
set(attempt 0)
set(succeeded 0)
while(${attempt} LESS 3 OR ${attempt} EQUAL 3 AND NOT ${succeeded})
  file(SHA1 "${file}" actual_value)
  if("${actual_value}" STREQUAL "${expect_value}")
    set(succeeded 1)
  elseif(${attempt} LESS 3)
    message(STATUS "SHA1 hash of ${file}
does not match expected value
  expected: ${expect_value}
    actual: ${actual_value}
Retrying download.
")
    file(REMOVE "${file}")
    execute_process(COMMAND ${CMAKE_COMMAND} -P "/home/conor/msc-project/openvslam/build/googletest-download/googletest-download-prefix/src/googletest-download-stamp/download-googletest-download.cmake")
  endif()
  math(EXPR attempt "${attempt} + 1")
endwhile()

if(${succeeded})
  message(STATUS "verifying file... done")
else()
  message(FATAL_ERROR "error: SHA1 hash of
  ${file}
does not match expected value
  expected: ${expect_value}
    actual: ${actual_value}
")
endif()
