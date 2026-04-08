Expands selections to the closest containing pairs of `'single'` or `"double"` quotes or ``` `backticks` ``` (user-configurable list of quotation marks).

The default keybinding (disabled to avoid conflicts) <kbd>⌃</kbd><kbd>'</kbd> (<kbd>⌘</kbd><kbd>'</kbd> on macOS):

(`⎀` is cursor location, `•` denotes selection range, `←` `→` are reference markers)

  - `"•Double quoted ⎀ string selected•"`
  - `"Double quoted outer '•inner ⎀ selected•' ignored"`
  - `"•Double quoted outer 'inner string ignored' ⎀ selected•"`

Supports ‘pair-different’ quotes via a `qp` command argument: `«guillemets»` `‹›` `‘curved’` `‛’` `“”` `‟”` `„“` `🙶heavy🙷` (≝keybind disabled to avoid conflicts: <kbd>⌃</kbd><kbd>"</kbd> (<kbd>⌘</kbd><kbd>"</kbd> on macOS))

  - `«•Double guillemet ⎀ string selected•»`
  - `“•Double fancy quotation ⎀ string selected•”`
  - `“ Double fancy quotation ‟•in⎀ner•” string selected”`
  - `" Double fancy quotation ‟•in⎀ner•” string selected"`

Can select quotes if called with an `inc` command argument (without one running the command twice expands to quotes)
  ```py
    "Double quotes inc=true"
  # •                      •
  ```

Some language-awareness built-in — escape quotes ignored, search scope limited to strings:

```py
a = '•Single quoted selected, \"\' esc⎀ped \'\" quotes ignored •'
b = "•Double quoted selected, \"\' esc⎀ped \'\" quotes ignored •"
c = '•Ignore shorter pair of →" ⎀•'  +  '"← because this is a different string'
d = '•Ignore shorter pair of →‟ ⎀•'  +  '”← because this is a different string'
d = ' Select …       …       →‟•⎀       •”←               the same      …     '
```

Likewise, you can add similar behavior to custom scopes, e.g., not break out of line comments:

```py
# requires user config modification:  "str+":["comment.line"]
a = "Hello don't break" #⎀'←do NOT break outside the comment scope'…
  # …to match ↑
```

## Configure

  - Quote symbols / escape / string definition rules:
    - Run command: `Preferences: Expand Selection to Quotes`
    - Open menu: `Preferences` ▶ `Package Settings` ▶ `Q̲ Expand Selection to Quotes` ▶ `Q̲ Settings – Default+User` (Win: <kbd>⎇</kbd><kbd>N</kbd>, <kbd>P</kbd>, <kbd>Q</kbd>, <kbd>Q</kbd>)
    - Copy the opened default `Expand Selection to Quotes.sublime-settings` template to your config and follow its instructions
  - Key bindings with quote-include / ‘pair-different’ quote arguments:
    - Run command: `Preferences: Expand Selection to Quotes Key Bindings`
    - Open menu `Preferences` ▶ `Package Settings` ▶ `Q̲ Expand Selection to Quotes` ▶ `E̲ Key Bindings – Default+User` (Win: <kbd>⎇</kbd><kbd>N</kbd>, <kbd>P</kbd>, <kbd>Q</kbd>, <kbd>E</kbd>)

## Known issues

  - Limited language-awareness:
    - only `constant.character.escape` scope defines escape chars
    - only `meta.string` `string.quoted.single` `string.quoted.double` scopes define string limit
    - scopes are not language-specific (good grammars should use standard/common scope names?)
    - !configure your own and submit a PR if you find good universal options!
  - Not all variants of ‘pair-different’ quotes are included due to _potential_ conflicts: `„“` but not `„”`. Add the missing ones to your config, exclude the ones you don't need, submit a PR (and tests) if the potential for conflict is only imaginary
