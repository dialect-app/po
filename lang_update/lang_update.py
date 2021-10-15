import argparse
import json
import os
import re
import requests
import subprocess
from bs4 import BeautifulSoup


LANGUAGES = {
    "af": "Afrikaans",
    "sq": "Albanian",
    "am": "Amharic",
    "ar": "Arabic",
    "hy": "Armenian",
    "az": "Azerbaijani",
    "eu": "Basque",
    "be": "Belarusian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "bg": "Bulgarian",
    "ca": "Catalan",
    "ceb": "Cebuano",
    "ny": "Chichewa",
    "zh": "Chinese",
    "zh-CN": "Chinese (Simplified)",
    "zh-TW": "Chinese (Traditional)",
    "co": "Corsican",
    "hr": "Croatian",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "en": "English",
    "eo": "Esperanto",
    "et": "Estonian",
    "tl": "Filipino",
    "fi": "Finnish",
    "fr": "French",
    "fy": "Frisian",
    "gl": "Galician",
    "ka": "Georgian",
    "de": "German",
    "el": "Greek",
    "gu": "Gujarati",
    "ht": "Haitian Creole",
    "ha": "Hausa",
    "haw": "Hawaiian",
    "iw": "Hebrew",
    "he": "Hebrew",
    "hi": "Hindi",
    "hmn": "Hmong",
    "hu": "Hungarian",
    "is": "Icelandic",
    "ig": "Igbo",
    "id": "Indonesian",
    "ga": "Irish",
    "it": "Italian",
    "ja": "Japanese",
    "jw": "Javanese",
    "kn": "Kannada",
    "kk": "Kazakh",
    "km": "Khmer",
    "rw": "Kinyarwanda",
    "ko": "Korean",
    "ku": "Kurdish (Kurmanji)",
    "ky": "Kyrgyz",
    "lo": "Lao",
    "la": "Latin",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "lb": "Luxembourgish",
    "mk": "Macedonian",
    "mg": "Malagasy",
    "ms": "Malay",
    "ml": "Malayalam",
    "mt": "Maltese",
    "mi": "Maori",
    "mr": "Marathi",
    "mn": "Mongolian",
    "my": "Myanmar (Burmese)",
    "ne": "Nepali",
    "no": "Norwegian",
    "or": "Odia (Oriya)",
    "ps": "Pashto",
    "fa": "Persian",
    "pl": "Polish",
    "pt": "Portuguese",
    "pa": "Punjabi",
    "ro": "Romanian",
    "ru": "Russian",
    "sm": "Samoan",
    "gd": "Scots Gaelic",
    "sr": "Serbian",
    "st": "Sesotho",
    "sn": "Shona",
    "sd": "Sindhi",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovenian",
    "so": "Somali",
    "es": "Spanish",
    "su": "Sundanese",
    "sw": "Swahili",
    "sv": "Swedish",
    "tg": "Tajik",
    "ta": "Tamil",
    "tt": "Tatar",
    "te": "Telugu",
    "th": "Thai",
    "tr": "Turkish",
    "tk": "Turkmen",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "ug": "Uyghur",
    "uz": "Uzbek",
    "vi": "Vietnamese",
    "cy": "Welsh",
    "xh": "Xhosa",
    "yi": "Yiddish",
    "yo": "Yoruba",
    "zu": "Zulu",
}

CLDR_NAMES = {
    "kmr": "ku",  # They seem to be the same since Kurmanji (ku) is Northern Kurdish (kmr).
    "zh_CN": "zh-Hans",
    "zh_TW": "zh-Hant",
    "zh-CN": "zh-Hans",
    "zh-TW": "zh-Hant",
}

DIALECT_NAMES = {
    "zh-Hans": "zh-CN",
    "zh-Hant": "zh-TW",
}

# Add any language to this list to exclude it from the automated process.
EXCLUDE_LIST = [
    # No decent source
    "oc",  # Occitan
    # Was manually updated by the translator
    "eo",  # Esperanto
    "fr",  # French
    "fy",  # Frisian
    "ja",  # Japanese
    "lv",  # Latvian
    "uk",  # Ukranian
    "zh_CN",  # Chinese
]
# Even if a language is in this list, you can pass it as a parameter to the program.

# If any language is on this list and it shouldn't be, please create an issue:
# https://www.github.com/dialect-app/po
# You can also open an issue if any language should be added.

# All languages that need "capitalization"
CAPS_LIST = [
    "it",  # Italian
]

parser = argparse.ArgumentParser()
parser.add_argument(
    "language", nargs="?", help="the language code for language to update"
)
parser.add_argument(
    "-g", "--google", help="force use google for language names", action="store_true"
)
args = parser.parse_args()

if not os.path.isdir("cldr-json"):
    print("Cloning Unicode CLDR repository...")
    subprocess.call(["git", "clone", "https://github.com/unicode-org/cldr-json"])


def process_language(lang, arged=False):
    lang = lang.strip()
    if lang and (arged is True or lang not in EXCLUDE_LIST):
        cldr_present = True  # Assume CLDR file is present.
        cldr_lang = CLDR_NAMES[lang] if lang in CLDR_NAMES else lang.replace("_", "-")

        g_lang = lang.split("_")[0]

        print(f"Reading {lang}.po ...")

        lang_file = open(f"../{lang}.po", "r")
        lang_file_contents = lang_file.read()
        lang_file.close()

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
                cldr_lang = g_lang
                cldr_file = open(
                    f"cldr-json/cldr-json/cldr-localenames-full/main/{cldr_lang}/languages.json",
                    "r",
                )
                cldr_json = json.load(cldr_file)
                print(f"Using file for {cldr_lang} instead.")
            except FileNotFoundError:
                print("Could not find possible substitutes.")
                cldr_present = False  # Correct earlier assumption.

        if cldr_present and not args.google:
            cldr_langs = cldr_json["main"][cldr_lang]["localeDisplayNames"]["languages"]
            for lang_code, lang_name in cldr_langs.items():
                if lang_code in DIALECT_NAMES:
                    lang_code = DIALECT_NAMES[lang_code]

                if lang_code not in LANGUAGES:
                    continue

                if cldr_lang in CAPS_LIST:
                    lang_name = lang_name.capitalize()

                lang_file_contents = re.sub(
                    rf'msgid "{re.escape(LANGUAGES[lang_code])}"\nmsgstr ".*"\n',
                    rf'msgid "{LANGUAGES[lang_code]}"\nmsgstr "{lang_name}"\n',
                    lang_file_contents,
                )
        else:
            print("Fetching localized names from Google Translate...")

            page = requests.get("https://translate.google.com/?hl=" + g_lang)
            soup = BeautifulSoup(page.text, "html5lib")

            print("Generating updated string with localized names...")

            for div in soup.find_all("div"):
                if div.attrs.get("class", None) == ["qSb8Pe"]:
                    lang_code = div.attrs["data-language-code"]
                    lang_name = div.find(attrs={"class": "Llmcnf"}).string

                    lang_file_contents = re.sub(
                        rf'msgid "{re.escape(LANGUAGES[lang_code])}"\nmsgstr ".*"\n',
                        rf'msgid "{LANGUAGES[lang_code]}"\nmsgstr "{lang_name}"\n',
                        lang_file_contents,
                    )

        print(f"Saving {lang}.po ...")

        lang_file = open(f"../{lang}.po", "w")
        lang_file.write(lang_file_contents)
        lang_file.close()

        print()


if args.language:
    process_language(args.language, True)
else:
    linguas_file = open("../LINGUAS", "r")
    for lang in linguas_file:
        process_language(lang)
