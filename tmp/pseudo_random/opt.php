 <?php

/*
 * one time padding encryption system
 *
 * we generate {$r = random_bytes()} which {strlen($r) == strlen($plaintext)}
 * and encrypt it with {$r ^ $plaintext}, so no body can break our encryption!
 */

// return $len bytes random data without null byte
function random_bytes_not_null($len)
{
    $result = '';
    for($i = 0; $i < $len; $i++)
        $result .= chr(random_int(1, 255));
    return $result;
}

if(empty($_GET['issue_otp'])) {
    highlight_file(__file__);
    exit;
}

require('flag.php');

header('Content-Type: text/plain');

for($i = 0; $i < 20; $i++) {
    // X ^ 0 = X, so we want to avoid null byte to keep your secret safe :)
    $padding = random_bytes_not_null(strlen($flag));
    echo bin2hex($padding ^ $flag)."\n";
}

