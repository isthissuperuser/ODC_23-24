<?php

error_reporting(0);
ini_set( 'display_errors', 0  );

$dbname = getenv("DB_NAME");
$dbhost = getenv("DB_HOST");
$dbuser = getenv("DB_USER");
$dbpass = getenv("DB_PASS");

try {
    $db_internal = new PDO("mysql:host=$dbhost;dbname=$dbname", $dbuser, $dbpass);
} catch(PDOException $e) {
    die("Error connecting to the database. If the problem persists, contact an administrator.");
}

require_once "classes/Model.inc.php";

$db = new Model($db_internal);
