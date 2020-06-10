
# Fire for C++

Fire for C++, inspired by [python-fire](https://github.com/google/python-fire), is a library that creates a command line interface from function signature. Here's a program that adds two numbers from command line:
 ```
#include <iostream>
#include <fire.hpp>

int fired_main(int x = fire::arg("x"), int y = fire::arg("y")) {
    std::cout << x + y << std::endl;
    return 0;
}

FIRE(fired_main)
```

That's it. And usage:

```
$ ./add -x=1 -y=2
3
```

As you likely expect,
* `--help` prints a meaningful message with required arguments and their types.
* an error message is displayed for incorrect usage.

### What's covered?

All the standard stuff, like
* flags; named and positional parameters; variable number of parameters
* optional parameters/default values
* conversions to integer, floating-point and `std::string`
* parameter descriptions
* typical constructs, such as expanding `-abc <=> -a -b -c` and `-x=1 <=> -x 1`

In addition, this library
* ~~works with Linux, Windows and Mac OS~~
* is a single header
* comes under very permissive [Boost licence](https://choosealicense.com/licenses/bsl-1.0/) (examples with [0-clause BSD](https://choosealicense.com/licenses/0bsd/))

## Q. Quick start

### Q.1 Requirements

* C++11 compatible compiler
* Compiling examples: CMake 3.1+
* Compiling/running tests: CMake 3.11+ and Python 3.5+

GTest is downloaded, compiled and linked automatically.

### Q.2 Running examples

Steps to run examples:
* Clone repo: `git clone https://github.com/kongaskristjan/fire-hpp`
* Create build and change directory: `cd fire-hpp && mkdir build && cd build`
* Configure/build: `cmake .. && cmake --build .` (or substitute latter command with appropriate build system invocation, eg. `make -j8` or `ninja`)
* Run: `./examples/basic --help` or `./examples/basic -x=3 -y=5` 

## T. Tutorial

Let's go through each part of the following example.

```
int fired_main(int x = fire::arg("x"), int y = fire::arg("y")) { // Define and convert arguments
    std::cout << x + y << std::endl;
    return 0;
}

FIRE(fired_main) // call fired_main()
```

* <a id="tutorialfire"></a> __FIRE(function name)__
`FIRE(fired_main)` expands into the actual `main()` function that defines your program's entry point and fires off `fired_main()`. `fired_main` is called without arguments, thus compiler is forced to use the default `fire::arg` values.

* __fire::arg(identifier)__
 A constructor that accepts the name/shorthand/position of the argument. The library prepends a single dash to single-character shorthands and two dashes to multi-character names (eg. `-x` and `--longer-name`). `fire::arg` objects should be used as default values for fired function parameters. See [documentation](#d_fire_arg) for more options.

* __int fired_main(arguments)__
This is your perceived program entry point. All arguments must be `bool`, integral, floating-point, `fire::optional<T>`, `std::string` or `std::vector<T>` type and default initialized with `fire::arg` objects (Failing to initialize properly results in undefined behaviour!). See [conversions](#d_arg_conversions) to learn how each of them changes the CLI.

## D. Documentation

### <a id="d_fire"></a> D.1 FIRE(...) and FIRE_NO_SPACE_ASSIGNMENT(...)

See `FIRE(...)` [quick start](#tutorialfire).

`FIRE(...)` and `FIRE_NO_SPACE_ASSIGNMENT(...)` both create a main function to parse arguments and call `...`, however they differ in how arguments are parsed. `FIRE(...)` parses `program -x 1` as `program -x=1`, but `FIRE_NO_SPACE_ASSIGNMENT(...)` parses `-x` as a flag and `1` as a positional argument.

In order to use positional or vector arguments, `FIRE_NO_SPACE_ASSIGNMENT(...)` must be used. There a two reasons:

* Mixing positional and named arguments with space separated values makes a bad CLI anyway, eg: `program a -x b c` doesn't seem like `-x=b` with `a` and `c` as positional.
* Implementing such a CLI within Fire API is rather complex, and likely even impossible without using exceptions.
 
 There is plan to lift this restriction in v0.3 for builds supporting exceptions.

### D.2 <a id="d_fire_arg"></a> fire::arg(identifier[, description[, default_value]])

#### D.2.1 Identifier

Identifier used to find arguments from command line. Can either be
* `const char * name`: named argument
    * Example: `int fired_main(int x = fire::arg("x"));`
    * CLI usage: `program -x=1`


* `{const char * shorthand, const char * full_name}`: named argument with a short-hand (single character) and long name
    * Example: `int fired_main(int x = fire::arg({"x", "long-name"}));`
    * CLI usage: `program -x=1`
    * CLI usage: `program --long-name=1`


* `int position`: positional argument (requires [no space assignment mode](#d_fire))
    * Example: `int fired_main(int x = fire::arg(0));`
    * CLI usage: `program 1`


* `{int position, const char * name}`: positional argument with name (name is only used for help) (requires [no space assignment mode](#d_fire))
    * Example: `int fired_main(int x = fire::arg(0));`
    * CLI usage: `program 1`

#### D.2.2 Descrpition (optional)

`std::string` argument description for `--help` message.

* Example: `int fired_main(int x = fire::arg("x", "an argument"));`
* CLI usage: `program --help`
* Output:
```
    Usage:
      ./examples/basic -x=<INTEGER>


    Options:
      -x=<INTEGER>  an argument
```

#### D.2.3 Default value (optional)

Default value if no value is provided through command line. `std::string`, integral or floating point type. This default is also displayed in help page.

* Example: `int fired_main(int x = fire::arg("x", "", 0));`
* CLI usage: `program` -> `x==0`
* CLI usage: `program -x=1` -> `x==1`

### <a id="d_arg_conversions"></a> D.3 fire::arg conversions

In order to conveniently obtain parsed arguments and automatically check the validity of input, `fire::arg` class defines several implicit conversions.

#### D.3.1 std::string, integral, or floating point

Converts the argument value on command line to respective type. Displayes an error if conversion is impossible or default value has wrong type.

* Example: `int fired_main(std::string name = fire::arg("name"));`
* CLI usage: `program --name=fire` -> `name=="fire"`

#### D.3.2 fire::optional

Used for optional arguments without a reasonable default value. This way the default value doesn't get printed in a help message. The underlying type can be `std::string`, integral or floating point.

`fire::optional` is a tear-down version of [`std::optional`](https://en.cppreference.com/w/cpp/utility/optional), with compatible implementations for [`has_value()`](https://en.cppreference.com/w/cpp/utility/optional/operator_bool), [`value_or()`](https://en.cppreference.com/w/cpp/utility/optional/value_or) and [`value()`](https://en.cppreference.com/w/cpp/utility/optional/value).

* Example: `int fired_main(fire::optional<std::string> name = fire::arg("name"));`
* CLI usage: `program` -> `name.has_value()==false`
* CLI usage: `program --name="fire"` -> `name.has_value()==true` and `name.value()=="fire"`

#### D.3.3 bool: flag argument

Boolean flags are `true` when they exist on command line and `false` when they don't. Multiple single-character flags can be packed on command line by prefixing with a single hyphen: `-abc <=> -a -b -c`

* Example: `int fired_main(bool flag = fire::arg("flag"));`
* CLI usage: `program` -> `flag==false`
* CLI usage: `program --flag` -> `flag==true`

### D.4 fire::arg::vector([description])

A method for getting all positional arguments (requires [no space assignment mode](#d_fire)). The constructed object can be converted to `std::vector<std::string>`, `std::vector<integral type>` or `std::vector<floating-point type>`. Description can be supplied for help message. Using `fire::arg::vector` forbids extracting positional arguments with `fire::arg(index)`.

* Example: `int fired_main(vector<std::string> params = fire::arg::vector());`
* CLI usage: `program abc xyz` -> `params=={"abc", "xyz"}`
* CLI usage: `program` -> `params=={}`

## Development

This library uses extensive testing. Unit tests are located in `tests/`, while `examples/` are used as integration tests. The latter also ensure examples are up-to-date. Before committing, please verify `python3 ./build/tests/run_standard_tests.py` succeed.

v0.1 release is tested on:
* Arch Linux gcc==10.1.0, clang==10.0.0: C++11, C++14, C++17 and C++20
* Ubuntu 18.04 clang=={3.5, 3.6, 3.7, 3.8, 3.9}: C++11, C++14 and clang=={4.0, 5.0, 6.0, 7.0, 8.0, 9.0}: C++11, C++14 and C++17
* Ubuntu 18.04 gcc=={4.8, 4.9}: C++11 and gcc=={5.5, 6.5, 7.5, 8.4}: C++11, C++14 and C++17
* Windows 10, MSVC=={19.26} (2019 Build Tools): C++11, C++14 and C++17

### TODO list:

#### Current state

* Test on Mac

#### v0.1 release

* Automatic testing for error messages
* Improve help messages
    * Refactor `log_elem::type` from `std::string` -> `enum class`
    * Help messages with better organization (separate positional arguments, named arguments, flags, etc. in `Usage` and descriptions)
    * Program description
* Ensure API user gets error message when using required positional arguments after optional positional arguments
* `save(...)` keyword enclosing `arg`, which will save program from exiting even if not all required arguments are present or correct (eg. for `--version`)
* `program --flags  --  --interpret-everything-as-positional-arguments-after-double-dash`
* Remove exceptions

#### v0.2 release

* If exceptions are still enabled, allow positional arguments in both FIRE(...) and FIRE_NO_SPACE_ASSIGNMENT(...)
* Subcommands (with separate help messages for each subcommand)
