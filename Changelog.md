# Changelog
All notable changes to this project will be documented in this file

[unreleased]: https://github.com/eugenesvk/sublime-expand-selection-to-quotes/compare/0.2.0...HEAD
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
