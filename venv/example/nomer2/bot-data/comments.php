<?php

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS, PUT, DELETE');
header('Access-Control-Allow-Headers: X-Requested-With,Origin,Content-Type,Cookie,Accept');
header('Content-type: application/json'); 



class Bd {
    protected static $datasourse = "mysql:host=localhost;dbname=u1145099_carhunter";
    protected static $login = "u1145099_default";
    protected static $pass = "Z!Hq2ukD";
    protected static $base;
    protected static $opt = [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES   => false, 
    ];
    
    function __construct () {}

    private static function crateBd() {
        if(!isset(self::$base)) {
            try {
                self::$base = new PDO(self::$datasourse , self::$login , self::$pass , self::$opt);
                self::$base->exec("set names utf8");
            }
            catch (PDOExceptin $e) {
                echo $error=$e->getMessage();
                exit();
            }
            return self::$base;
        }
    }
    public static function getBd() {
        return self::crateBd();
    }
}

$conn = Bd::getBd();


class Comments {


    private $bd;
    private $dataPost;
    private $dataGet;
    
    function __construct($bds)
    {
        $this->bd = $bds;
        $this->dataPost = json_decode(file_get_contents('php://input'), true);
        $this->dataGet = $_GET['reg'];
    }

    public function initor() {
        if(isset($this->dataPost)) {
            $this->putCom($this->dataPost);
        } else if (isset($_GET['reg'])) {
            $this->getCom($this->dataGet);
        } else {
            echo json_encode(array("ERROR" => "Not Data"));
        }
    }


    private function isCom($name, $reg) {
        $stmt = $this->bd->prepare('SELECT * FROM `comm` WHERE `name` = ? AND `reg` = ?');
        $stmt->execute(array($name, $reg));
        $res = $stmt->fetchColumn();
        if($res == 0) {
            return true;
        } 
            return false;
    }

    private function putCom($props) {
        $isRes = $this->isCom($props['name'],  $props['reg']);
        if($isRes) {
            $stmt = $this->bd->prepare('INSERT INTO `comm`( `name`, `date`, `reg`, `text`) VALUES (:nm, :dt, :rg, :txt )');
            $stmt->execute(array("nm" =>  $props['name'], "dt" => date("m.d.y"), "rg" => $props['reg'], "txt" => $props['text']));
            $this->getCom($props['reg']);
        } else {
            $this->getCom($props['reg']);
        }
        
    }

    private function getCom($props) {
        $stmt = $this->bd->prepare('SELECT * FROM `comm` WHERE `reg` = ?');
        $stmt->execute(array($props));
        $dataArr = [];
        while ($row = $stmt->fetch(PDO::FETCH_LAZY))
        {
            $dataArr[] = array( 
                "name" => $row['name'],
                "date" => $row['date'],
                "text" => $row['text'],
            ); 
        }
        echo json_encode($dataArr, JSON_UNESCAPED_UNICODE);
    }

}

 $res = new Comments($conn);
 $res->initor();


?>

