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
        $data = file_get_contents('../data/cursos.json');
        $cursos = json_decode($data);
        $datos_curso = array_filter($cursos, function ($f) use ($curso) {   return $f->clave == $curso; });
        if (count($datos_curso) === 0) {
            die('Curso no encontrado :(');
        }
        $datos_curso = array_pop($datos_curso);
        $datos = file_get_contents('../data/educacion/'.$datos_curso->codigo.'.json');
        $fat->mset([
            'datos' => $datos_curso,
            'fecha' => file_get_contents('../data/educacion/actualizacion-'.$datos_curso->codigo.'.txt'),
            'curso' => json_decode($datos),
            'nombre' => str_replace("Wikimedia Chile/", "", json_decode($datos)->nombre)
        ]);
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
