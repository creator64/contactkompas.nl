def sql_nested_replace(col_name: str, *chars_to_remove, replace_to: str = '') -> str | None:
    if not chars_to_remove:
        return
    output = f"replace({col_name}, '{chars_to_remove[0]}', '{replace_to}')"
    for char in chars_to_remove[1:]:
        output = f"replace({output}, '{char}', '{replace_to}')"
    return output


def remove_multiple_characters(target: str, *chars_to_remove: str):
    for char in chars_to_remove:
        target = target.replace(char, "")
    return target
