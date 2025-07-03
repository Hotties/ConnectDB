import json

class FileWriter:
    def __init__(self, prefix='response', extension='json', folder='.'):
        self.file_number = 0
        self.prefix = prefix
        self.extension = extension
        self.folder = folder

    def write(self, data):
        file_name = f"{self.folder}/{self.prefix}{self.file_number}.{self.extension}"
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"[✔] {file_name} 저장 완료")
        self.file_number += 1
