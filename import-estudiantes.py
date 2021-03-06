# -*- coding: utf-8 -*-
import json
import urllib2, urllib
import re, os
from time import strftime

user_agent = 'Wikimedia Chile stats importer 1.0 <dennis.tobar@wikimediachile.cl>'

with open('data/cursos.json') as data_file:
    cursos = json.load(data_file)

cursos = map(lambda x: x.get('codigo'), filter(lambda x: x.get('activo') == True, cursos))

api = 'https://es.wikipedia.org/w/api.php?action=liststudents&format=json&courseids=%s&prop=username&group=1' % "|".join(cursos)
req = urllib2.Request(api)
req.add_header('User-Agent', user_agent)
resp = urllib2.urlopen(req)
data = resp.read()

data_cursos = json.loads(data)

for curso in data_cursos.values():
    print 'Procesando curso'
    estudiantes = curso.get('students')
    profesores = curso.get('instructors')
    voluntarios_linea = curso.get('online_volunteers')
    voluntarios_campus = curso.get('campus_volunteers')
    inicio = curso.get('start').replace("-", "")+"000000"
    termino = curso.get('end').replace("-", "")+"000000"

    listado_estudiantes = { }

    for estudiante in estudiantes:
        listado_estudiantes[estudiante['username']] = {'articulos': [], 'contador': {}, 'contribs': []}
        listado_estudiantes[estudiante['username']]['articulos'] = map(lambda x: x.get('title'), filter(lambda x: type(x) is dict, estudiante.itervalues()))

    nombres_estudiantes = "|".join(listado_estudiantes.keys()).encode('utf-8')

    continuar = True
    continuacion = []
    while True:
        api = 'https://es.wikipedia.org/w/api.php?action=query&format=json&list=usercontribs&uclimit=500&ucuser=%s&ucend=%s&ucstart=%s&ucdir=older&%s' % (urllib.quote_plus(nombres_estudiantes), inicio, termino, "=".join(continuacion))
        req = urllib2.Request(api)
        req.add_header('User-Agent', user_agent)
        resp = urllib2.urlopen(req)
        data = resp.read()
        data = json.loads(data)

        for cambio in data.get('query').get('usercontribs'):
            listado_estudiantes[cambio.get('user')]['contribs'].append({
                'namespace' : cambio.get('ns'),
                'tamano' : cambio.get('size'),
                'pagina' : cambio.get('title'),
                'fecha' : re.sub(r"[:\-ZT]*", r"", cambio.get('timestamp'))
            })

        if 'continue' not in data.keys():
            break
        else:
            continuacion = ['uccontinue', data.get('continue').get('uccontinue').replace(" ", "%20")]
        print continuacion

    suma_total = ns_principal = ns_otros = suma_ns_principal = 0
    articulos = []
    for estudiante, datos in listado_estudiantes.items():
        suma_total += sum(map(lambda x: abs(x.get('tamano')), datos['contribs']))
        ns_principal += len(filter(lambda x: x.get('namespace') == 0, datos['contribs']))
        ns_otros += len(filter(lambda x: x.get('namespace') != 0, datos['contribs']))
        suma_ns_principal = sum(map(lambda x: abs(x.get('tamano')), filter(lambda x: x.get('namespace') == 0, datos['contribs'])))
        articulos.extend(datos['articulos'])
        listado_estudiantes[estudiante]['contador'] = {
            'ediciones': {
                'principal' : len(filter(lambda x: x.get('namespace') == 0, datos['contribs'])),
                'otros': len(filter(lambda x: x.get('namespace') != 0, datos['contribs']))
            },
            'tamano' : {
                'principal' : sum(map(lambda x: abs(x.get('tamano')), filter(lambda x: x.get('namespace') == 0, datos['contribs']))),
                'otros': sum(map(lambda x: abs(x.get('tamano')), filter(lambda x: x.get('namespace') != 0, datos['contribs'])))
            }
        }

    datos_curso = {
        'id' : curso.get('id'),
        'nombre' : curso.get('name'),
        'inicio': inicio,
        'fin': termino,
        'ediciones' : { 'principal' : ns_principal, 'otros' : ns_otros, 'total': ns_principal + ns_otros },
        'cantidad' : {
            'estudiantes': len(listado_estudiantes.keys()),
            'profesores' : len(profesores),
            'voluntarios_linea' : len(voluntarios_linea),
            'voluntarios_campus' : len(voluntarios_campus),
            'articulos': len(articulos)
        },
        'usuarios':{
            'estudiantes': listado_estudiantes.keys(),
            'profesores': map(lambda x: x.get('username'), profesores),
            'voluntarios_linea': map(lambda x: x.get('username'), voluntarios_linea),
            'voluntarios_campus': map(lambda x: x.get('username'), voluntarios_campus)
        },
        'tamano' : { 'principal': suma_ns_principal, 'otros' : suma_total - suma_ns_principal, 'total' : suma_total },
        'listado_estudiantes' : listado_estudiantes,
        'articulos' : articulos
        }

    contribs = {}
    graficos = {'tamano': {'principal': [], 'otros': []}, 'ediciones': {'principal': [], 'otros': []}, 'diario': []}
    for estudiante, datos in listado_estudiantes.items():
        graficos.get('tamano').get('principal').append({ 'usuario': estudiante, 'conteo': datos.get('contador').get('tamano').get('principal') })
        graficos.get('tamano').get('otros').append({ 'usuario': estudiante, 'conteo': datos.get('contador').get('tamano').get('otros') })
        graficos.get('ediciones').get('principal').append({ 'usuario': estudiante, 'conteo': datos.get('contador').get('ediciones').get('principal') })
        graficos.get('ediciones').get('otros').append({ 'usuario': estudiante, 'conteo': datos.get('contador').get('ediciones').get('otros') })
        for contribucion in datos.get('contribs'):
            print contribucion
            fecha = contribucion.get('fecha')[:8]
            if fecha not in contribs.keys():
                contribs[fecha] = 0
            contribs[fecha] += 1

    for fecha, valor in contribs.items():
        graficos.get('diario').append({ 'dia': fecha, 'conteo': valor })


    f = open('data/educacion/'+str(curso.get('id'))+'.json', 'w')
    f.write(json.dumps(datos_curso))
    f.close()
    f = open('data/educacion/resumen-'+str(curso.get('id'))+'.json', 'w')
    f.write(json.dumps(graficos))
    f.close()
    f = open('data/educacion/actualizacion-'+str(curso.get('id'))+'.txt', 'w')
    f.write(strftime("%d-%m-%Y %H:%M"))
    f.close()
