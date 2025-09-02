#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os

# Tolerance to consider number zero.
EQ_TOLERANCE = 1e-8

# Molecular data directory.
THIS_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
DATA_DIRECTORY = os.path.realpath(os.path.join(THIS_DIRECTORY, 'testing/data'))


def check_file_size(file_path, max_size_mb=100):
    """
    Check if a file exceeds a certain size limit.

    Args:
        file_path (str): The path to the file.
        max_size_mb (int): The maximum file size in megabytes.

    Raises:
        ValueError: If the file size exceeds the limit.
    """
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > max_size_mb:
        raise ValueError(f"File size of {file_path} ({file_size_mb:.2f}MB) "
                         f"exceeds the limit of {max_size_mb}MB.")
