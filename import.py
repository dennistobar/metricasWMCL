# -*- coding: utf-8 -*-
import json
import urllib2
import os.path
import os
import sys
import hashlib
from time import strftime
from datetime import datetime

from dateutil.relativedelta import relativedelta

user_agent = 'Wikimedia Chile stats importer 1.0 <dennis.tobar@wikimediachile.cl>'
mesActual = strftime('%Y%m', datetime.today().timetuple())
mesAnterior = strftime('%Y%m', (datetime.today() - relativedelta(months=1)).timetuple())

datos = {}
resumen = {1:{},2:{},3:{}}
archivos = {1: [
# etapa 1
'ChFSA FD1197205170(1).djvu', 'ChFSA FD1197204030(1).djvu', 'ChFSA FD1197204070(1).djvu',
'ChFSA FD1197204210(1).djvu', 'ChFSA FD1197209040(1).djvu', 'ChFSA FD1197212020(1).djvu',
'ChFSA FD1197309040(1).djvu', 'ChFSA FD1197109040(1).djvu', 'ChFSA FD1197107110(1).djvu',
'ChFSA FD1197212040(1).djvu' ], 2: [
# etapa 3
'ChFSA FD1197107240(1).djvu', 'ChFSA FD1197108050(1).djvu', 'ChFSA FD1197110310(1).djvu',
'ChFSA FD1197111090(1).djvu', 'ChFSA FD1197202112(1).djvu', 'ChFSA FD1197202210(1).djvu',
'ChFSA FD1197202290(1).djvu', 'ChFSA FD1197208100(1).djvu', 'ChFSA FD1197209100(1).djvu',
'ChFSA FD1197210180(1).djvu', 'ChFSA FD1197210211(1).djvu', 'ChFSA FD1197210270(1).djvu',
'ChFSA FD1197301080(1).djvu', 'ChFSA FD119730130(1).djvu', 'ChFSA FD1197302160(1).djvu',
'ChFSA FD1197303020(1).djvu', 'ChFSA FD1197303050(1).djvu', 'ChFSA FD1197303080(1).djvu',
'ChFSA FD1197303081(1).djvu', 'ChFSA FD1197304250(1).djvu', 'ChFSA FD1197306170(1).djvu',
'ChFSA FD1197307061(1).djvu', 'ChFSA FD1197308031(1).djvu', 'ChFSA FD1197308131(1).djvu',
'ChFSA FD1197308160(1).djvu'], 3 : [
#etapa 2
'ChFSA FD1197110180(1).djvu', 'ChFSA FD1197202110(1).djvu', 'ChFSA FD1197202140(1).djvu',
'ChFSA FD1197205260(1).djvu', 'ChFSA FD1197207250(1).djvu', 'ChFSA FD1197210140(1).djvu',
'ChFSA FD1197210240(1).djvu', 'ChFSA FD1197211100(1).djvu', 'ChFSA FD1197212221(1).djvu',
'ChFSA FD1197212220(1).djvu', 'ChFSA FD1197302120(1).djvu', 'ChFSA FD1197302150(1).djvu',
'ChFSA FD1197303230(1).djvu', 'ChFSA FD1197304100(1).djvu', 'ChFSA FD1197305040(1).djvu']}

# Obtenemos los datos de los discursos con indice y donde estan transcluidos (sí, es el término real)
api = 'https://es.wikisource.org/w/api.php?action=query&format=json&prop=proofread%7Cimages%7Cinfo%7Ctranscludedin&list=&generator=allpages&imlimit=500&tinamespace=0&tishow=!redirect&tilimit=500&gapprefix=ChFSA&gapnamespace=104&gapfilterredir=nonredirects&gaplimit=100'
req = urllib2.Request(api)
req.add_header('User-Agent', user_agent)
resp = urllib2.urlopen(req)
data = resp.read()

data = json.loads(data)

print 'Hola API!'

if 'query' not in data.keys():
    print 'Error en el acceso a la API de wikisource'
    sys.exit(3)

