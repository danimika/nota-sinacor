import PyPDF2
import re
from pprint import pprint

class Nota_sinacor:
    def __init__(self, pdf_path) -> None:
        self.pdf_path = pdf_path
        self.full_note = ''        
        self.data = []

        self.date = None
        self.cliente = None
        self.operacoes = []
        self.resumo = []
        self.totais = []
        self.custos = []

        self.read_note()
        self.get_data()
        self.find_info()

    def read_note(self):
        text = ''
        with open(self.pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()

        self.full_note = text

    def get_data(self):
        lines = self.full_note.splitlines()
        relevant_lines = []
        for line in lines:
            if re.match(r'^\d{2}/\d{2}/\d{4}|\d[\d,.]*', line):
                relevant_lines.append(line)
        self.data = relevant_lines

    def find_date(self,line):
        match = re.match(r'^(\d{2}/\d{2}/\d{4})', line)
        if match:
            self.date = match.group(1)
            return True
        return False
    
    def find_client(self, line):
        cpf_match = re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', line)
        if cpf_match:
            self.cliente = line
            return True
        return False

    def find_operations(self, line):
        if line.endswith('1-BOVESPA'):
            self.operacoes.append(line)
            return True
        return False
    
    def get_resumo(self, line):
        line = re.sub(r'(D)(\d+)', r'-\2', line)
        line = re.sub(r'(C)(\d)', r'\2', line)
        self.resumo.append(line)




    def find_info(self):
        for line in self.data:
            if self.find_date(line):
                continue

            if self.find_client(line):
                continue

            if self.find_operations(line):
                continue
            
            if self.get_resumo(line):
                continue
        

    



pdf_file_path = 'notas/notacv.pdf'
nota = Nota_sinacor(pdf_file_path)


pprint(nota.date)
pprint(nota.cliente)
pprint(nota.operacoes)
pprint(nota.resumo)