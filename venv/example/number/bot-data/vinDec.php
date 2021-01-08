<?php 
require_once('../bot-manager/new-bot//vendor/autoload.php');
use DiDom\Document;
use DiDom\Element;

$vin = $_GET['vin'];

// class PARTSAPI
// {
//     public static function VINdecodeShort($vin, $lang, $key) {
//         $curl = curl_init();
//         curl_setopt_array($curl, array(
//             CURLOPT_URL => "https://partsapi.ru/api.php?act=VINdecodeShort&vin=$vin&lang=$lang&key=$key",
//             CURLOPT_RETURNTRANSFER => true,
//             CURLOPT_POST => false,
//         ));
//         $response = curl_exec($curl);
//         $response = json_decode($response, false);
//         curl_close($curl);
//         return $response;
//     }
// }
// $lang="ru";
// $key="huJuRBXoM2KwJmyzIVO9VvaNS3tG5bFe";
// $result=PARTSAPI::VINdecodeShort($vin, $lang, $key);
// echo json_encode($result , JSON_UNESCAPED_UNICODE);

function getBus($vin) {
    $headers = array();
    $heder[] = 'cache-control: no-store, no-cache, must-revalidate';
    $heder[] = 'content-type: text/html; charset=UTF-8';
    $heder[] = 'content-type: text/html; charset=UTF-8';
    $heder[] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1';
    $heder[] = 'pragma: no-cache';
    $params=['vin'=>'Z94CT41CBFR420383', 'token'=>'03AGdBq25m73_ivrFDZKHkdrXAjlcHimzfK_oetfpgyTqM8UdZjH5UXr5YvCilTQo_W2McZZ78duH6WlIsngUfc5RxEbX1oFWNpRDY_qV8ZDtO-jwgV6iaV_5A1hlwU6BlI2SDWWhc7sidUIH_2i1GASa-IAZg7aRiCO-t4THVSijScoqss7ZwXXqU7WaaAf7TZ3w4uM4Spg08bIU2fXpt-01yP9QqD1F7YFKyAY6YsKkyZCkc6z_3DAnmX-6STwox84qgI9D_jDjbiXGkRFJPiXeqTslLbWFCnzKZjDlRYloQjve1qpCqhJ095xDURnpq5tTFOJ65mwu4tfW1M9Lg6xI0KxPhh-2mTMs8wD4PQMfU99YVBs1NIwWVv0Ea2_NWRquetzdyn5zaF09ArWvvP5j8O-qRYKMCY1m0tp45p1JKVqAjka3VKE9rD0Aosj9ygJLxlKtqHytp', 'clientId'=>'703603098.1608822222' ];

    $ch = curl_init();
    sleep(2);
    curl_setopt($ch, CURLOPT_URL, 'https://autobius.ru/data/');
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS , $params);
    sleep(2);
    $result = curl_exec($ch);
    return $result;

}



function parse($vin) {
    sleep(2);
    $res = getBus($vin);
    file_put_contents('parse.html' , print_r( $res , 1));

    $docParse = new Document('parse.html' , TRUE);
    echo $docParse;
    //echo $docParse;
    $el = $docParse->find('tr th');
    $el2 = $docParse->find('tr td');
    $vinInfo = [];
    foreach($el as $prop => $key) {
        $vinInfo[$key->text()] = $el2[$prop]->text();

    }
    echo json_encode($vinInfo, JSON_UNESCAPED_UNICODE);
}

parse($vin);

?>