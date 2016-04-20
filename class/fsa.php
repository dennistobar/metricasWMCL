<?php

class fsa{

    public function index(\Base $fat){
        $fat->mset(['contenido' => 'fsa/fsa-resumen.html']);
        $json = json_decode(file_get_contents('../data/fsa.json'));
        $resumen = [];
        for ($i = 1; $i < 4; ++$i) {
            $resumen[$i] = $json->{$i}->resumen;
        }
        $fat->mset(['resumen' => $resumen,
            'total.paginas' => array_sum(array_map(function ($f) {return $f->paginas;}, $resumen)),
            'total.discursos' => array_sum(array_map(function ($f) {return $f->discursos;}, $resumen)),
            'total.mes_anterior' => array_sum(array_map(function ($f) {return $f->mes_anterior;}, $resumen)),
            'total.mes_actual' => array_sum(array_map(function ($f) {return $f->mes_actual;}, $resumen)),
            'total.visitas' => array_sum(array_map(function ($f) {return $f->visitas;}, $resumen)),
        ]);
        echo \Template::instance()->render('page.html');
    }

    public function fase(\Base $fat){
        $fat->mset(['contenido' => 'fsa/fsa.html', 'titulo' => 'Discursos oficiales de Salvador Allende']);
        $num = $fat->get('PARAMS.num');
        $json = json_decode(file_get_contents('../data/fsa.json'));
        $resumen = $json->{$num}->resumen;
        unset($json->{$num}->resumen);
        $fat->mset(['archivos' => $json->{$num}, 'resumen' => $resumen]);
        echo \Template::instance()->render('page.html');
    }

    public function discurso(\Base $fat){
        $fat->mset(['contenido' => 'fsa/fsa-detalle.html', 'titulo' => 'Discursos oficiales de Salvador Allende']);
        $num = $fat->get('PARAMS.num');
        $discurso = str_replace(' ', '_', $fat->get('PARAMS.discurso'));
        $json = json_decode(file_get_contents("../data/fsa/{$discurso}.json"));
        $visitas = (array) $json->visitas;
        ksort($visitas);
        $anos = array_unique(array_map(function ($f) { return substr($f, 0, 4); }, array_keys($visitas)));
        $fat->mset(['elemento' => $json, 'meses' => $visitas, 'anos' => $anos]);
        echo \Template::instance()->render('page.html');
    }

}
