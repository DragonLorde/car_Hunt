<?php
require_once('../bot-manager/new-bot//vendor/autoload.php');
use DiDom\Document;
use DiDom\Element;

// $ch = curl_init('https://avto-nomer.ru/ru/gallery.php?fastsearch=%D1%81518%D1%85%D1%80152');
// curl_setopt($ch, CURLOPT_PUT, true);
// curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
// curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
// curl_setopt($ch, CURLOPT_HEADER, false);
// $html = curl_exec($ch);
// curl_close($ch);    
$reg = $_GET['reg'];


$document = new Document('https://avto-nomer.ru/ru/gallery.php?fastsearch=' . $reg, true);


$posts = $document->find('.img-responsive');
$title = $document->find('.panel-body');

if($reg != null) {
    if ($title == null) {
        echo json_encode(array('src' => 'no__img'));
    } else {
        $id = uniqid();

        $img  = file_get_contents($posts[0]->getAttribute('src'));

        file_put_contents($id . '.jpg', $img  , FILE_APPEND);

        echo json_encode(array("src" => 'http://bsl-show.online/bot-data/' . $id . '.jpg'));
    }
} else {
    echo json_encode(array('src' => 'no_reg'));
}

?>