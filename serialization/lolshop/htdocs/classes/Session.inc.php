<?php

class Session {

    private $id;
    private $name;
    private $email_address;

    function __construct($id, $name, $email_address) {
        $this->id = $id;
        $this->name = $name;
        $this->email_address = $email_address;
    }

    function getId() {
        return $this->id;
    }

    function getName() {
        return $this->name;
    }

    function getEmailAddress() {
        return $this->email_address;
    }

}

