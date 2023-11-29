<?php
header('Content-Type: application/json');

require_once '../config.inc.php';

if(isset($_REQUEST['name']) && isset($_REQUEST['email'])) {

    $name = $_REQUEST['name'];
    $email_address = $_REQUEST['email'];

    if(preg_match('/^[a-zA-Z0-9\w]+$/', $name) && 
        preg_match('/^[a-zA-Z0-9\w]+$/', $name) ) {

        $session = $db->createSession($name, $email_address);
        $state = new State($session);

        echo json_encode(array(
            'session_id' => $session->getId(),
            'state' => $state->save()
        ), JSON_PRETTY_PRINT);
    
    } else {
        // hackerz!
        http_response_code(406);
    }

} else {
    http_response_code(400);
}

?>