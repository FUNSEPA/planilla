import pathlib
import errno
import shutil
from datetime import datetime

import pdfkit
from openpyxl import load_workbook
from jinja2 import Environment, FileSystemLoader

from core.send_email import send_message
from core.empleado import Empleado
from core.config import EMAIL_DATA


class PlanillaParser:
    lista_empleados = []
    quincena = ''

    def __init__(self, data_path='data', file_name='planilla.xlsx', quincena=1):
        self.data_path = pathlib.Path(data_path)
        self.file_name = file_name

        self.full_file_name = str(self.data_path / self.file_name)
        self.parse_lista(quincena)

    def parse_lista(self, quincena=1):
        self.lista_empleados = []
        wb = load_workbook(self.full_file_name, data_only=True, guess_types=False)
        if quincena == 1:
            for numero, row in enumerate(wb['Anticipo'].rows):
                if row[0].value is not None and numero >= 6:
                    self.lista_empleados.append(Empleado(quincena=quincena, datos=row))

            self.quincena = wb['Anticipo']['A3'].value
        elif quincena == 2:
            for numero, row in enumerate(wb['Fin de Mes'].rows):
                if row[0].value is not None and numero >= 6:
                    self.lista_empleados.append(Empleado(quincena=quincena, datos=row))

            self.quincena = wb['Fin de Mes']['A3'].value

        elif quincena == 4 or quincena == 3:
            for numero, row in enumerate(wb['Nomina'].rows):
                if row[0].value is not None and numero >= 6:
                    self.lista_empleados.append(Empleado(quincena=quincena, datos=row))

            self.quincena = wb['Nomina']['A4'].value


class HTMLGenerator:
    options = {
        'margin-top': '0.7in',
        'margin-right': '0.1in',
        'margin-bottom': '1.5in',
        'margin-left': '0.6in'
    }

    def __init__(self, output_folder='output', template_folder='templates', enviar=False, to=''):
        self.output_folder = pathlib.Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.template_folder = template_folder
        self.env = Environment(loader=FileSystemLoader(self.template_folder))
        self.enviar = enviar
        self.to = to

    @classmethod
    def copy(cls, src, dest):
        try:
            shutil.copytree(src, dest)
        except OSError as e:
            if e.errno == errno.ENOTDIR:
                shutil.copy(src, dest)
            else:
                pass

    def crear_lista(self, planilla, template_name='template_lista.html'):
        template = self.env.get_template(template_name)
        full_template_name = str(self.output_folder / 'lista_empleados.html')
        html_output = template.render(
            lista_empleados=planilla.lista_empleados,
            quincena=planilla.quincena,
            hora=datetime.now())

        with open(full_template_name, "w") as fh:
            fh.write(html_output)
        self.copy(self.template_folder + '/img', str(self.output_folder / 'img'))

        pdf = self.generar_pdf(full_template_name, 'lista_empleados')
        if self.enviar and pdf is not None:
            msg = send_message(
                EMAIL_DATA['from'],
                self.to,
                planilla.quincena,
                '{}.pdf'.format(pdf),
                self.output_folder)
            if msg:
                print("Mensaje enviado")

    def crear_unico(self, planilla, template_name='template_unico.html'):
        template = self.env.get_template(template_name)
        self.copy(self.template_folder + '/img', str(self.output_folder / 'img'))
        for persona in planilla.lista_empleados:
            full_template_name = str(self.output_folder / '{}.html'.format(persona.codigo))
            html_output = template.render(
                persona=persona,
                quincena=planilla.quincena,
                hora=datetime.now())

            with open(full_template_name, "w") as fh:
                fh.write(html_output)
            pdf = self.generar_pdf(full_template_name, persona.codigo)
            if self.enviar and pdf:
                msg = send_message(
                    EMAIL_DATA['from'],
                    persona.correo,
                    planilla.quincena,
                    '{}.pdf'.format(pdf),
                    self.output_folder)
                if msg:
                    print("Mensaje enviado")

    def generar_pdf(self, template, file_name):
        output_filename = str(self.output_folder / '{}.pdf'.format(file_name))
        try:
            pdfkit.from_file(
                str(pathlib.Path(template).resolve()),
                output_filename,
                options=self.options)
        except Exception:
            pass
        return file_name
