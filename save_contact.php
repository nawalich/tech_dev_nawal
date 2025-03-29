<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = htmlspecialchars($_POST["name"]);
    $email = htmlspecialchars($_POST["email"]);
    $message = htmlspecialchars($_POST["message"]);

    $file = "contacts.csv";
    $file_exists = file_exists($file);

    $handle = fopen($file, "a");
    if ($handle) {
        if (!$file_exists) {
            fputcsv($handle, ["Nom", "Email", "Message"]);
        }

        fputcsv($handle, [$name, $email, $message]);
        fclose($handle);
        
        echo "✅ Merci ! Votre message a été enregistré.";
    } else {
        echo "❌ Erreur : Impossible d'enregistrer les données.";
    }
} else {
    echo "❌ Accès non autorisé.";
}
?>
