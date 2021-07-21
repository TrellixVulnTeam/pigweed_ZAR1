// Copyright 2021 The Pigweed Authors
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may not
// use this file except in compliance with the License. You may obtain a copy of
// the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations under
// the License.

#include "pw_rpc/benchmark.h"

#include <algorithm>

namespace pw::rpc {
namespace {

StatusWithSize CopyBuffer(ConstByteSpan input, ByteSpan output) {
  if (input.size() > output.size()) {
    return pw::StatusWithSize::ResourceExhausted();
  }
  std::copy(input.begin(), input.end(), output.begin());
  return pw::StatusWithSize(input.size());
}

}  // namespace

StatusWithSize BenchmarkService::UnaryEcho(ServerContext&,
                                           ConstByteSpan request,
                                           ByteSpan response) {
  return CopyBuffer(request, response);
}

void BenchmarkService::BidirectionalEcho(
    ServerContext&, RawServerReaderWriter& new_reader_writer) {
  reader_writer_ = std::move(new_reader_writer);

  reader_writer_.set_on_next([this](ConstByteSpan request) {
    Status status = reader_writer_.Write(request);
    if (!status.ok()) {
      reader_writer_.Finish(status);
    }
  });
}

}  // namespace pw::rpc
