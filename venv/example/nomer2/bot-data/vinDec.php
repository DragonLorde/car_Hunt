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

    $ch = curl_init();
    sleep(2);
    curl_setopt($ch, CURLOPT_URL, 'https://autobius.ru/lookup/X9F4XXEED47T11217');
    sleep(3);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    $result = curl_exec($ch);
    return $result;

}



function parse($vin) {
    $res = getBus($vin);
    file_put_contents('parse.html' , print_r( $res , 1));

    $docParse = new Document('parse.html' , TRUE);
    echo $docParse;
    //echo $docParse;
    // $el = $docParse->find('tr th');
    // $el2 = $docParse->find('tr td');
    // $vinInfo = [];
    // foreach($el as $prop => $key) {
    //     $vinInfo[$key->text()] = $el2[$prop]->text();

    // }
    echo json_encode($vinInfo, JSON_UNESCAPED_UNICODE);
}

parse($vin);

?>