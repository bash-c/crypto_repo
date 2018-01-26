<?php
require_once '/home/max/crypto_repo/pseudo_random/Requests/library/Requests.php';
Requests::register_autoloader();

$h = array('Content-Type' => 'text/plain');
$r = Requests::get('https://hackme.inndy.tw/otp/?issue_otp=1', $header = $h);
// echo $r->body."\n\n\n";
for($st = 0; $st <= 2000; $st += 101)
{
	$encrypted = substr($r->body, $st, 100);
	// echo $encrypted."\n\n";
	
	$result = '';
	for($i = 0; $i < 50; $i++)
		$result .= chr(random_int(1, 255));
	
	echo ($result ^ hex2bin($encrypted));
}

?>
