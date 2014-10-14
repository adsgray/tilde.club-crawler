#!/usr/bin/perl


sub usersql($$) {
	my ($username, $siteid) = @_;
	return qq|INSERT INTO user (name, site_id) VALUES ('$username', $siteid);|;
}


### Extract users from a "standard" tilde-galaxy site user list
my $site=2;

while (my $line=<>) {
#<li><a href="http://totallynuclear.club/~adrian">adrian</a></li>
	chomp($line);
	if ($line =~ qr|.*a href="http.*/~(\w+)"|) {
	#if ($line =~ qq|.*~(\w+).*|) {
		print usersql($1, $site) . "\n";
	}
}
