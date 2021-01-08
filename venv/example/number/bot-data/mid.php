<?php
require_once('../bot-manager/new-bot//vendor/autoload.php');
use DiDom\Document;
use DiDom\Element;

    function getBus($website) {
        $ch = curl_init();
        sleep(2);
        curl_setopt($ch, CURLOPT_URL, $website);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
        $result = curl_exec($ch);
        return $result;

    }


 function midSeale($mark , $model , $eyar ) {
    $website = 'https://auto.drom.ru/region72/' . $mark . '/' . $model . '/year-' . $eyar . '/';
    $res = getBus($website);
    #var_dump($res);
    file_put_contents('parseDrom.html' , print_r( $res , 1));

    $docParse = new Document('parseDrom.html' , TRUE);
    $el = $docParse->find('span[data-ftid="bull_price"]');
    $arrSale = [];
        foreach($el as $prop) {
            $sale = str_replace(" ", "", $prop->text());
            settype($sale , 'integer');
            $arrSale[] = $sale;
        }
        //var_dump($arrSale);
        $cur = 0;
        for($i = 0; $i < count($arrSale); $i++) {
            $cur += $arrSale[$i];
        // echo $cur;
            //echo '</br>';
        }
        $cur /= count($arrSale);
        echo json_encode(array('seal' => (string)(int)$cur));

}

$mr = $_GET['mrk'];
$md = $_GET['mdl'];
$yer = $_GET['yer'];

midSeale(mb_strtolower($mr) , mb_strtolower($md) , mb_strtolower($yer) );


?>