Expands selections to the closest containing pairs of `'single'` or `"double"` quotes or ``` `backticks` ```.

The default keybinding (disabled to avoid conflicts) <kbd>⌃</kbd><kbd>'</kbd> (<kbd>⌘</kbd><kbd>'</kbd> on macOS), see [## Configure]

(`⎀` is cursor location, `←` `→` is first/last selected characters)

  - `"←Double quoted ⎀ string selected→"`
  - `"Double quoted outer '←inner ⎀ selected→' ignored"`
  - `"←Double quoted outer 'inner string ignored' ⎀ selected→"`

Limited[^1][^2] language-awareness built-in

```py
a = '←Single quoted selected, \"\' esc⎀ped \'\" quotes ignored →'
b = "←Double quoted selected, \"\' esc⎀ped \'\" quotes ignored →"
```

But no string-awareness is built-in, so separation of strings is ignored:

```py
a = 'This \' is ignored, but this is not "← ⎀'  +  '→" '
```
Since the first `'string'` is not parsed as single text object, and the `"inner quotes"` are shorter than the `'outer'` ones


## Configure

  - Language-specific escape rules:
    - Run command: `Preferences: Expand Selection to Quotes`
    - Open menu: `Preferences` → `Package Settings` → `Q̲ Expand Selection to Quotes` → `Q̲ Settings – Default+User` (Win: <kbd>⎇</kbd><kbd>N</kbd>, <kbd>P</kbd>, <kbd>Q</kbd>, <kbd>Q</kbd>)
  - Key bindings:
    - Run command: `Preferences: Expand Selection to Quotes Key Bindings`
    - Open menu `Preferences` → `Package Settings` → `Q̲ Expand Selection to Quotes` → `E̲ Key Bindings – Default+User` (Win: <kbd>⎇</kbd><kbd>N</kbd>, <kbd>P</kbd>, <kbd>Q</kbd>, <kbd>E</kbd>)

[^1]: Only 1 `\`esc / 1 non-`\`esc language included as an example, the rest are configured to use `\` and escape `' "`, though it's user configurable (PRs to include more languages are welcome!)
[^2]: Requires precise matching, so if some syntax defines AutoHotkey as `source.ahk.1` or `source.ahk.2` depending on its version, the settings must include the versioned scope, and if other tools define it as a generic `source.ahk`, the settings must also include this general version
