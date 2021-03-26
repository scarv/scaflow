# [`scaflow`](https://github.com/scarv/scaflow): dataflow-based side-channel analysis

<!--- -------------------------------------------------------------------- --->

[![Build Status](https://travis-ci.com/scarv/scaflow.svg)](https://travis-ci.com/scarv/scaflow)
[![Documentation](https://codedocs.xyz/scarv/scaflow.svg)](https://codedocs.xyz/scarv/scaflow)

<!--- -------------------------------------------------------------------- --->

*Acting as a component part of the wider
[SCARV](https://www.scarv.org)
project,
`scaflow` is framework, and suite of associated tools, which allow
expression of side-channel analysis flows as
[dataflow programs](https://en.wikipedia.org/wiki/Dataflow_programming),
and
execution of those flows, where appropriate
[offloading](https://en.wikipedia.org/wiki/Computation_offloading)
computation to suitable resources.*

<!--- -------------------------------------------------------------------- --->

## Organisation

```
├── bin                     - scripts (e.g., environment configuration)
├── build                   - working directory for build
└── src
    └── scaflow             - source code for scaflow
```

<!--- -------------------------------------------------------------------- --->

## Quickstart

1. Install any associated pre-requisites, e.g.,

   - a
     [Python 3](https://www.python.org)
     distribution,
   - the
     [Doxygen](http://www.doxygen.nl)
     documentation generation system.

2. Execute

   ```sh
   git clone https://github.com/scarv/scaflow.git ./scaflow
   cd ./scaflow
   git submodule update --init --recursive
   source ./bin/conf.sh
   ```

   to clone and initialise the repository,
   then configure the environment;
   for example, you should find that the environment variable
   `REPO_HOME`
   is set appropriately.

3. Use targets in the top-level `Makefile` to drive a set of
   common tasks, e.g.,

   | Command                   | Description                                                                          |
   | :------------------------ | :----------------------------------------------------------------------------------- |
   | `make venv`               | build the Python [virtual environment](https://docs.python.org/library/venv.html)    |
   | `make doxygen`            | build the [Doxygen](http://www.doxygen.nl)-based documentation                       |
   | `make spotless`           | remove *everything* built in `${REPO_HOME}/build`                                    |

<!--- -------------------------------------------------------------------- --->

## Questions?

- read the
  [wiki](https://github.com/scarv/scaflow/wiki),
- raise an
  [issue](https://github.com/scarv/scaflow/issues),
- raise a
  [pull request](https://github.com/scarv/scaflow/pulls),
- drop us an
  [email](mailto:info@scarv.org?subject=scaflow).

<!--- -------------------------------------------------------------------- --->

## Acknowledgements

This work has been supported in part
by EPSRC via grant
[EP/R012288/1](https://gow.epsrc.ukri.org/NGBOViewGrant.aspx?GrantRef=EP/R012288/1) (under the [RISE](https://www.ukrise.org) programme).

<!--- -------------------------------------------------------------------- --->
