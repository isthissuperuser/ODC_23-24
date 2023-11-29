<?php
include 'base.php';
?>

<h1>Welcome to METACTF</h1>


  <form enctype="multipart/form-data" action="/upload_user.php" method="post">
  <div style="margin: 32px; display: flex; justify-content: center">
    <p style="margin: 0">User Backup file:&nbsp</p>
    <input type="file"
           id="user_bak" name="user_bak">
    <br/>
  </div>
  <div style="margin: 32px; justify-content: center">
    <button class="btn" id="restart">Load User</button>
  </div>
  </form>


  <?php
  if (isset($_FILES['user_bak'])){
      $filename = $_FILES['user_bak']["tmp_name"];
      $file = fopen($filename, "r");
      $data= fread($file,filesize($filename));
      fclose($file);
      $data = unserialize($data);
      $_SESSION['user'] = $data;
      }
  ?>


<?php
include 'footer.php';
?>
