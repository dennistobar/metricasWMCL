import json
import urllib2
import os.path
import os
import collections
import time
import random
import sys

datos = {}
archivos = [
# etapa 1
'ChFSA FD1197205170(1).djvu', 'ChFSA FD1197204030(1).djvu', 'ChFSA FD1197204070(1).djvu',
'ChFSA FD1197204210(1).djvu', 'ChFSA FD1197209040(1).djvu', 'ChFSA FD1197212020(1).djvu',
'ChFSA FD1197309040(1).djvu', 'ChFSA FD1197109040(1).djvu', 'ChFSA FD1197107110(1).djvu',
'ChFSA FD1197212040(1).djvu',
# etapa 3
'ChFSA FD1197107240(1).djvu', 'ChFSA FD1197108050(1).djvu', 'ChFSA FD1197110310(1).djvu',
'ChFSA FD1197111090(1).djvu', 'ChFSA FD1197202112(1).djvu', 'ChFSA FD1197202210(1).djvu',
'ChFSA FD1197202290(1).djvu', 'ChFSA FD1197208100(1).djvu', 'ChFSA FD1197209100(1).djvu',
'ChFSA FD1197210180(1).djvu', 'ChFSA FD1197210211(1).djvu', 'ChFSA FD1197210270(1).djvu',
'ChFSA FD1197301080(1).djvu', 'ChFSA FD119730130(1).djvu', 'ChFSA FD1197302160(1).djvu',
'ChFSA FD1197303020(1).djvu', 'ChFSA FD1197303050(1).djvu', 'ChFSA FD1197303080(1).djvu',
'ChFSA FD1197303081(1).djvu', 'ChFSA FD1197304250(1).djvu', 'ChFSA FD1197306170(1).djvu',
'ChFSA FD1197307061(1).djvu', 'ChFSA FD1197308031(1).djvu', 'ChFSA FD1197308131(1).djvu',
'ChFSA FD1197308160(1).djvu',
#etapa 2
'ChFSA FD1197110180(1).djvu', 'ChFSA FD1197202110(1).djvu', 'ChFSA FD1197202140(1).djvu',
'ChFSA FD1197205260(1).djvu', 'ChFSA FD1197207250(1).djvu', 'ChFSA FD1197210140(1).djvu',
'ChFSA FD1197210240(1).djvu', 'ChFSA FD1197211100(1).djvu', 'ChFSA FD1197212221(1).djvu',
'ChFSA FD1197212220(1).djvu', 'ChFSA FD1197302120(1).djvu', 'ChFSA FD1197302150(1).djvu',
'ChFSA FD1197303230(1).djvu', 'ChFSA FD1197304100(1).djvu', 'ChFSA FD1197305040(1).djvu']

for archivo in archivos:
    datos = datos_finales = {}
    for ano in range(2013, 2016, 1):
        for mes in range(1,13,1):
            mes = str(mes) if mes > 9 else '0'+str(mes)
            ano = str(ano)
            archivo = archivo.replace(" ", "_")
            api = 'http://stats.grok.se/json/commons.m/%s/File:%s' % (ano+mes, archivo)
            req = urllib2.Request(api)
            req.add_header('User-Agent', 'Wikimedia Chile stats importer 1.0 <dennis.tobar@wikimediachile.cl>')
            resp = urllib2.urlopen(req)
            data = resp.read()

            data = json.loads(data)

            datos[ano+mes] = sum(data['daily_views'].values())

    for key in sorted(datos.iterkeys()):
        datos_finales[key] = datos[key]

    fs = open('data/fsa/old/%s.json' % archivo.replace('File:', '').replace(" ", "_"), 'w')
    fs.write(json.dumps(datos_finales))
    fs.close()

    print 'Visitas anteriores procesadas << %s' % archivo
