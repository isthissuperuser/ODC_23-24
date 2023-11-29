<?php

require_once 'Item.inc.php';
require_once 'Product.inc.php';
require_once 'State.inc.php';
require_once 'Session.inc.php';

class Model {

    private $db;

    function __construct($db) {
        $this->db = $db;
    }

    function createSession($name, $email_address) {
        $sessid = bin2hex(random_bytes(32));
        $stmt = $this->db->prepare("INSERT INTO session (id, name, email_address, creation) VALUES (:id, :name, :email_address, NOW());");
        if($stmt->execute(array(':id' => $sessid, ':name' => $name, ':email_address' => $email_address))) {
            return new Session($sessid, $name, $email_address);
        } else {
            //print_r($stmt->errorInfo());
            die('Failed to create session');
        }
    }

    function getAvailableProducts() {
        $stmt = $this->db->prepare("SELECT * FROM product");
        if($stmt->execute()) {
            $arr = array();
            while($row = $stmt->fetch()) {
                array_push($arr, new Product($row['id'], $row['name'], $row['description'], $row['picture'], $row['price']));
            }
            return $arr;
        }
        return null;
    }

    function purchase($session, $cart, $payment_info) {
        $this->db->beginTransaction();
        $stmt = $this->db->prepare("INSERT INTO purchase (session_id, credit_card, cvv, expiry_month, expiry_year) VALUES (:session_id, :credit_card, :cvv, :expiry_month, :expiry_year)");
        if($stmt->execute(array(
            ':session_id' => $session->getId(),
            ':credit_card' => $payment_info['credit_card'],
            ':cvv' => $payment_info['cvv'],
            ':expiry_month' => $payment_info['expiry_month'],
            ':expiry_year' => $payment_info['expiry_year'],
        ))) {
            $id = $this->db->lastInsertId();
        } else {
            $this->db->rollback();
            //print_r($stmt->errorInfo());
            return false;
        }
        foreach($cart as $product_id => $quantity) {
            $stmt = $this->db->prepare("INSERT INTO purchase_item (product_id, purchase_id, quantity) VALUES (:product_id, :purchase_id, :quantity)");
            if(!$stmt->execute(array(':product_id' => $product_id, ':purchase_id' => $id, ':quantity' => $quantity))) {
                $this->db->rollback();
                //print_r($stmt->errorInfo());
                return false;
            }
        }
        $this->db->commit();
        return true;
    }

    function saveState($state) {
        $token = bin2hex(random_bytes(4));
        $stmt = $this->db->prepare("INSERT INTO saved_state (okey, content) values (:okey, :content)");
        if(!$stmt->execute(array(':okey' => $token, ':content' => $state))) {
            //print_r($stmt->errorInfo());
            return false;
        }
        return $token;
    }

    function retrieveState($token) {
        $stmt = $this->db->prepare("SELECT * FROM saved_state WHERE okey = :okey LIMIT 1");
        if($stmt->execute(array(':okey' => $token))) {
            if($row = $stmt->fetch()) {
                return $row['content'];
            }
            return false;
        }
        return false;
    }

}

?>
