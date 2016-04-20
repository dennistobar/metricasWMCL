<?php

require_once '../vendor/autoload.php';

$fat = \Base::instance();
$fat->config('../config.ini');

$fat->route('GET /', function (\Base $fat) {
    $fat->mset(['contenido' => 'fsa/fsa.html']);
    echo \Template::instance()->render('page.html');
});

$fat->route('GET /fsa', 'fsa->index');
$fat->route('GET /fsa/', 'fsa->index');
$fat->route('GET /fsa/@num', 'fsa->fase');
$fat->route('GET /fsa/@num/@discurso', 'fsa->discurso');

$fat->run();
