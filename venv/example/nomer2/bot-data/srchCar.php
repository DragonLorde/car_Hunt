<?php

require_once('../bot-manager/new-bot//vendor/autoload.php');
use DiDom\Document;
use DiDom\Element;


function get_Link($mark, $model, $year) {
    $url = "https://auto.drom.ru/" . $mark . "/" . $model . "/year-" . $year . "/used/";
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL,$url);
    sleep(1);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER,1);//для возврата результата в виде строки, вместо прямого вывода в браузер
    $returned = curl_exec($ch);
    curl_close ($ch);
    return $returned;
}

function stat_link($links) {
    $url = $links;
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL,$url);
    sleep(1);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER,1);//для возврата результата в виде строки, вместо прямого вывода в браузер
    $returned = curl_exec($ch);
    curl_close ($ch);
    return $returned;
}

function link_Parse($data) {
    
    file_put_contents('parseDrom2.html' , print_r( $data , 1));
    //echo $data;
    $docParse = new Document('parseDrom2.html' , TRUE);
    $el = $docParse->find('.css-grspv8');
    $arrLink = [];
    $arrSortLink = [];
    foreach($el as $prop) {
        $arrLink[] = $prop->getAttribute('href');        
    }

    for($i = 0; $i <= count($arrLink); $i++) {
       $res = stat_link($arrLink[$i]);
       $arrSortLink[] = $res;
    }
    
}

function link_Each($data) {

}

link_Parse(get_Link("toyota" , "camry", "2015"));


?>