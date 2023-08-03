# 用来 tokenize 中英文文本


def is_chinese_char(char):
    # 判断是否为中文字符
    return '\u4e00' <= char <= '\u9fff'


def trim_irrelevant_char(text):
    new_text = ""
    for char in text:
        if char.isspace() or is_chinese_char(char) or char.isalnum():
            new_text += char
    return new_text


def tokenize_mixed_text(text):
    tokens = []
    current_token = ''
    is_english_token = None

    for char in text:
        if is_chinese_char(char):
            if current_token and is_english_token:
                tokens.extend(current_token.split())
                current_token = ''
            current_token += char
            tokens.append(current_token)
            current_token = ''
            is_english_token = False
        else:
            if current_token and not is_english_token:
                tokens.append(current_token)
                current_token = ''
            if char.isspace():
                if current_token:
                    tokens.append(current_token)
                    current_token = ''
            else:
                current_token += char
                is_english_token = True

    if current_token:
        tokens.append(current_token)

    return tokens


def trim_and_tokenize(text):
    return tokenize_mixed_text(trim_irrelevant_char(text))

