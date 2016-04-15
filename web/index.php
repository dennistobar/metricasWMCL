<?php

require_once '../vendor/autoload.php';

$fat = \Base::instance();
$fat->config('../config.ini');

$fat->route('GET /', function(\Base $fat){
    $fat->mset(['contenido' => 'fsa.html']);
    echo \Template::instance()->render('page.html');
});

$fat->route('GET /fsa/*', function(\Base $fat){
    $fat->mset(['contenido' => 'fsa.html', 'titulo' => 'Fundación Salvador Allende']);
    echo \Template::instance()->render('page.html');
});

$fat->run();
