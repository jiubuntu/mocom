<?php
include 'db_config.php';

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Access-Control-Allow-Headers,Content-Type,Access-Control-Allow-Methods, Authorization, X-Requested-With');

$id = $_POST['id'];

$sql = "DELETE FROM news WHERE no = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $id);
$result = $stmt->execute();

if ($result) {
  echo json_encode(['message' => 'Event added successfully']);
} else {
  echo json_encode(['message' => 'Error adding event']);
}

$conn->close();
?>