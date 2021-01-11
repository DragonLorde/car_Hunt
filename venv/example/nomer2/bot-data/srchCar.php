<?php

require_once('../bot-manager/new-bot//vendor/autoload.php');
use DiDom\Document;
use DiDom\Element;


function get_Link($mark, $model, $year, $mv) {
    //https://auto.drom.ru/suzuki/grand_vitara/year-2007/?mv=1.8
    $url = "https://auto.drom.ru/" . $mark . "/" . $model . "/year-" . $year . "/?mv=" . $mv;
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL,$url);
    sleep(1);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER,1);//для возврата результата в виде строки, вместо прямого вывода в браузер
    $returned = curl_exec($ch);
    curl_close ($ch);
    return $returned;
}

function get_Link_page($mark, $model, $year, $mv, $pageNumber) {
    //https://auto.drom.ru/suzuki/grand_vitara/year-2007/?mv=1.8
    $url = "https://auto.drom.ru/" . $mark . "/" . $model . "/year-" . $year . "/?mv=" . $mv . $pageNumber;
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL,$url);
    sleep(1);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER,1);//для возврата результата в виде строки, вместо прямого вывода в браузер
    $returned = curl_exec($ch);
    curl_close ($ch);
    return $returned;
}

function stat_link($links) {
    // $url = $links;
    // $ch = curl_init();
    // curl_setopt($ch, CURLOPT_URL,$url);
    // sleep(1);
    // curl_setopt($ch, CURLOPT_RETURNTRANSFER,1);//для возврата результата в виде строки, вместо прямого вывода в браузер
    // $returned = curl_exec($ch);
    // curl_close ($ch);
    // file_put_contents('parseDrom2_links.html' , print_r( $returned , 1));
    $docParse = new Document('parseDrom2_links.html' , TRUE);
    $el = $docParse->find('a[data-ftid="bulls-list_bull"]');
    $arrLinks = [];
    foreach($el as $prop) {
        array_push($arrLinks , $prop->getAttribute('href'));
    }
    //data-ftid="bulls-list_bull"    
    return $arrLinks;
}   

function vin_detected($links) {
    $url = $links;
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL,$url);
    sleep(1);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER,1);//для возврата результата в виде строки, вместо прямого вывода в браузер
    $returned = curl_exec($ch);
    curl_close ($ch);
    file_put_contents('parseDrom2_links_vin.html' , print_r( $returned , 1));
    $docParse = new Document('parseDrom2_links.html' , TRUE);
    $el = $docParse->find('.css-u42a2k');
    foreach($el as $prop) {
        var_dump($prop);
    }
}


function link_Parse($data) {
    
    // file_put_contents('parseDrom2.html' , print_r( $data , 1));
    $docParse = new Document('parseDrom2.html' , TRUE);
    $el = $docParse->find('.css-grspv8');
    $arrAllLink = [];
    foreach($el as $prop) {
       array_push( $arrAllLink, $prop->getAttribute('href'));
    }

    $arrData = [];

    for($i = 0; $i < count($arrAllLink); $i++ ) {
        array_push($arrData, stat_link($arrAllLink[$i]));
    }

    for($i = 0; $i < count($arrData); $i++) {
        for($i2 = 0; $i2 < count($arrData[$i]); $i2++) {
            vin_detected($arrData[$i][$i2]);
        }
    }
    
}

link_Parse(get_Link("toyota" , "camry", "2015", '2.2'));


?>