for page_id, page_data in data['query']['pages'].items():
    archivo = page_data.get('images')[0].get('title').replace('Archivo:', '')
    discurso = page_data.get('transcludedin')[0].get('title')
    nombre_discurso = discurso.split('/')[-1]
    url_archivo = archivo.replace(" ", "_")
    md5_commons = hashlib.md5(url_archivo)
    primer, segundo = md5_commons.hexdigest()[:1], md5_commons.hexdigest()[:2]
    commons = 'https://upload.wikimedia.org/wikipedia/commons/thumb/%s/%s/%s/page1-436px-%s.jpg' % (primer, segundo, url_archivo, url_archivo)
    datos = {'nombre': archivo, 'discurso': discurso, 'commons': commons, 'nombre_discurso': nombre_discurso}
    datos['fase'] = [key for key, value in archivos.items() if archivo in value][0]

    print 'Procesando API de visitas de %s' % archivo

    url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/commons.wikimedia.org/all-access/all-agents/%s/daily/20150801/20991231' % ('File:'+url_archivo)

    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent)
    resp = urllib2.urlopen(req)
    data = resp.read()

    resultados = json.loads(data)
    mes = visitas = {}
    for resultado in resultados['items']:
        timestamp, views = [resultado['timestamp'], resultado['views']]
        mes_actual = int(timestamp[:6])
        if mes_actual not in mes.keys():
            mes[mes_actual] = 0
        mes[mes_actual] += int(views)

    for key in sorted(mes.iterkeys()):
        visitas[str(key)] = mes[key]

    datos['visitas'] = visitas

    api2 = 'https://es.wikisource.org/w/api.php?action=query&format=json&prop=contributors&generator=allpages&utf8=1&pclimit=500&gapprefix=%s&gapnamespace=102&gapfilterredir=nonredirects&gaplimit=500' % url_archivo

    print '>> Obteniendo personas que ayudaron en %s' % archivo

    req = urllib2.Request(api2)
    req.add_header('User-Agent', user_agent)
    resp = urllib2.urlopen(req)
    data_contribuyentes = resp.read()

    resultados_contribuyentes = json.loads(data_contribuyentes)
    contribuyentes = []

    for page_id, page_data in resultados_contribuyentes['query']['pages'].items():
        map(lambda y: contribuyentes.append(y), map(lambda x: x['name'], page_data.get('contributors')))

    datos['contribuyentes'] = list(set(contribuyentes))
    datos['paginas'] = len(resultados_contribuyentes['query']['pages'].items())

    # Veamos las visitas previas
    fs = open('data/fsa/old/%s.json' % url_archivo,'r')
    visitas_old = json.loads(fs.read())
    fs.close()

    datos['visitas'] = visitas_old
    datos['visitas'].update(visitas)


    archivo = open('data/fsa/%s.json' % url_archivo, 'w')
    archivo.write(json.dumps(datos))
    archivo.close()


    resumen[datos['fase']][datos['nombre']] = {
        'nombre' : datos['nombre_discurso'],
        'archivo': datos['nombre'],
        'visitas': sum(datos['visitas'].values()),
        'mes_anterior': datos['visitas'][mesAnterior],
        'mes_actual': datos['visitas'][mesActual],
        'paginas': datos['paginas']
    }

for kresumen in resumen.iterkeys():
    resumen[kresumen]['resumen'] = {
        'paginas': sum(map(lambda x: x.get('paginas'), resumen[kresumen].values())),
        'visitas': sum(map(lambda x: x.get('visitas'), resumen[kresumen].values())),
        'mes_anterior': sum(map(lambda x: x.get('mes_anterior'), resumen[kresumen].values())),
        'mes_actual': sum(map(lambda x: x.get('mes_actual'), resumen[kresumen].values())),
        'discursos': len(resumen[kresumen].keys())
     }

fs = open('data/fsa.json', 'w')
fs.write(json.dumps(resumen))
fs.close()

fs = open('data/fsa-fecha.txt', 'w');
fs.write(strftime("%d-%m-%Y %H:%M"))
fs.close()
