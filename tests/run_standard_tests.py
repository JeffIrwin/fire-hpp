
"""
    Copyright Kristjan Kongas 2022

    Boost Software License - Version 1.0 - August 17th, 2003

    Permission is hereby granted, free of charge, to any person or organization
    obtaining a copy of the software and accompanying documentation covered by
    this license (the "Software") to use, reproduce, display, distribute,
    execute, and transmit the Software, and to prepare derivative works of the
    Software, and to permit third-parties to whom the Software is furnished to
    do so, all subject to the following:

    The copyright notices in the Software and this entire statement, including
    the above license grant, this restriction and the following disclaimer,
    must be included in all copies of the Software, in whole or in part, and
    all derivative works of the Software, unless such copies or derivative
    works are solely in the form of machine-executable object code generated by
    a source language processor.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
    SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
    FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
"""

import subprocess, sys, json
import run_examples
from pathlib import Path

def print_result(success):
    print()
    if success:
        print("++++++++          SUCCESS          ++++++++")
    else:
        print("--------        TEST FAILED        --------")
    print()


def run(pth):
    pth = str(pth)
    print("Running " + pth)
    result = subprocess.run(pth.split())
    if result.returncode != 0:
        print_result(False)
        sys.exit(1)


def get_path_prefix(subdir):
    cur_dir = Path(__file__).absolute().parent
    with (cur_dir / "build_dirs.json").open() as json_file:
        json_obj = json.load(json_file)
        return cur_dir, cur_dir / json_obj[subdir]


def main():
    cur_dir, path_prefix = get_path_prefix("run_tests")
    run(path_prefix / "run_tests")
    run_examples.main()
    run(path_prefix / "link_test")
    print_result(True)


if __name__ == "__main__":
    main()
