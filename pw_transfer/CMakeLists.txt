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

pw_add_module_library(pw_transfer
  PUBLIC_DEPS
    pw_assert
    pw_bytes
    pw_containers
    pw_result
    pw_status
    pw_stream
    pw_transfer.proto.raw_rpc
  PRIVATE_DEPS
    pw_log
    pw_transfer.proto.pwpb
  TEST_DEPS
    pw_rpc.test_utils
)

pw_proto_library(pw_transfer.proto
  SOURCES
    transfer.proto
  PREFIX
    pw_transfer
)
