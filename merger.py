import pathlib, sys, datetime, os
from PyPDF2 import PdfFileReader, PdfFileMerger

class Merger:
    def __init__(self, root_path, recursive):
        self.current_time = datetime.datetime.now()
        self.root_path = pathlib.Path(root_path)
        self.new_file = pathlib.Path(self.root_path / f"new_merged_file-{self.current_time.day}-{self.current_time.month}-{self.current_time.year}-{self.current_time.hour}:{self.current_time.minute}.pdf")
        self.merger = PdfFileMerger(strict=False)
        self.recursive = recursive

    def run(self):
        # Check if the recursive option is enabled, if it is, then every pdf file in the root_path (including subdirs) is merged
        # If it is not enabled, then only the pdf files in the root_path are merged
        if self.recursive:
            files_to_merge = [pathlib.Path(root, f).resolve() for root, dirs, files in os.walk(self.root_path) for f in files if f.endswith(".pdf")]
        else:
            files_to_merge = [pathlib.Path(x).resolve() for x in self.root_path.glob("*.pdf")]
        # For loop to iterate through each PDF file in the given directory and add to the merger object
        for file in sorted(files_to_merge):
            self.merger.append(open(file, "rb"))
            print(f"[+] File {file} added sucessfully...")

        # Writes the content of the merger object to a new file
        with self.new_file.open(mode="wb") as f:
            self.merger.write(f)
            print(f"\n[+] New merged file saved to: {self.new_file}\n")

if __name__ == "__main__":
    def main():
        root_path = sys.argv[1] if len(sys.argv) > 1 else "."
        recursive = sys.argv[2] if len(sys.argv) > 2 else False
        m = Merger(root_path, recursive)
        m.run()

    main()
