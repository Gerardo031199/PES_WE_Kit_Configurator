import yaml
from pathlib import Path

class Config:
    config_dir = "config"
    def __init__(self):
        self.get_config_files()

    def get_config_files(self):
        self.filelist = []
        self.games_config = []
        for p in Path(self.config_dir).iterdir():
            if p.is_file():
                self.filelist.append(p.name)
                self.games_config.append(p.stem)

    def load_config(self, file):
        with open(self.config_dir + "/" + file) as stream:
            self.file = yaml.safe_load(stream)

        self.game_name = self.file["Gui"]["Game Name"]
        self.game_data = self.file["Game Data"]
        self.settings = self.file["Settings"]