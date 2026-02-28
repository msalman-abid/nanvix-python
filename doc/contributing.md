# Contributing

Contributions are welcome! To get started:

1. Fork the repository and create a feature branch.
2. Run `./z setup && ./z build && ./z test` to verify your changes
   locally.
3. If adding a new statically linked C extension, add a documentation
   file in `patches/` following the existing `*_static_builtin.md`
   pattern.
4. If adding a new pip package, append it to the appropriate
   requirements file and create a matching
   `tests/func/test_NNN_<package>.py` test file.
5. Open a pull request — CI will automatically build and test all four
   platform configurations.

## Further Reading

- [Building from Source](building.md)
- [Statically Linked C Extensions](extensions.md)
- [Testing](testing.md)
- [Supported Packages](packages.md)
- [CI / CD](ci.md)
- [Standalone Runtime Bundle](release.md)
