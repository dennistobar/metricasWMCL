<?php

require_once '../vendor/autoload.php';

$fat = \Base::instance();
$fat->config('../config.ini');

$fat->route('GET /', function(\Base $fat){
    $fat->mset(['contenido' => 'fsa.html']);
    echo \Template::instance()->render('page.html');
});

$fat->route('GET /fsa/@num', function(\Base $fat){
    $fat->mset(['contenido' => 'fsa.html', 'titulo' => 'Fundación Salvador Allende']);
    $num = $fat->get('PARAMS.num');
    $json = json_decode(file_get_contents('../data/fsa.json'));
    $resumen = $json->{$num}->resumen;
    unset($json->{$num}->resumen);
    $fat->mset(['archivos' => $json->{$num}, 'resumen' => $resumen]);
    echo \Template::instance()->render('page.html');
});

$fat->route('GET /fsa/@num/@discurso', function(\Base $fat){
    $fat->mset(['contenido' => 'fsa.html', 'titulo' => 'Fundación Salvador Allende']);
    $num = $fat->get('PARAMS.num');
    $discurso = str_replace(" ", "_", $fat->get('PARAMS.discurso'));
    $json = json_decode(file_get_contents("../data/fsa/{$discurso}.json"));
    $fat->set('archivos', $json->{$num});
    echo \Template::instance()->render('page.html');
});

$fat->run();
