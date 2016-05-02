<?php

class educacion
{
    public function index(\Base $fat)
    {
        $fat->mset(['contenido' => 'educacion/portada.html']);

    }

    public function curso(\Base $fat)
    {
        $fat->mset(['contenido' => 'educacion/curso.html']);
        $curso = $fat->get('PARAMS.curso');
    }

    public function beforeroute(\Base $fat)
    {
        $fat->mset(['titulo' => 'Wikipedia en la Universidad']);
    }

    public function afterroute(\Base $fat)
    {
        echo \Template::instance()->render('page.html');
    }
}
