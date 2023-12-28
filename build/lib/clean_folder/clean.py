import os
import shutil
import re
import sys

from pathlib import Path


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}

file_formats = {
    'images' : ['jpeg', 'png', 'jpg', 'svg'],
    'videos' : ['avi', 'mp4', 'mov', 'mkv'],
    'documents' : ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
    'musics' : ['mp3', 'ogg', 'wav', 'amr'],
    'archives' : ['zip', 'gz', 'tar']
}

FOLDERS_DICT = {}

KNOWN_EXTENSIONS = set()
UNKNOWN_EXTENSIONS = set()
KNOWN_FILES = []

# Function normalize() get input str and return str
def normalize(file_name):
    # Translate characters 
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    translated = file_name.translate(TRANS)
    
    # Replace all not A-Za-z0-9. characters to '_'
    normalized_file_name = re.sub(r'[^A-Za-z0-9.]', '_', translated)
    return normalized_file_name

# Make new directories
def make_folders(path):
    os.makedirs(path, exist_ok=True)

# Sort files to new directories 
def sort(path):
    list_dir = os.listdir(path)
    print(list_dir)
    for el in list_dir:
        item_path = os.path.join(path, el)
        print(item_path)
        if os.path.isfile(item_path):
            filename, file_extension = os.path.splitext(el)
            file_extension = file_extension.replace('.', '').lower() # /folder/file.txt -> folder, file, .txt

            KNOWN_FILES.append(el)
            
            if file_extension in file_formats["documents"]:
                KNOWN_EXTENSIONS.add(file_extension)
                dir = FOLDERS_DICT.get('documents')
                new_file_name = normalize(el)
                shutil.move(item_path, os.path.join(dir, new_file_name))
            elif file_extension in file_formats["images"]:
                KNOWN_EXTENSIONS.add(file_extension)
                dir = FOLDERS_DICT.get('images')
                new_file_name = normalize(el)
                shutil.move(item_path, os.path.join(dir, new_file_name))
            elif file_extension in file_formats["videos"]:
                KNOWN_EXTENSIONS.add(file_extension)
                dir = FOLDERS_DICT.get('videos')
                new_file_name = normalize(el)
                shutil.move(item_path, os.path.join(dir, new_file_name))
            elif file_extension in file_formats["musics"]:
                KNOWN_EXTENSIONS.add(file_extension)
                dir = FOLDERS_DICT.get('musics')
                new_file_name = normalize(el)
                shutil.move(item_path, os.path.join(dir, new_file_name))
            elif file_extension in file_formats["archives"]:
                KNOWN_EXTENSIONS.add(file_extension)
                dir = FOLDERS_DICT.get('archives')
                new_file_name = normalize(el)
                shutil.move(item_path, os.path.join(dir, new_file_name))
            else:
                UNKNOWN_EXTENSIONS.add(file_extension)
                dir = FOLDERS_DICT.get('other')
                new_file_name = normalize(el)
                shutil.move(item_path, os.path.join(dir, new_file_name))
            
        if os.path.isdir(item_path):
            sort(item_path)
            if item_path not in FOLDERS_DICT.values():
                try:
                    os.rmdir(item_path)
                    print(f"Removed empty folder: {item_path}")
                except OSError:
                    pass

def create_target_folders(folder_path):
    for folder in file_formats.keys():
        target_folder_path = os.path.join(folder_path, folder)
        make_folders(target_folder_path)
        FOLDERS_DICT.update({folder : target_folder_path})
    other_folder_path = os.path.join(folder_path, 'other')
    make_folders(other_folder_path)
    FOLDERS_DICT.update({'other' : other_folder_path})

def unpack_archives(path):
    for el in Path(path).iterdir():
        file_name = el.stem
        try:
            shutil.unpack_archive(el, os.path.join(path, file_name))
        except:
            dir = FOLDERS_DICT.get('other')
            shutil.move(el, os.path.join(dir, el.name))
        else:
            os.remove(el)

def write_to_file(path, items):
    with open(path, 'w') as output_file:
        for item in items:
            output_file.write(f'{item}\n')

def main():
    folder_path = os.path.abspath(sys.argv[1])
    # folder_path = os.path.abspath('test_garbage_folder_etalon')

    create_target_folders(folder_path)
    make_folders(folder_path)
    sort(folder_path)
    unpack_archives(FOLDERS_DICT.get('archives'))

    known_extension_path = os.path.join(folder_path, 'known_extensions.txt')
    unknown_extension_path = os.path.join(folder_path, 'unknown_extensions.txt')
    files_path = os.path.join(folder_path, 'files.txt')
    write_to_file(known_extension_path, KNOWN_EXTENSIONS)
    write_to_file(unknown_extension_path, UNKNOWN_EXTENSIONS)
    write_to_file(files_path, KNOWN_FILES)

if __name__ == "__main__":
    main()
