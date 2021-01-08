<?php
require_once('../bot-manager/new-bot//vendor/autoload.php');
use DiDom\Document;
use DiDom\Element;

unlink('parse2.html');

function getBus($website) {
    $ch = curl_init();
    sleep(2);
    curl_setopt($ch, CURLOPT_URL, $website);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
    $result = curl_exec($ch);
    return $result;

}

function getData() {
    $number = $_GET['number'];
    $website = 'https://' . $number .'.drom.ru/archive/';
    $res = getBus($website);
    file_put_contents('parse2.html' , print_r( $res , 1) );

    $dataArr = [];

    $docParse = new Document('parse2.html' , TRUE);
    $seal = $docParse->find('span[data-ftid="bull_price"]');
    $title = $docParse->find('span[data-ftid="bull_title"]');
    $a = $docParse->find('a[data-ftid="bulls-list_bull"]');
    $loc = $docParse->find('span[data-ftid="bull_location"]');
    $date = $docParse->find('div[data-ftid="bull_date"]');
    
    foreach($seal as $prop => $key) {
        
        $dataArr[] = array("title" => $title[$prop]->text() ,
            "link" => $a[$prop]->href ,
            "seal" => $seal[$prop]->text() ,
            "loc" => $loc[$prop]->text() ,
            "date" => $date[$prop]->text() ,
        );
    }
    echo json_encode($dataArr, JSON_UNESCAPED_UNICODE);

}


getData()

?>