<html>
<body>
<style>
#players {
  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

#players td, #players th {
  border: 1px solid #ddd;
  padding: 8px;
}

#players tr:nth-child(even){background-color: #f2f2f2;}

#players tr:hover {background-color: #ddd;}

#players th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #4CAF50;
  color: white;
}
</style>
<input type="text" id="myInput" onkeyup="myFunction(1)" placeholder="Search for names..." title="Type in a name">
<?php
$servername = "localhost";
$username = "root";
$password = "raspberry";
$dbname = "theshow";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT * FROM player_19";
$result = $conn->query($sql);
echo "<table id='players'>
		<tr class='header'>
			<th>ID <input type='text' id='myInput0' onkeyup='myFunction(0)' placeholder='Search for ID...' title='Type in a name'></th>
			<th>Name <input type='text' id='myInput1' onkeyup='myFunction(1)' placeholder='Search for names...' title='Type in a name'></th>
			<th>Overall <input type='text' id='myInput2' onkeyup='myFunction(2)' placeholder='Search for Overall...' title='Type in a name'></th>
		</tr>";
if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo 	"<tr>
					<td>".$row["id"]."</td>
					<td>".$row["name"]."</td>
					<td>".$row["ovr"]."</td>
				</tr>";
    }
} else {
    echo "0 results";
}
echo "</table>";
$conn->close();
?>
<script>
function myFunction(z) {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput" + z);
  filter = input.value.toUpperCase();
  table = document.getElementById("players");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[z];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}
</script>
</body>
</html>