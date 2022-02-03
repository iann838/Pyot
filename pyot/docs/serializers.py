from typing import Any, List


class PyotDocTypeSerializer:

    def __init__(self, type: Any, relative_paths: List[str]) -> None:
        if type is None:
            self.data = None
            return
        self.data = str(type)
        self.data = self.data.replace("typing.", "")
        self.data = self.data.replace("<class ", "")
        self.data = self.data.replace(">", "")
        self.data = self.data.replace("'", "")
        for relative_path in relative_paths:
            if self.data.startswith(relative_path):
                self.data = self.data[len(relative_path):]
