<?php

class State {

    private $session;
    private $cart;

    function __construct($session) {
        $this->session = $session;
        $this->cart = array();
    }

    function getSessionID() {
        return $this->session->getId();
    }

    function getSession() {
        return $this->session;
    }

    function getCart() {
        return $this->cart;
    }

    function clearCart() {
        $this->cart = array();
    }

    function addToCart($product_id) {
        if(array_key_exists($product_id, $this->cart)) {
            $this->cart[$product_id]++;
        } else {
            $this->cart[$product_id] = 1;
        }
    }

    function toDict() {
        $out = array();
        foreach($this->cart as $product_id => $quantity) {
            array_push($out, array("product" => $product_id, "quantity" => $quantity));
        }
        return array("name" => $this->session->getName(), "email" => $this->session->getEmailAddress(), "cart" => $out);
    }

    function save() {
        return base64_encode(gzcompress(serialize($this)));
    }

    static function restore($token) {
        return unserialize(gzuncompress(base64_decode($token)));
    }

}

?>
