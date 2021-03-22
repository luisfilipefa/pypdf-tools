from PyPDF2 import PdfFileMerger
import PySimpleGUI as sg
import pathlib, os

"""
    <--- GUI CODE --->
    1 - CREATE A NEW LAYOUT
    2 - CREATE A NEW WINDOW OBJECT
    3 - RUN METHOD TO READ THE INPUTS FROM THE WINDOW
"""

class MergerGui:
    def __init__(self):
        sg.theme("Black")
        self.layout = [
            [sg.Text("Arquivos PDF", size=(15,0)),
             sg.Input(size=(30,0), key="src_path"),
             sg.FolderBrowse("Navegar", size=(15,0))],
            [sg.Text("Novo Arquivo", size=(15,0)),
             sg.Input(size=(30,0), key="dst_file"),
             sg.SaveAs("Navegar", size=(15,0), file_types=(("Arquivos PDF", "*.pdf"),))],
            [sg.Checkbox("Recursivo", key="recursive")],
            [sg.Output(size=(65,10))],
            [sg.Button("Unificar", size=(15,0), key="merge", bind_return_key=True)]
        ]

        self.window = sg.Window("Unificador de PDF").Layout(self.layout)

    def run(self):
        self.event, self.values = self.window.Read()

"""
    <--- MERGER CLASS CODE --->
    1 - CONSTRUCTOR
        1 - RECEIVES THE SRC_PATH TO THE PDF FILES TO MERGE
        2 - RECEIVES THE DST_FILE TO SAVE THE MERGED PDF TO
        3 - CREATES A NEW INSTANCE VARIABLE THAT CONTAINS A LIST OF ALL THE PDF FILES IN THE SRC_PATH
        4 - CREATES A NEW PDFFILEMERGER OBJECT FROM THE PYPDF2 LIB
    2 - RUN METHOD
        1 - FOR LOOP A
            1 - READ EVERY PDF FILE IN THE SRC_PATH
            2 - ADD THE CURRENT FILE IN THE LOOP TO THE MERGER OBJECT (READING BINARY)
        2 - OPENS THE DST_FILE AS WRITE BINARY AND WRITES THE CONTENT OF THE MERGER OBJECT

"""

class Merger:
    def __init__(self, src_path, dst_file, recursive):
        self.src_path = pathlib.Path(src_path).resolve()
        self.dst_file = pathlib.Path(dst_file).resolve()
        self.merger = PdfFileMerger(strict=False)
        self.recursive = recursive
    def run(self):
        if self.recursive:
            records = [pathlib.Path(root, f).resolve() for root, dirs, files in os.walk(self.src_path) for f in files if f.endswith(".pdf")]
        else:
            records = [x for x in self.src_path.glob("*.pdf")]

        for file in records:
            self.merger.append(open(file, "rb"))
            print(f"-> [OK] {file} adicionado com sucesso...")

        with self.dst_file.open(mode="wb") as f:
            self.merger.write(f)
            print("")
            print(f"-> [!] {len(records)} arquivos PDF encontrados no diretório")
            print(f"-> [+] Novo arquivo unificado criado em: {self.dst_file}")

if __name__ == "__main__":
    def main():
        g = MergerGui()

        # Initiates the event loop from the GUI
        while True:
            try:
                # Starts the method to run the GUI and read its values
                g.run()

                # Checks the data received from the GUI
                if g.event == sg.WIN_CLOSED: # If user clicks on the x (close) in the window, closes the program
                    break
                elif g.event == "merge": # If user clicks on the Unificar button, creates an instance of the Merger class and starts the run method
                    m = Merger(g.values["src_path"], g.values["dst_file"], g.values["recursive"])
                    m.run()
            except KeyboardInterrupt:
                break

    main()
