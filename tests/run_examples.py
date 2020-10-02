
"""
    Copyright Kristjan Kongas 2020

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

import subprocess, json
from pathlib import Path

fire_failure_code = 1

class assert_runner:
    test_count = 0
    check_count = 0

    def __init__(self, pth):
        self.pth = str(pth)
        assert_runner.test_count += 1
        self.help_success("-h")
        self.help_success("--help")

    def equal(self, cmd, out):
        result = subprocess.run([self.pth] + cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert result.returncode == 0
        assert self.remove_newline(self.b2str(result.stdout.strip())) == self.remove_newline(out.strip())
        assert result.stderr == b""
        assert_runner.check_count += 1

    def handled_failure(self, cmd):
        result = subprocess.run([self.pth] + cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert result.returncode == fire_failure_code
        assert result.stdout == b""
        assert result.stderr != b""
        assert_runner.check_count += 1

    def help_success(self, cmd):
        result = subprocess.run([self.pth] + cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert result.returncode == 0
        assert_runner.check_count += 1

    def remove_newline(self, strn):
        return strn.replace("\r", "").replace("\n", "")

    def b2str(self, b):
        return str(b, "utf-8")


def run_all_combinations(path_prefix):
    runner = assert_runner(path_prefix / "all_combinations")

    runner.equal("0 -i=0", "")
    runner.equal("0 1 -i=0 --def-r=0.0 --opt-s=string", "")
    runner.equal("0 1 -i 0 --def-r 0.0 --opt-s string", "")


def run_basic(path_prefix):
    runner = assert_runner(path_prefix / "basic")

    runner.equal("-x 3 -y 4", "3 + 4 = 7")
    runner.equal("-x -3 -y 3", "-3 + 3 = 0")
    runner.equal("-x=-3 -y=3", "-3 + 3 = 0")
    runner.handled_failure("")
    runner.handled_failure("-x 3")
    runner.handled_failure("-y 4")
    runner.handled_failure("-x test")
    runner.handled_failure("-x")
    runner.handled_failure("--undefined 0")
    runner.help_success("-x 0 -h")
    runner.help_success("-h --undefined")


def run_flag(path_prefix):
    runner = assert_runner(path_prefix / "flag")

    runner.equal("", "flag-a: false   flag-b: false")
    runner.equal("-a -b", "flag-a: true   flag-b: true")
    runner.equal("-ab", "flag-a: true   flag-b: true")
    runner.equal("--flag-a", "flag-a: true   flag-b: false")
    runner.equal("--flag-b", "flag-a: false   flag-b: true")
    runner.handled_failure("-a 1")


def run_optional_and_default(path_prefix):
    runner = assert_runner(path_prefix / "optional_and_default")

    runner.equal("", "optional: [no value]\ndefault: 0")
    runner.equal("--default 1", "optional: [no value]\ndefault: 1")
    runner.equal("--optional -1", "optional: -1\ndefault: 0")
    runner.equal("--optional -1 --default 1", "optional: -1\ndefault: 1")


def run_positional(path_prefix):
    runner = assert_runner(path_prefix / "positional")

    runner.handled_failure("")
    runner.handled_failure("test")
    runner.equal("2", "2 0")
    runner.equal("2 3", "2 3")
    runner.handled_failure("2 3 4")
    runner.equal("-1 -3", "-1 -3")


def run_vector_positional(path_prefix):
    runner = assert_runner(path_prefix / "vector_positional")

    runner.equal("", "\n")
    runner.equal("b a", "b a\n")
    runner.equal("b a -o", "b\na\n")
    runner.equal("b a -s", "a b\n")
    runner.equal("b a -os", "a\nb\n")
    runner.equal("a -- -b", "a -b\n")


def run_no_exceptions(path_prefix):
    runner = assert_runner(path_prefix / "no_exceptions")

    runner.equal("", "\n")
    runner.equal("1 2", "1 2 \n")
    runner.equal("1 2 -r=2", "1 2 \n1 2 \n")


def get_path_prefix(subdir):
    cur_dir = Path(__file__).absolute().parent
    with (cur_dir / "build_dirs.json").open("r") as json_file:
        json_obj = json.load(json_file)
        return cur_dir / json_obj[subdir]


def main():
    path_prefix = get_path_prefix("examples")

    print("Running tests in {} ...".format(path_prefix), end="")

    run_all_combinations(path_prefix)
    run_basic(path_prefix)
    run_flag(path_prefix)
    run_optional_and_default(path_prefix)
    run_positional(path_prefix)
    run_vector_positional(path_prefix)

    run_no_exceptions(path_prefix)

    print(" SUCCESS! (ran {} tests with {} checks)".format(assert_runner.test_count, assert_runner.check_count))


if __name__ == "__main__":
    main()
