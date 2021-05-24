import tempfile
import logging
import os


class Temporal:
    def __init__(self):
        with tempfile.TemporaryDirectory() as file:
            self.temp_folder = file
        os.mkdir(self.temp_folder)
        logging.info(f"Temporal files will be written in {self.temp_folder}")
    
        self.sub_temp_folder = os.path.join(self.temp_folder, "tmp")
        os.mkdir(self.sub_temp_folder)
    
    
    def get_temp_folder(self):
        return self.temp_folder
    
    
    def get_temp_file(self, suffix=".pdf"):
        with tempfile.NamedTemporaryFile(suffix=suffix, dir=self.sub_temp_folder) as file:
            return file.name
