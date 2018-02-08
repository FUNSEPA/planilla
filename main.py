import argparse
from core import tools
from core.config import EMAIL_DATA

parser = argparse.ArgumentParser()
parser.add_argument(
    "--quincena",
    type=int,
    default=1,
    help="Número de quincena a pagar")
parser.add_argument(
    "--individual",
    type=int,
    default=0,
    help="Si son separados o en listado")
parser.add_argument(
    "--enviar",
    action='store_true',
    help="Activar 1 para enviar por correo")
parser.add_argument(
    "--to",
    type=str,
    default=EMAIL_DATA['to'],
    help="Correo al cual enviar el listado")
parser.add_argument(
    "--preview",
    action='store_true',
    help="Vista previa de los datos")

args = parser.parse_args()

if args.individual == 0:
    template_tipo = 'lista'
else:
    template_tipo = 'unico'
if args.quincena == 1:
    template_quincena = 'primera'
    data_name = 'planilla.xlsx'
elif args.quincena == 2:
    template_quincena = 'segunda'
    data_name = 'planilla.xlsx'
elif args.quincena == 3:
    template_quincena = 'bono'
    data_name = 'bono.xlsx'
elif args.quincena == 4:
    template_quincena = 'aguinaldo'
    data_name = 'aguinaldo.xlsx'

template_name = 'template_{}_{}.html'.format(template_quincena, template_tipo)

enviar = True if args.enviar else False
planilla = tools.PlanillaParser(
    quincena=args.quincena,
    file_name=data_name)

if not args.preview:
    if args.individual == 0:
        tools.HTMLGenerator(
            enviar=enviar,
            to=args.to).crear_lista(
            planilla,
            template_name=template_name)
    else:
        tools.HTMLGenerator(
            enviar=enviar,
            to=args.to).crear_unico(
            planilla,
            template_name=template_name)

# tools.HTMLGenerator().crear_lista(planilla, template_name='template_segunda_lista.html')

# tools.HTMLGenerator().crear_unico(planilla, template_name='template_segunda_unico.html')
