# ToDo
  - add a guard against ending UP in a comment scope: helpful when you ignore jails but still don't want to mix scopes too much
  - ± (partially, List is, value Str types are not checked) test user config validity on import: types of values and existence of required keys in a dictionary
  - simplify config to accept a single value str `' " ‹› ‟”` or a list of str/list ``` [' " ‹› ‟”,   ["`'","'"]] ```
    - whitespace-separate
    - 1char: open=close=char
    - 2char: `s[0]`open  `s[1]`close
    - 2+char: must be a list with `l[0]` open and `l[1]` close
  - ? add a way to only search for quotes that form valid punctuation `.begin`/`.end` (at least limit this to normal `' " ` chars), this way
    - `x`←²  `←¹⎀¹→` will not extend to ²→`x`
    - why is this needed, not like you have nested strings like this, so can only select 1 begin/end?
  - ? add extra scopes to limit expansion similar to string/source (workaround: use `str+`/`cmt+`)
    - text language
# Testing
  - Add GitHub actions tests using the `UnitTesting` packages
# Perf
  - ? instead of finding all quotes of all types, find the nearest left/right unescaped quote and use that?
    - !especially if we're inside a string, not point in searching beyond
# Done
  - ± via custom symbols/scopes/jail_breaks add paired symbos like `[]` `{}` ??? (separate command? or maybe a different plugin which already exists)
    - sublime default only works on syntax, not symbols, so fails on plain text
      - doesn't support custom syntax
  + ✓ add command arguments that allow skipping safeguards like not jumping across source scope or string scope
  + ✓ add (every) command to the command panel
  + ✓ allow overriding all scopes on a per-command basic
  + add comment scope expansion limit
  + ✓ add more granular selection undo
  + ✓ limit search not only to strings scope, but also source. scope so that mixed scopes don't bleed into each other's quotes
  + ✓ write tests that automatically test for corret text selection
  + ✓ add another command argument to select inclusive of quotes
  + ✓ add paired quotes «» ‹› ‘’ ‛’ “” ‟” „“ 🙶🙷 
  + ✓ prioritize string scope so that Python's string selects the 1st string instead of `"disjointed"` quotations
    ```py
      '•1st string "⎀•' + '" 2nd string'
    ```
  + (no need, rely on scope matches) add more non\ escaping languages (custom symbol and quote repeats)
  - ✗ for plain text files bother with detecting apostrophes?
    - ✗ No, do it properly: use some plain texty grammar to parse
  - ✗ penalize newline within quotes so that ↓ works even without syntax highlighting parsing all the quotes properly
    - ✗ No, same thing - do it properly via grammar parsing
    ```
    a = 'test'
    b = "This shouldn't break"
    ```
