# Copyright 2021 Mufeed Ali
# Copyright 2023 Rafael Mardojai CM
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import os
import subprocess
import polib

CLDR_NAMES = {
    "kmr": "ku",  # They seem to be the same since Kurmanji (ku) is Northern Kurdish (kmr).
    "zh_CN": "zh-Hans",
    "zh_TW": "zh-Hant",
    "zh-CN": "zh-Hans",
    "zh-TW": "zh-Hant",
}
""" Maps gettext (Weblate) codes to CLDR """


def process_language(lang, english_langs, langs_list):
    lang = lang.strip()
    print(f"Processing {lang}...")

    cldr_present = True  # Assume CLDR file is present.
    cldr_lang = CLDR_NAMES[lang] if lang in CLDR_NAMES else lang.replace("_", "-")

    country_code = lang.split("_")[0]

    try:
        print("Looking for required CLDR file...")
        cldr_file = open(
            f"cldr-json/cldr-json/cldr-localenames-full/main/{cldr_lang}/languages.json",
            "r",
        )
        cldr_json = json.load(cldr_file)
    except FileNotFoundError:
        print(f"No CLDR file found for language: {cldr_lang}.")
        try:
            cldr_lang = country_code
            cldr_file = open(
                f"cldr-json/cldr-json/cldr-localenames-full/main/{cldr_lang}/languages.json",
                "r",
            )
            cldr_json = json.load(cldr_file)
            print(f"Using file for {cldr_lang} instead.")
        except FileNotFoundError:
            print("Could not find possible substitutes.")
            cldr_present = False  # Correct earlier assumption.

    if cldr_present:
        po = polib.POFile()
        po.metadata = {
            "Project-Id-Version": "dialect-cldr-langs",
            "Language": lang,
            "Content-Type": "text/plain; charset=utf-8",
            "Content-Transfer-Encoding": "8bit",
        }

        cldr_langs = cldr_json["main"][cldr_lang]["localeDisplayNames"]["languages"]

        for lang_code, lang_name in cldr_langs.items():
            english_name = english_langs.get(lang_code)

            if english_name is not None:
                entry = polib.POEntry(
                    msgid=english_name,
                    msgstr=lang_name,
                )
                po.append(entry)

        po.save(f"cldr-langs/{lang}.po")
        langs_list.append(lang)


# Clone CLDR json data if needed
if not os.path.isdir("cldr-json"):
    print("Cloning Unicode CLDR repository...")
    subprocess.call(["git", "clone", "https://github.com/unicode-org/cldr-json"])

try:
    # Get English names for gettext catalog creation
    print("Getting language English names for catalog...")
    cldr_file = open(
        "cldr-json/cldr-json/cldr-localenames-full/main/en/languages.json",
        "r",
    )
    cldr_json = json.load(cldr_file)
    english_langs = cldr_json["main"]["en"]["localeDisplayNames"]["languages"]

    # Parse UI LINGUAS file to know what languages generate
    linguas_file = open("ui/LINGUAS", "r")
    generated = []  # Store generated languages
    for lang in linguas_file:
        # Create catalog for language
        process_language(lang, english_langs, generated)

except FileNotFoundError:
    print("No CLDR file found for English!")

print("Creating LINGUAS file...")
with open("cldr-langs/LINGUAS", "w") as f:
    f.writelines("\n".join(generated) + "\n")
