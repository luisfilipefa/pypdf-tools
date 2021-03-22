import pathlib, sys, time
from PyPDF2 import PdfFileReader, PdfFileWriter

class Splitter:
    def __init__(self, file):
        self.file_to_split = pathlib.Path(file).resolve()
        self.reader = PdfFileReader(self.file_to_split.open(mode="rb"), strict=False)

    def run(self):
        for page in range(self.reader.numPages):
            writer = PdfFileWriter()
            writer.addPage(self.reader.getPage(page))
            new_file = pathlib.Path(self.file_to_split.parents[0] / f"{self.file_to_split.stem}-pag-{page+1}.pdf")
            with new_file.open(mode="wb") as f:
                writer.write(f)

if __name__ == "__main__":
    def main():
        file = sys.argv[1] if len(sys.argv) > 1 else "."
        s = Splitter(file)
        s.run()

    main()


"""
1 - ler arquivo
2 - pegar cada página
3 - adicionar ao merger object
4 - escrever página para novo arquivo
"""
