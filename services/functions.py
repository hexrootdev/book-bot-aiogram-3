
PAGE_SIZE = 1050
book = {}

def _to_dict(arg1, arg2) -> dict[str, str]:
    return dict(zip(arg1, arg2))

def _get_part_text(text: str, start: int, size: int):
    ends = '.,:;!?'
    text = text[start:(start + size)]
    if text[-1] in ends and text[-2] in ends:
        text = text[:-2]
    for el in text[::-1]:
        if el in ends:
            return text[:(text.rfind(el)) + 1]

def prepare_book(path: str):
    book.clear()

    with open(path, 'r', encoding='utf-8') as file:
        content = file.read().replace(r'\n', ' ').replace('...', '.')
    number = 0
    while content.strip():
        number += 1
        text = _get_part_text(content, 0, PAGE_SIZE)
        lenght = len(text)
        content = content[lenght:]
        book[number] = text.lstrip()
    return book


