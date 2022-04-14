class fileWriter:
    def __init__(self, file_dir):
        self.file_handle = open(file_dir, 'w+')
    def __del__(self):
        self.file_handle.close()