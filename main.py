import os
import requests
import subprocess
from documentcloud.addon import AddOn
from documentcloud.exceptions import APIError

class ExtractThenTag(AddOn):
    """Add-On that extracts text between a start and end string"""
    def main(self):
        os.makedirs(os.path.dirname("./out/"), exist_ok=True)
        os.chdir('out')
        self.set_message("Extracting text from documents...")
        start = self.data.get('start')
        end = self.data.get('end')
        for document in self.get_documents():
            text_to_parse = document.full_text
            text_to_parse = text_to_parse.replace("\n", " ")
            start_char = text_to_parse.find(start) + len(start)
            end_char = text_to_parse.find(end)
            extracted_text = text_to_parse[start_char:end_char]
            name_key = self.data.get("key_name")
            try:
                document.data[name_key] = extracted_text
                document.put()
            except requests.exceptions.RequestException as e:
                pass
            except APIError as ed:
                pass
        self.set_message("Add-On run complete.")
if __name__ == "__main__":
    ExtractThenTag().main()
