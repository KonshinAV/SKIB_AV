from pprint import pprint


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

class TXTFile:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = None

    def load_data(self, mode = 'r', encoding = 'utf-8', show_exceptions = False):
        try:
            with open(f'{self.file_name}', f'{mode}', encoding = encoding) as file:
                self.data = []
                for str in file: self.data.append(str.replace('\n', ''))
        except Exception as ex:
            if show_exceptions is True: print(f'Exception: {ex}')
            self.data = None

    def write_data(self, path, mode = 'w', encoding= 'utf-8', show_exceptions = False, show_progress = False):
        from tqdm import tqdm
        try:
            with open(f"{path}", f"{mode}", encoding=encoding) as file:
                if show_progress is True:
                    for line in tqdm(iterable=self.data, desc= f'Writing {self.file_name}'): file.write(f"{line}\n")
                else:
                    for line in self.data: file.write(f"{line}\n")
        except Exception as ex:
            if show_exceptions is True: print(f'Exception: {ex}')

    def find_value(self, value):
        self.value = value

class CSVFile:
    def write_data (self, file_path, data, mode='w', newline='', delimiter=';', header=False):
        import csv
        self.data = data
        with open(file_path, mode=mode, newline=newline) as file:
            writer = csv.writer(file, delimiter=delimiter)
            writer.writerows(self.data)
