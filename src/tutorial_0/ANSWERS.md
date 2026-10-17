##Answers to Questionnaire

1. Mostly yes, package, module, function and member names follow PEP 8. But the classes libpy2 and libpy3 should be CamelCase (LibPy2, LibPy3).

2. No, because the environment is built with colcon build --symlink-install, it links the installed files to the source files instead of copying them, so edits to existing Python files take effect right away.

3. Recompiling is needed when the package structure or metadata changes: new files, new entry points or data files in setup.py, new dependencies in package.xml, new packages, custom message or service definitions, or any C++ code. Editing existing Python files doesn't require a rebuild when you use --symlink-install.