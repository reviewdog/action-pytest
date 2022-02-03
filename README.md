# action-pytest

[![Test](https://github.com/reviewdog/action-pytest/workflows/Test/badge.svg)](https://github.com/reviewdog/action-pytest/actions?query=workflow%3ATest)
[![reviewdog](https://github.com/reviewdog/action-pytest/workflows/reviewdog/badge.svg)](https://github.com/reviewdog/action-pytest/actions?query=workflow%3Areviewdog)
[![depup](https://github.com/reviewdog/action-pytest/workflows/depup/badge.svg)](https://github.com/reviewdog/action-pytest/actions?query=workflow%3Adepup)
[![release](https://github.com/reviewdog/action-pytest/workflows/release/badge.svg)](https://github.com/reviewdog/action-pytest/actions?query=workflow%3Arelease)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/reviewdog/action-pytest?logo=github&sort=semver)](https://github.com/reviewdog/action-pytest/releases)
[![action-bumpr supported](https://img.shields.io/badge/bumpr-supported-ff69b4?logo=github&link=https://github.com/haya14busa/action-bumpr)](https://github.com/haya14busa/action-bumpr)

## Input

<!-- TODO: update -->
```yaml
inputs:
  github_token:
    description: 'GITHUB_TOKEN'
    default: '${{ github.token }}'
  workdir:
    description: 'Working directory relative to the root directory.'
    default: '.'
  ### Flags for reviewdog ###
  level:
    description: 'Report level for reviewdog [info,warning,error]'
    default: 'error'
  reporter:
    description: 'Reporter of reviewdog command [github-pr-check,github-check,github-pr-review].'
    default: 'github-pr-check'
  filter_mode:
    description: |
      Filtering mode for the reviewdog command [added,diff_context,file,nofilter].
      Default is added.
    default: 'added'
  fail_on_error:
    description: |
      Exit code for reviewdog when errors are found [true,false]
      Default is `false`.
    default: 'false'
  reviewdog_flags:
    description: 'Additional reviewdog flags'
    default: ''
  ### Flags for pytest ###
```

## Usage

```yaml
name: reviewdog
on: [pull_request]
jobs:
  pytest:
    name: runner / pytest
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: reviewdog/action-pytest@v1
        with:
          github_token: ${{ secrets.github_token }}
          # Change reviewdog reporter if you need [github-pr-check,github-check,github-pr-review].
          reporter: github-pr-review
          # Change reporter level if you need.
          # GitHub Status Check won't become failure with warning.
          level: warning
```

## Inputs

### `github_token`

**Required**. The [GITHUB_TOKEN](https://docs.github.com/en/free-pro-team@latest/actions/reference/authentication-in-a-workflow). Must be in form of `github_token: ${{ secrets.github_token }}`. Defaults to `${{ github.token }}`.

### `workdir`

**Optional**. The directory to run pytest on. Defaults to `.`.

#### `pytest_args`

**Optional**. Command-line arguments to the pytest executable. Defaults to `""`.

Please note that some command-line arguments can be defined with other fields in your configuration.  You may combine the `pytest_args` setting with the other settings below, or use `pytest_args` to configure pytest without the other Action settings.

#### `level`

**Optional**. The log level of the reviewdog reporter. Options: `[info, warning, error]`. Defaults to `error`.

#### `reporter`

**Optional**. Reporter of reviewdog command `[github-pr-check, github-pr-review, github-check]`. Defaults to `github-pr-check`.

#### `filter_mode`

**Optional**. Filtering mode for the reviewdog command `[added, diff_context, file, nofilter]`. Defaults to `added`.

#### `fail_on_error`

**Optional**. Exit code for reviewdog when errors are found `[true, false]`. Defaults to `false`.

#### `reviewdog_flags`

**Optional**. Additional reviewdog flags. Defaults to `""`.

#### `tool_name`

**Optional**. Tool name to use for reviewdog reporter. Defaults to `pytest`.

## Development

### Release

#### [haya14busa/action-bumpr](https://github.com/haya14busa/action-bumpr)
You can bump version on merging Pull Requests with specific labels (bump:major,bump:minor,bump:patch).
Pushing tag manually by yourself also work.

#### [haya14busa/action-update-semver](https://github.com/haya14busa/action-update-semver)

This action updates major/minor release tags on a tag push. e.g. Update v1 and v1.2 tag when released v1.2.3.
ref: https://help.github.com/en/articles/about-actions#versioning-your-action

### Lint - reviewdog integration

This reviewdog action is integrated with reviewdog to run lints
which is useful for Docker container based actions.

![reviewdog integration](https://user-images.githubusercontent.com/3797062/72735107-7fbb9600-3bde-11ea-8087-12af76e7ee6f.png)

Supported linters:

- [reviewdog/action-shellcheck](https://github.com/reviewdog/action-shellcheck)
- [reviewdog/action-hadolint](https://github.com/reviewdog/action-hadolint)
- [reviewdog/action-misspell](https://github.com/reviewdog/action-misspell)

### Dependencies Update Automation
This repository uses [reviewdog/action-depup](https://github.com/reviewdog/action-depup) to update
reviewdog version.

[![reviewdog depup demo](https://user-images.githubusercontent.com/3797062/73154254-170e7500-411a-11ea-8211-912e9de7c936.png)](https://github.com/reviewdog/action-pytest/pull/6)
