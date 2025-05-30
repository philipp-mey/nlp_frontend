from easy_nlp_translate import initialize_translator


def main():
    translator = initialize_translator(
        translator_name="mbart", source_lang="en", target_lang="de"
    )

    translated_text = translator.translate("""1
00:00:00,000 --> 00:00:03,880
What do you mean, what is GitHub?

2
00:00:03,880 --> 00:00:11,640
It's the largest, most complete development platform in the world.

3
00:00:11,640 --> 00:00:14,680
Millions of developers use it, and it's not just developers.""")
    return translated_text


if __name__ == "__main__":
    print(main())
