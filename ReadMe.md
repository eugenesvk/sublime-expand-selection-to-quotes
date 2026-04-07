Expands selections to the closest containing pairs of `'single'` or `"double"` quotes or ``` `backticks` ```.

The default keybinding (disabled to avoid conflicts) <kbd>⌃</kbd><kbd>'</kbd> (<kbd>⌘</kbd><kbd>'</kbd> on macOS), see [## Configure]

(`⎀` is cursor location, `•` denotes selection range, `←` `→` are reference markers)

  - `"•Double quoted ⎀ string selected•"`
  - `"Double quoted outer '•inner ⎀ selected•' ignored"`
  - `"•Double quoted outer 'inner string ignored' ⎀ selected•"`

Some language-awareness built-in:

```py
a = '•Single quoted selected, \"\' esc⎀ped \'\" quotes ignored •'
b = "•Double quoted selected, \"\' esc⎀ped \'\" quotes ignored •"
c = '•Ignore shorter pair of →" ⎀•'  +  '"← because this is a different string'
```

## Known issues

  - Limited language-awareness:
    - only `constant.character.escape` scope defines escape chars
    - only `meta.string` `string.quoted.single` `string.quoted.double` scopes define string limit
    - scopes are not language-specific
    - !configure your own and submit a PR if you find good universal options!

## Configure

  - Quote symbols / escape / string definition rules:
    - Run command: `Preferences: Expand Selection to Quotes`
    - Open menu: `Preferences` • `Package Settings` • `Q̲ Expand Selection to Quotes` • `Q̲ Settings – Default+User` (Win: <kbd>⎇</kbd><kbd>N</kbd>, <kbd>P</kbd>, <kbd>Q</kbd>, <kbd>Q</kbd>)
    - Copy the opened default `Expand Selection to Quotes.sublime-settings` template to your config and follow its instructions
  - Key bindings:
    - Run command: `Preferences: Expand Selection to Quotes Key Bindings`
    - Open menu `Preferences` • `Package Settings` • `Q̲ Expand Selection to Quotes` • `E̲ Key Bindings – Default+User` (Win: <kbd>⎇</kbd><kbd>N</kbd>, <kbd>P</kbd>, <kbd>Q</kbd>, <kbd>E</kbd>)
