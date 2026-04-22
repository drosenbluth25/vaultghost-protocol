# Contributing

This repository is maintained by Daniel Rosenbluth ([@drosenbluth25](https://github.com/drosenbluth25)).

## Before Opening a Pull Request

- All pull requests require code-owner review before merge.
- All commits to the default branch must be GPG- or SSH-signed.
  GitHub will reject unsigned commits on protected branches.
- Open an issue first for any non-trivial change to discuss scope.

## Signed Commits

To sign commits with GPG:

```sh
git config --global user.signingkey <YOUR_KEY_ID>
git config --global commit.gpgsign true
```

Or with an SSH key (Git 2.34+):

```sh
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

GitHub will display a **Verified** badge on signed commits once your key is registered
at [github.com/settings/keys](https://github.com/settings/keys).

## Canonical Source Files

- `.md` and `.html` source files are canonical.
- PDFs and other derived artifacts are generated snapshots and are not committed.

## License

By contributing, you agree that your contributions are licensed under
the same terms as this repository. See `LICENSE`.
