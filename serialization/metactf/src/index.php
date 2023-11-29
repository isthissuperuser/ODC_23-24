<?php
include 'base.php';
?>

<h1>Welcome to METACTF</h1>

<?php

if(isset($_SESSION["user"]) && isset($_SESSION["challenges"])){

    foreach ($_SESSION["challenges"] as &$c) {
        printf("<div> <span> Name: %s </span> <p> Desc: %s </p> <p> Points: %d </p> </div>", $c["name"], $c["descriptions"], $c["points"]);
    }

}
?>


<?php
include 'footer.php';
?>
