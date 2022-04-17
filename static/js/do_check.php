if(!empty($_POST["username"]))) {
    $sql = "
    SELECT
    *
        FROM name
        WHERE
            name='" . $_POST["username"] . "' AND
            date_order='" . $_POST["date_order"] . "' AND
            time_order='" . $_POST["time_order"] . "' AND
            table_num='" . $_POST["table_num"] . "'
    ";
           $result = mysql_query($sql);
           if(mysql_num_rows($result) > 0) {
               echo "<span class='status-not-available'> Username Not Available.</span>";
           }
           else{
               echo "<span class='status-available'> Username Available.</span>";
          }
}
else{
    echo "Одно из полей пустое";
}