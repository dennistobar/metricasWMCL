<?php

class fsa
{
    public function index(\Base $fat)
    {
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
    }

    public function fase(\Base $fat)
    {
        $fat->mset(['contenido' => 'fsa/fsa.html']);
        $num = $fat->get('PARAMS.num');
        $json = json_decode(file_get_contents('../data/fsa.json'));
        $resumen = $json->{$num}->resumen;
        unset($json->{$num}->resumen);
        $fat->mset(['archivos' => $json->{$num}, 'resumen' => $resumen]);
    }

    public function discurso(\Base $fat)
    {
        $fat->mset(['contenido' => 'fsa/fsa-detalle.html']);
        $num = $fat->get('PARAMS.num');
        $discurso = str_replace(' ', '_', $fat->get('PARAMS.discurso'));
        $json = json_decode(file_get_contents("../data/fsa/{$discurso}.json"));
        $visitas = (array) $json->visitas;
        $anual = (array) $json->anuales;
        ksort($visitas);
        ksort($anual);
        $anos = array_keys($anual);
        $fat->mset(['elemento' => $json, 'meses' => $visitas, 'anos' => $anos, 'anual' => $anual]);
    }

    public function beforeroute(\Base $fat)
    {
        $fat->mset(['titulo' => 'Discursos oficiales de Salvador Allende', 'fecha' => file_get_contents('../data/fsa-fecha.txt')]);
    }

    public function afterroute(\Base $fat)
    {
        echo \Template::instance()->render('page.html');
    }
}
