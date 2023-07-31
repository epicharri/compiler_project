# Compilers project

## Mini-PL interpreter.

The program should be runnable using the development tools available at the Computer Science department of University of Helsinki, because it is written and tested using the computer managed by CS department. In the computer, the newest version of Python is Python 3.6.9, and it is used for running the program.

To interpret a program, give the file path of the source code file as the first parameter.

For example:

```
python3 minipl.py sample_programs/sample6.mpl
```

Notice you may have Python 3 as a default. Then, instead of `python3` you may use `python`.

In addition, you can use the following parameters:

| Parameter              | Description                                                            |
| ---------------------- | ---------------------------------------------------------------------- |
| `--print-tokens`       | To print tokens during parsing.                                        |
| `--print-ast`          | To print AST.                                                          |
| `--print-debug-info`   | To print information during debugging.                                 |
| `--print-symbol-table` | To print symbol table after parsing, semantic analysis, and execution. |

For example, to pretty print AST of the mini-PL program reachable in `sample_programs/sample6.mpl`, write the following.

```
python3 minipl.py sample_programs/sample6.mpl --print-ast
```
