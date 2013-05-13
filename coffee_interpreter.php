<?php
// create array to hold input variables
$readings = array($volt0, $volt1, $volt2, $volt3, $volt4);

// get numbers from Arduino site
function get_data() {
  while true {
		global $url;
		$url = (' Arduino IP ');
		global $last_reading;
		$last_reading = file_get_contents($url);
		settype($last_reading, "float");
			return $last_reading;
	}
}

// define empty volts
$empty_decanter = // 4000;
$new_brew = // 5400;
$last_cup = // 650;
$cup = 250;

// rebuild array with new set of input variables
function new_variable() {
	while true {
		$readings[4] = $volt3;
		$readings[3] = $volt2;
		$readings[2] = $volt1;
		$readings[1] = $volt0;
		$readings[0] = $last_reading;
	}
}

// interpreting data and returning analysis of the coffee situation
function coffee_interpreter() {
	global $readings;
	$difference = $readings[1] - $readings[0];
	$prev_diff1 = $readings[2] - $readings[1];
	$prev_diff2 = $readings[3] - $readings[2];
	$prev_diff3 = $readings[4] - $readings[3];
	// is the difference positive
	if ((int)$difference == $difference && (int)$difference > 0) {
		if ((int)$prev_diff1 == $prev_diff1 && (int)$prev_diff1 > 0) {
			if $readings[0] >= $new_brew {
				echo "Coffee is ready!";
			}
			else {
				echo "Coffee is being brewed!";
			}
		}
		else {
			echo "I'm going to have to gather more data.";
		}
	}
	// or negative
	elseif ((int)$difference == $difference && (int)$difference < 0) {
		$cups_remaining = (($readings[0] - $empty_decanter)/$cups);
		// has someone just lifted the decanter?
		if ((int)$prev_diff1 == $prev_diff1 && (int)$prev_diff1 < 0) && ((int)$prev_diff2 == $prev_diff2 && (int)$prev_diff2 < 0) {
				if $readings[0] <= $last_cup || $cups_remaining <= 1 {
					echo "Coffee tiger says, Raaar!";
				}
				elseif {
					echo "There are still about " . ($cups_remaining, 1) . " cups of coffee left!";
				}		
		}
		else {
			echo "Hold on a second here, someone may just be pouring themselves some coffee.";
			break;
		}
	}
	// or no change
	elseif ((int)$difference == $difference && (int)$difference == 0)
		echo "Not much going on around here.";
	}
}

// run the program
get_data($url);
new_variable($last_reading);
coffee_interpreter($readings);
?>
