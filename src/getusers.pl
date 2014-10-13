#!/usr/bin/perl


$fname = "/etc/passwd";

#create table user(
#	id INTEGER PRIMARY KEY,
#	name varchar(100)
#);
sub usersql($) {
	my $username = shift;
	return qq|INSERT INTO user (name) VALUES ('$username');|;
}

open (my $fh, "<$fname");
while (my $line = <$fh>) {
	chomp($line);
	my @arr = split ':', $line;
	$username = $arr[0];
	if (-d "/home/$username/public_html" && -f "/home/$username/public_html/index.html") {
		print usersql($username) . "\n";
	}
}
close($fh);
