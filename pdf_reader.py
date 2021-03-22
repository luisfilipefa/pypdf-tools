import pathlib, os, time, sys
from PyPDF2 import PdfFileReader

class PDFReader:
    def __init__(self, path):
        self.path = pathlib.Path(path).resolve()
        self.file = self.path.open(mode="rb")
        self.reader = PdfFileReader(self.file, strict=False)

    def run(self):
        for p in range(self.reader.numPages):
            page = self.reader.getPage(p)
            content = page.extractText()
            if "COMPROVANTE" in content:
                print("O documento é um comprovante!")

if __name__ == "__main__":
    def main():
        path = sys.argv[1] if len(sys.argv) > 1 else "."
        p = PDFReader(path)
        p.run()

    main()
