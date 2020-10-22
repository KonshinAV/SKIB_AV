

def json_dump_write (path, data, mode = 'w', ensure_ascii = False, indend = 4):
    import json
    with open(f"{path}",f"{mode}") as file:
        json.dump(data, file, ensure_ascii=ensure_ascii, indent=indend)


def json_dump_read (path, mode = 'r', show_exceptions = False):
    import json
    try:
        with open(f"{path}",f"{mode}") as file:
            data = json.load(file)
            return data
    except Exception as ex:
        if show_exceptions:
            print(f"Excepion: {ex}")
        return None