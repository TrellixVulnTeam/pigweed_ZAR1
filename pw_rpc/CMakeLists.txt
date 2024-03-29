# Copyright 2020 The Pigweed Authors
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

include($ENV{PW_ROOT}/pw_build/pigweed.cmake)
include($ENV{PW_ROOT}/pw_protobuf_compiler/proto.cmake)

if(NOT "${dir_pw_third_party_nanopb}" STREQUAL "")
  add_subdirectory(nanopb)
endif()

add_subdirectory(raw)
add_subdirectory(system_server)

pw_add_module_library(pw_rpc.server
  SOURCES
    responder.cc
    server.cc
    service.cc
  PUBLIC_DEPS
    pw_rpc.common
  PRIVATE_DEPS
    pw_log
)

pw_add_module_library(pw_rpc.client
  SOURCES
    base_client_call.cc
    client.cc
  PUBLIC_DEPS
    pw_rpc.common
  PRIVATE_DEPS
    pw_log
)

pw_add_module_library(pw_rpc.client_server
  SOURCES
    client_server.cc
  PUBLIC_DEPS
    pw_rpc.client
    pw_rpc.server
)

pw_add_module_library(pw_rpc.common
  SOURCES
    channel.cc
    packet.cc
  PUBLIC_DEPS
    pw_assert
    pw_bytes
    pw_containers
    pw_function
    pw_span
    pw_status
    pw_rpc.protos.pwpb
  PRIVATE_DEPS
    pw_log
)

pw_add_module_library(pw_rpc.synchronized_channel_output
  PUBLIC_DEPS
    pw_rpc.common
    pw_sync.mutex
)

pw_add_module_library(pw_rpc.test_utils
  SOURCES
    fake_channel_output.cc
  PUBLIC_DEPS
    pw_assert
    pw_bytes
    pw_rpc.client
    pw_rpc.server
)
target_include_directories(pw_rpc.test_utils PUBLIC .)

pw_proto_library(pw_rpc.protos
  SOURCES
    internal/packet.proto
    echo.proto
  INPUTS
    echo.options
  PREFIX
    pw_rpc
)

pw_proto_library(pw_rpc.test_protos
  SOURCES
    pw_rpc_test_protos/test.proto
)

pw_auto_add_module_tests(pw_rpc
  PRIVATE_DEPS
    pw_rpc.client
    pw_rpc.server
)
