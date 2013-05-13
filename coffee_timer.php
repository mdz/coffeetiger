<?php
// check whether it's business hours and run the program if it is
function business_hours() {
  $ready = NULL;
	global $ready;
	$hour = date('G');
	$day  = date('N');
	$date = date('m/j/y');
	$holidays = array('1/01/13', '1/21/13', '2/18/13', '3/27/13', '07/4/13', '07/5/13', '09/2/13', '11/28/13', '11/29/13', '12/25/13', '12/26/13', '12/27/13', '12/28/13', '12/29/13', '12/30/13', '12/31/13');
	if ((($hour >= 9  && $hour <= 5) || ($day >=1 && $day <= 5)) && ($date != in_array($date, $holidays))) {
  		$ready = true;

// schedule program to run every 30 seconds
$interval=30; //seconds
set_time_limit(0);
while ($ready = true) {
	$now=time();
	include("coffee_interpreter.php");
	sleep($interval*30-(time()-$now));
}
?>
