# Changelog
All notable changes to this project will be documented in this file

[unreleased]: https://github.com/eugenesvk/sublime-expand-selection-to-quotes/compare/0.3.9...HEAD
## [Unreleased]
<!-- - ✨ __Added__ -->
  <!-- + new features -->
<!-- - Δ __Changed__ -->
  <!-- + changes in existing functionality -->
<!-- - 🐞 __Fixed__ -->
  <!-- + bug fixes -->
<!-- - 💩 __Deprecated__ -->
  <!-- + soon-to-be removed features -->
<!-- - 🗑️ __Removed__ -->
  <!-- + now removed features -->
<!-- - 🔒 __Security__ -->
  <!-- + vulnerabilities -->

- 🐞 __Fixed__
  + cfg: fix wrong var name in warnings

[0.3.9]: https://github.com/eugenesvk/sublime-expand-selection-to-quotes/releases/tag/0.3.9
## [0.3.9]
- ✨ __Added__
  + command argument `c` to override any user settings

[0.3.8]: https://github.com/eugenesvk/sublime-expand-selection-to-quotes/releases/tag/0.3.8
## [0.3.8]
- ✨ __Added__
  + command arguments to break out of str/cmt scope jails, i.e., expand to valid quotes even if they are outside of the current string/comment scope
  + more custom commands to the command palette/selection menu/settings menu

[0.3.7]: https://github.com/eugenesvk/sublime-expand-selection-to-quotes/releases/tag/0.3.7
## [0.3.7]
- ✨ __Added__
  + `scope` argument to select strings by scope, not quote chars (and quotes by punctuation scopes, not chars)

[0.3.6]: https://github.com/eugenesvk/sublime-expand-selection-to-quotes/releases/tag/0.3.6
## [0.3.6]
- 🐞 __Fixed__
  + cfg: add missing cmt key

[0.3.5]: https://github.com/eugenesvk/sublime-expand-selection-to-quotes/releases/tag/0.3.5
## [0.3.5]
- 🐞 __Fixed__
  + dedupe quote counting when one pair is within the other: ``` `' ' ``` when counting closing `'` will include the opening since it's part of it

[0.3.4]: https://github.com/eugenesvk/sublime-expand-selection-to-quotes/releases/tag/0.3.4
## [0.3.4]
- ✨ __Added__
  + comment scope-awareness to limit search to contiguous comment scopes only

[0.3.3]: https://github.com/eugenesvk/sublime-expand-selection-to-quotes/releases/tag/0.3.3
## [0.3.3]
- 🐞 __Fixed__
  + remove hardcoded `"` and use custom one to calculate number of paired quotes within/outside the selected area

[0.3.2]: https://github.com/eugenesvk/sublime-expand-selection-to-quotes/releases/tag/0.3.2
## [0.3.2]
- ✨ __Added__
  + granular undo for a sequence of selection extension commands

[0.3.1]: https://github.com/eugenesvk/sublime-expand-selection-to-quotes/releases/tag/0.3.1
## [0.3.1]
- ✨ __Added__
  + scope-awareness to limit search to contiguous scopes only
- Δ __Changed__
  + 🧪 manual tests with automated ones

[0.3.0]: https://github.com/eugenesvk/sublime-expand-selection-to-quotes/releases/tag/0.3.0
## [0.3.0]

- ✨ __Added__
  + support for paired quotes «» ‹› ‘’ ‛’ “” ‟” „“ 🙶🙷 (user-configurable) as a command argument
  + command argument to select inclusive of quotation marks
- 🐞 __Fixed__
  + content/quote selection for 2-char quotes
  + search for quotes as regex, not literally

[0.2.0]: https://github.com/eugenesvk/sublime-expand-selection-to-quotes/releases/tag/0.2.0
## [0.2.0]

- ✨ __Added__
  + string-awareness to limit search to valid strings only `"ignore→' " + " '←ignore"`
  + reload user settings on update
  + basic user settings validation on load
  + basic (manual) 🧪tests
- Δ __Changed__
  + use scopes to skip escape-quotes instead of error-prone manual escape char searching
- 🐞 __Fixed__
  + Config typo
  + Breaking on empty scopes in user config

[0.1.2]: https://github.com/eugenesvk/sublime-expand-selection-to-quotes/releases/tag/0.1.2
## [0.1.2]

- 🐞 __Fixed__
  + Config typo

[0.1.1]: https://github.com/eugenesvk/sublime-expand-selection-to-quotes/releases/tag/0.1.1
## [0.1.1]

- 🐞 __Fixed__
  + Quotes acting as escapes not being ignored, e.g., newline escapes in ``` "`nhello`n" ``` (limited language example only)

[0.1.0]: https://github.com/eugenesvk/sublime-expand-selection-to-quotes/releases/tag/0.1.0
## [0.1.0]

- ✨ __Added__
  + Language-specific escapes `"\" in Markdown"` or ```"`" in AutoHotkey"```
  + Language-specific quote-self-escapes like `"Ends with a quote"""` in AutoHotkey
  + Support for `Expand Selection To Quotes.sublime-settings` to configure escapes
  + Menu options to open keybinds/settings
  + Commands to open keybinds/settings

- 🐞 __Fixed__
  + Escaped quotes not being ignored `"ignore →\"← this"`

[0.0.2]: https://github.com/eugenesvk/sublime-expand-selection-to-quotes/releases/tag/0.0.2
## [0.0.2]

- Δ __Changed__
  + Plugin host version to Python 3.8

[0.0.1]: https://github.com/eugenesvk/sublime-expand-selection-to-quotes/releases/tag/0.0.1
## [0.0.1]

- Δ __Changed__
  + Removed default keybinds to avoid conflicts with user configuration
