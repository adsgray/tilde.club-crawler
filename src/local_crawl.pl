#!/usr/bin/perl

use strict;
use HTML::Parser ();

sub get_text_from_html_file($) {
	my ($fname) = @_;
	open (my $fh, "<$fname");
	my @array = ();

	my $p = HTML::Parser->new( api_version => 3,
                         handlers => { text => [\@array, "text"]},
                         marked_sections => 1,
                       );

	my $ret = $p->parse_file($fh);
	close($fh);

	my $acc = "";
	for my $txt (@array) {
		# discard the whitespace chunks that parse_file returns
		if ($txt->[0] !~ /^$/) {
			$acc .= $txt->[0] . " ";
		}
	}

	return $acc;
}

sub get_sentences_from_text($) {
	my ($txt) = @_;
	# elimenate extra whitespace
	$txt =~ s/\s+/ /g;
	# split on perion-space
	return split(/\.\s+/, $txt);
}

# takes an array of sentences and a max length
sub launder_sentences {
	my ($aref, $maxlen) = @_;
	my @ret = ();

	for my $sentence (@{$aref}) {
		if (length($sentence) <= $maxlen) {
			push @ret, $sentence;
		}
	}

	return @ret;
}

sub create_sql_inserts {
	my ($userid, $aref) = @_;

	my $ret = "";

	for my $sentence (@{$aref}) {
		$sentence =~ s/'/\\'/g;
		$ret .= qq|INSERT INTO tweet(user_id, text) VALUES($userid, '$sentence');\n|;
	}

	return $ret;
}


sub process_user {
	my ($userid, $user) = @_;

	my $fname = "/home/$user/public_html/index.html";
	my $txt = get_text_from_html_file($fname);
	my @sentences = get_sentences_from_text($txt);
	# actually, do this in the database select
	#my @tweetable = launder_sentences(\@sentences, 125);

	#print join "\n", @sentences;
	return create_sql_inserts($userid, \@sentences);
}

# all text from html file
my $usermapfile = $ARGV[0];

open (my $usermap, "<$usermapfile") || die "couldn't open usermap file";
while (my $line = <$usermap>) {
	chomp($line);
	my ($userid, $user) = split('\|', $line);
	print process_user($userid, $user);
}
close($usermap);

