#! /usr/bin/env python
import re
import os


class Directories:
    root_dir = ''
    files_with_changes = []
    directories = []

    def __init__(self, files_with_changes, root_dir=''):
        self.root_dir = root_dir

        self.set_only_files(files_with_changes)

    # En caso que haya directorios en files_with_changes,
    # extrae los archivos y remueve esos elementos (directorios)
    def set_only_files(self, files_with_changes=None):
        for key in files_with_changes:
            self.process_directory(re.sub(r"" + os.sep + '$', '', key))

    # Retorna una ruta completa del archivo dado
    def full_path(self, path=''):
        return self.root_dir + os.sep + path

    # Procesa directorio y subdirectorios en busca de archivos
    # Se incluyen los archivos a la lista files_with_changes
    def process_directory(self, file=''):
        is_dir = 0

        for root, dirs, files in os.walk(file):
            is_dir = 1
            for dir in dirs:
                self.process_directory(file + os.sep + dir)

            for archivo in files:
                if os.path.exists(file + os.sep + archivo):
                    self.files_with_changes.append(file + os.sep + archivo)

        root, ext = os.path.splitext(file)
        if is_dir == 0 and ext and os.path.exists(file):
            self.files_with_changes.append(file)

        return

    def set_directories_list(self):
        for arch in self.files_with_changes:
            dirs = arch.split(os.sep)
            dir_acum = ''
            count_aux = 0

            for dir in dirs:
                count_aux += 1

                dir_acum = dir_acum + os.sep + dir
                if count_aux == len(dirs):
                    if not self.file_exists_in_directories(dir_acum):
                        self.directories.append(dir_acum)
                else:
                    if not self.file_exists_in_directories(dir_acum + os.sep):
                        self.directories.append(dir_acum + os.sep)

    def file_exists_in_directories(self, path=''):
        if path in self.directories:
            return True
        else:
            return False

    def print_directories_list(self):
        print('')
        for directory in self.directories:
            print(directory)
