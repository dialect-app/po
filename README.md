# Translations

<a href="https://hosted.weblate.org/engage/dialect/">
<img src="https://hosted.weblate.org/widgets/dialect/-/dialect/svg-badge.svg" alt="Translation status" />
</a>

This repository contains all translations of Dialect.

Dialect is a translation application, meaning it's intended to help get over language barriers, so we believe UI translation to be an essential part of the application's development. As such, we really appreciate all the work put into it! :)

Dialect has been translated into the following languages:

<a href="https://hosted.weblate.org/engage/dialect/">
<img src="https://hosted.weblate.org/widgets/dialect/-/dialect/multi-auto.svg" alt="Translation status" />
</a>

## Languages names translations

Translations for language names are automatically generated from the [Unicode CLDR Project](https://cldr.unicode.org/) data. You can contribute there if translations for your language are missing.

### Generation script

#### How to use

```bash
git clone https://github.com/dialect-app/po
pip install polib
python gen_cldr_langs.py
```

The script needs `polib` to run.

`gen_cldr_langs.py` should be run with `po/` as the working directory and will not work as expected otherwise.

#### How to contribute

The `gen_cldr_langs.py` script has a few things you could help with as well:

- If your language is named differently in the Unicode CLDR project, add a mapping in `CLDR_NAMES`.
