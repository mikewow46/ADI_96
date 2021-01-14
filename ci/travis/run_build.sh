#!/bin/bash

set -ex

. ci/travis/lib.sh

build_default() {
    pushd "${TRAVIS_BUILD_DIR}"
    sudo mkdir -p build
    cd build
    sudo cmake -DCMAKE_PREFIX_PATH="${DEPS_DIR}/installed/glog;${DEPS_DIR}/installed/protobuf;${DEPS_DIR}/installed/websockets;${DEPS_DIR}/installed/Open3D;" ..
    sudo make -j${NUM_JOBS}
    popd
}

build_cppcheck() {
    check_cppcheck
}

build_clang_format() {
    check_clangformat
}

build_deploy_doxygen() {
    pushd "${TRAVIS_BUILD_DIR}/doc"
    mkdir build && cd build && cmake ..
    check_doxygen
    deploy_doxygen
    popd
}

build_dragonboard() {
    run_docker ${DOCKER} /aditof_sdk/ci/travis/inside_docker.sh -DDRAGONBOARD=TRUE
}

build_raspberrypi3() {
    run_docker ${DOCKER} /aditof_sdk/ci/travis/inside_docker.sh -DRASPBERRYPI=TRUE
}

build_ros(){
    pushd "${TRAVIS_BUILD_DIR}"
    cd build
    sudo cmake --build . --target install
    cmake --build . --target aditof_ros_package
    popd
}

build_${BUILD_TYPE:-default}
