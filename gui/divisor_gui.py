from PyPDF2 import PdfFileMerger, PdfFileReader, PageRange
import PySimpleGUI as sg
import pathlib

""" 
    <--- GUI CODE --->
    1 - CREATE A NEW LAYOUT
    2 - CREATE A NEW WINDOW OBJECT
    3 - RUN FUNCTION TO READ THE INPUTS FROM THE WINDOW 
"""

class SplitterGui:
    def __init__(self):
        sg.theme("Black")
        self.layout = [
            [sg.Text("Arquivo PDF", size=(15,0)), 
             sg.Input(size=(39,0), key="src_file"), 
             sg.FileBrowse("Navegar", size=(15,0), file_types=(("Arquivos PDF", "*.pdf"),))],
            [sg.Text("Novos Arquivos", size=(15,0)), 
             sg.Input(size=(39,0), key="dst_path"), 
             sg.FolderBrowse("Navegar", size=(15,0))],
            [sg.Radio("Cada página", group_id="method", default=True, key="each"),
             sg.Radio("Intervalo específico", group_id="method", key="custom_range"),
             sg.Radio("Páginas específicas", group_id="method", key="custom_pages"),
             sg.Input(size=(20,0), key="term")],
            [sg.Output(size=(75,10))],
            [sg.Button("Dividir", size=(15,0), key="split", bind_return_key=True)]
        ]

        self.window = sg.Window("Divisor de PDF").Layout(self.layout)

    def run(self):
        self.event, self.values = self.window.Read()

"""
    <--- SPLITTER CLASS CODE --->
    1 - CONSTRUCTOR
        1 - RECEIVES THE SRC_FILE TO THE PDF 
        2 - RECEIVES THE DST_PATH TO SAVE THE SPLITTED FILES
    1 - EACH PAGE METHOD
        1 - CREATES A NEW READER OBJECT FROM THE PDFFILEREADER CLASS IN THE PYPDF2 LIB
        2 - FOR LOOP A 
            - TAKES EACH PAGE FROM THE SRC_FILE
            - ADDS TO THE MERGER OBJECT
            - DEFINES THE PATTER FOR THE NEW FILE
             - WRITES THE PAGE TO THE NEW FILE
    2 - CUSTOM RANGE METHOD
        1 - RECEIVES THE CUSTOM RANGE FROM THE INPUT IN THE GUI
        2 - FOR LOOP TO ADD THE RANGE OF PAGES TO THE MERGER OBJECT
        3 - WRITES THE CONTENT OF THE MERGER OBJECT TO THE NEW FILE
    3 - CUSTOM PAGES METHOD
        1 - SAME AS THE CUSTOM RANGE METHOD, BUT INSTEAD OF A RANGE, TAKES INDIVIDUAL PAGES FROM THE INPUT AND WRITES EACH PAGE TO A NEW FILE
"""

class Splitter:
    def __init__(self, src_file, dst_path):
        self.src_file = pathlib.Path(src_file).resolve()
        self.dst_path = pathlib.Path(dst_path).resolve()

    def each_page(self):
        reader = PdfFileReader(self.src_file.open(mode="rb"), strict=False)

        for page in range(reader.numPages):
            merger = PdfFileMerger(strict=False)
            merger.append(self.src_file.open(mode="rb"), pages=PageRange(str(page)))
            print(f"-> [OK] Página {page+1} dividida com sucesso...")
            new_file = pathlib.Path(self.dst_path / f"{self.src_file.stem}-pag-{page+1}.pdf")

            with new_file.open(mode="wb") as f:
                merger.write(f)

        print("")
        print(f"-> [!] {reader.numPages} páginas divididas com sucesso...")
        print(f"-> [+] Novos arquivos salvos em: {new_file.parents[0]}")

    def custom_range(self, r):
        total_ranges = [x for x in r.split(",")]
        
        for current_range in total_ranges:
            custom_range = [int(x)-1 for x in current_range.split("-")]
            count = 0

            for _ in range(custom_range[1]+1 - custom_range[0]):
                count+=1
                print(f"-> [OK] Página {custom_range[0]+count} dividida com sucesso...")

            merger = PdfFileMerger(strict=False)
            merger.append(self.src_file.open(mode="rb"), pages=PageRange(f"{str(custom_range[0])}:{str(custom_range[1]+1)}"))
            new_file = pathlib.Path(self.dst_path / f"{self.src_file.stem}-pags-{custom_range[0]+1}-{custom_range[1]+1}.pdf")

            with new_file.open(mode="wb") as f:
                merger.write(f)

            print("")
            print(f"-> [!] {custom_range[1]+1 - custom_range[0]} páginas divididas com sucesso...")
            print(f"-> [+] Novo arquivo salvo em: {new_file.parents[0]}")
            print("")

    def custom_pages(self, p):
        custom_pages = [int(x) for x in p.split("-")]

        for page in custom_pages:
            merger = PdfFileMerger(strict=False)
            merger.append(self.src_file.open(mode="rb"), pages=PageRange(str(page-1)))
            print(f"-> [OK] Página {page} adicionada com sucesso...")
            new_file = pathlib.Path(self.dst_path / f"{self.src_file.stem}-pag-{page}.pdf")

            with new_file.open(mode="wb") as f:
                merger.write(f)

        print("")
        print(f"-> [!] {len(custom_pages)} páginas divididas com sucesso...")
        print(f"-> [+] Novos arquivos salvos em: {new_file.parents[0]}")

if __name__ == "__main__":
    def main():
        g = SplitterGui()
        
        # Initiates the event loop from the GUI
        while True:
            try:
                # Starts the method to run the GUI and read its values
                g.run()
                if g.event == sg.WIN_CLOSED: # If user clicks on the x (close) in the window, closes the program
                    break
                elif g.event == "split":# If user clicks on the Dividir button, creates an instance of the Splitter class and starts the method acording to the Radio Selected in the GUI
                    s = Splitter(g.values["src_file"], g.values["dst_path"])
                    if g.values["each"]: # If Radio checked in the GUI, returns True
                        s.each_page()
                    if g.values["custom_range"]: # If Radio checked in the GUI, returns True
                        s.custom_range(g.values["term"])
                    if g.values["custom_pages"]: # If Radio checked in the GUI, returns True
                        s.custom_pages(g.values["term"])
            except KeyboardInterrupt:
                break  

    main()
