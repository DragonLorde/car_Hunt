<?php

$url = "https://autoteka.ru/report_by_vin/KNMCSHLMS6P607595";
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL,$url);
sleep(6);
curl_setopt($ch, CURLOPT_RETURNTRANSFER,1);//для возврата результата в виде строки, вместо прямого вывода в браузер
$returned = curl_exec($ch);
curl_close ($ch);
echo $returned;




?>