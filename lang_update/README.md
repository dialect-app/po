# Language Names Updater

This script tries to pull language names from the sources:

- Unicode CLDR
- Google Translate

## How to use

```bash
git clone https://github.com/dialect-app/po
cd po/lang_update
python lang_update.py
```

`lang_update.py` should be run with `po/lang_update` as the working directory and will not work as expected otherwise.

`-g` or `--google` can be passed to force the usage of Google Translate as the source for language names.

You can also pass a language code to only update one language:

```bash
python lang_update.py "ca"
```

## How to contribute

If you would like to work on language names, please contribute to [Unicode CLDR](https://cldr.unicode.org/).

If you decide that the language names from Unicode CLDR are not good enough and feel like you could do a better job, you can open an issue at [dialect-app/po](https://github.com/dialect-app/po/issues) and continue updating your translation as per usual. You could also instead add your language code to the `EXCLUDE_LIST` in the `lang_update.py` script and send a PR.

The `lang_update.py` script has a few things you could help with as well:

- The `EXCLUDE_LIST` list could be expanded or shortened depending on the accuracy of Unicode CLDR project's language names for a particular language. You could do this by checking `cldr-json`. For example: [French Unicode CLDR languages.json](https://github.com/unicode-org/cldr-json/blob/main/cldr-json/cldr-localenames-full/main/fr/languages.json) . The link format is:
  ```
  https://github.com/unicode-org/cldr-json/blob/main/cldr-json/cldr-localenames-full/main/{language_code_here}/languages.json
  ```
- If language names should be capitalized in your language, add the language code to `CAPS_LIST`.
- If your language is named differently in the Unicode CLDR project, add a mapping in `CLDR_NAMES`.
