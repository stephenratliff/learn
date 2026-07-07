#!/usr/bin/env perl
# =============================================================================
#  gradebook.pl — A Perl Tour Through a Student Grade Book
# =============================================================================
#  This is a self-contained, working program that covers the core of Perl.
#  Run it with:   perl gradebook.pl
#  Each section introduces new language features, building on the last.
# =============================================================================

use strict;        # Require variable declarations — catches name typos early
use warnings;      # Warn about suspicious code — always have these two lines
use feature 'say'; # Enable say() — like print but adds a newline automatically
use feature 'state';
use List::Util   qw(sum max min);
use Scalar::Util qw(looks_like_number blessed);
use POSIX        qw(floor);

# =============================================================================
# SECTION 1: SCALARS — The basic building block
# =============================================================================
# A scalar holds one value: a string, number, or reference.
# All scalar variables start with $ (the "sigil").

my $class_name    = "Introduction to Programming";   # String
my $teacher       = "Ms. Hernandez";
my $semester      = "Fall 2025";
my $passing_score = 60;           # Integer — no quotes needed
my $bonus_points  = 2.5;          # Float
my $class_open    = 1;            # Perl has no boolean — 1 is true, 0 is false

# Double quotes interpolate variables. Single quotes are always literal.
say "Class:    $class_name";
say 'Teacher:  $teacher';          # prints literally: $teacher
say "Teacher:  $teacher\n";        # \n is a newline; only works in ""

# String operators: . concatenates, x repeats
my $separator = "=" x 50;          # "=================================================="
say $separator;
say "Class: " . $class_name . " — " . $semester;
say $separator . "\n";

# sprintf formats a string (like C's sprintf). printf prints it directly.
my $label = sprintf("%-20s  %s", "Semester:", $semester);
say $label;

# Arithmetic: + - * / % ** (exponent). Numbers auto-convert from strings.
my $weeks        = 16;
my $days         = $weeks * 5;
my $hours        = $days * 1.5;
printf "Weeks: %d  Days: %d  Hours: %.1f\n\n", $weeks, $days, $hours;


# =============================================================================
# SECTION 2: ARRAYS — Ordered lists of scalars
# =============================================================================
# Arrays use @. One element uses $ (you're getting a scalar out).

my @subjects = ("Math", "English", "Science", "History", "Art");
my @scores   = (88, 74, 92, 61, 95);        # A list of numbers
my @counts   = (1..10);                     # Range operator: (1,2,3,...,10)

# qw() = "quote words" — convenient shorthand for a list of strings
my @days = qw(Mon Tue Wed Thu Fri Sat Sun);

say "Subjects:  " . join(", ", @subjects);  # join glues a list into a string
say "First:     $subjects[0]";              # Index from 0
say "Last:      $subjects[-1]";             # Negative index = from the end
say "Count:     " . scalar(@subjects);      # scalar() context = element count
say "Last idx:  $#subjects";               # $#array = index of last element

# Modifying arrays
push    @subjects, "PE";         # Append to end
my $popped = pop @subjects;      # Remove and return from end
unshift @subjects, "Coding";     # Prepend to front
my $shifted = shift @subjects;   # Remove and return from front

say "After push/pop/shift/unshift: " . join(", ", @subjects);

# Slices: extract multiple elements at once
my @first_three = @subjects[0..2];          # Slice with range
my @pick        = @scores[0, 2, 4];        # Slice with explicit indices
say "Slice:   " . join(", ", @first_three);
say "Picked:  " . join(", ", @pick) . "\n";

# sort and reverse
my @sorted  = sort @subjects;              # Alphabetical
my @rsorted = reverse sort @subjects;      # Reverse alphabetical
my @nsorted = sort { $a <=> $b } @scores; # Numeric ascending ($a, $b are special sort vars)
say "Sorted subjects: " . join(", ", @sorted);
say "Sorted scores:   " . join(", ", @nsorted) . "\n";


# =============================================================================
# SECTION 3: HASHES — Key-value pairs (like a dictionary/map)
# =============================================================================
# Hashes use %. One value uses $ (getting a scalar). The "fat comma" =>
# auto-quotes the left side and signals a pair — use it for readability.

my %grade_letter = (
    'A' => 90,
    'B' => 80,
    'C' => 70,
    'D' => 60,
    'F' => 0,
);

my %student_info = (
    name    => "Alice Chen",
    email   => 'alice@school.edu',
    year    => 2,
    gpa     => 3.8,
);

say "Student:  $student_info{name}";
say "GPA:      $student_info{gpa}\n";

# exists: is the key present? defined: is its value not undef?
say "Has 'name'?   " . (exists  $student_info{name}  ? "yes" : "no");
say "Has 'phone'?  " . (exists  $student_info{phone} ? "yes" : "no");

# Adding, deleting
$student_info{phone} = "555-0101";    # Add new key
delete $student_info{phone};          # Remove key

# Iterating a hash — keys returns all keys (in arbitrary order)
say "\nStudent info:";
for my $key (sort keys %student_info) {
    printf "  %-10s => %s\n", $key, $student_info{$key};
}

# each() returns (key, value) pairs — useful for while loops
say "\nGrade thresholds:";
while (my ($letter, $threshold) = each %grade_letter) {
    say "  $letter : $threshold%";
}
say "";


# =============================================================================
# SECTION 4: COMPLEX DATA STRUCTURES — Arrays of Hashrefs
# =============================================================================
# This is the most common real-world pattern. An arrayref [ ] stores an
# anonymous array as a scalar. A hashref { } stores an anonymous hash.
# The arrow operator -> dereferences: $ref->[i] or $ref->{key}

my @students = (
    { name => "Alice Chen",     scores => [92, 88, 95, 91, 87], email => 'alice@school.edu'   },
    { name => "Bob Martinez",   scores => [74, 68, 72, 80, 65], email => 'bob@school.edu'     },
    { name => "Carol Williams", scores => [85, 90, 88, 92, 94], email => 'carol@school.edu'   },
    { name => "David Kim",      scores => [55, 62, 58, 70, 60], email => 'david@school.edu'   },
    { name => "Eve Patel",      scores => [98, 95, 99, 97, 100],email => 'eve@school.edu'     },
    { name => "Frank Johnson",  scores => [41, 50, 38, 45, 55], email => 'frank@school.edu'   },
);

# Accessing nested data
say "Students enrolled: " . scalar(@students);
say "First student:     " . $students[0]{name};         # array[i]{key}
say "Her third score:   " . $students[0]{scores}[2];    # array[i]{key}[j]
say "";

# Dereferencing an arrayref with @{ }
my @alices_scores = @{ $students[0]{scores} };          # Gets the actual array
say "Alice's scores: " . join(", ", @alices_scores) . "\n";


# =============================================================================
# SECTION 5: SUBROUTINES — Reusable named blocks of code
# =============================================================================
# All arguments arrive in @_ as a flat list. Unpack it with my (...) = @_.
# The last evaluated expression is the implicit return value (explicit return
# is clearer and always recommended).

sub calculate_average {
    my (@scores) = @_;
    return 0 unless @scores;           # Guard clause: return early if empty
    return sum(@scores) / scalar(@scores);
}

sub letter_grade {
    my ($avg) = @_;
    return 'A' if $avg >= 90;
    return 'B' if $avg >= 80;
    return 'C' if $avg >= 70;
    return 'D' if $avg >= 60;
    return 'F';
}

# Returning multiple values — Perl lists make this natural
sub score_stats {
    my (@scores) = @_;
    return () unless @scores;
    return (
        avg => calculate_average(@scores),
        max => max(@scores),
        min => min(@scores),
        rng => max(@scores) - min(@scores),
    );
}

# Subroutines can modify caller data through references
sub add_computed_fields {
    my ($student_ref) = @_;                          # Receive a hashref
    my @scores = @{ $student_ref->{scores} };
    my $avg    = calculate_average(@scores);
    $student_ref->{avg}   = $avg;                    # Modify through the ref
    $student_ref->{grade} = letter_grade($avg);
    $student_ref->{pass}  = $avg >= $passing_score ? 1 : 0;
    return $student_ref;                             # Return for method-chaining idiom
}

# Compute fields for every student
add_computed_fields($_) for @students;

say "Subroutine results:";
my $avg   = calculate_average(80, 90, 85, 70);
my $grade = letter_grade($avg);
printf "  avg=%.1f  grade=%s\n", $avg, $grade;
my %stats = score_stats(80, 90, 85, 70, 65);
printf "  max=%d  min=%d  range=%d\n\n", $stats{max}, $stats{min}, $stats{rng};


# =============================================================================
# SECTION 6: CONTROL FLOW — if, unless, ternary, given/when alternative
# =============================================================================

sub describe_score {
    my ($score) = @_;

    # if / elsif / else — standard branching
    if    ($score >= 90) { return "Excellent"    }
    elsif ($score >= 80) { return "Good"         }
    elsif ($score >= 70) { return "Satisfactory" }
    elsif ($score >= 60) { return "Passing"      }
    else                 { return "Failing"      }
}

sub check_honor_roll {
    my ($avg) = @_;
    # unless = "if not" — reads naturally for negative conditions
    unless ($avg >= 90) {
        return "not on honor roll";
    }
    return "HONOR ROLL";
}

# Postfix if/unless — put the condition AFTER a single statement
# Great for guard clauses and short conditional actions
sub safe_percent {
    my ($score, $max) = @_;
    return 0 unless defined $score && $max > 0;   # postfix unless
    return ($score / $max) * 100;
}

# Ternary operator: CONDITION ? VALUE_IF_TRUE : VALUE_IF_FALSE
# Can be cascaded for multi-branch decisions
sub grade_emoji {
    my ($grade) = @_;
    return $grade eq 'A' ? "⭐"
         : $grade eq 'B' ? "✓ "
         : $grade eq 'C' ? "~ "
         : $grade eq 'D' ? "△ "
         :                 "✗ ";
}

say "Control flow examples:";
for my $n (100, 85, 72, 65, 45) {
    printf "  score=%-3d  desc=%-12s  honor=%s  emoji=%s\n",
        $n, describe_score($n), check_honor_roll($n), grade_emoji(letter_grade($n));
}
say "";


# =============================================================================
# SECTION 7: LOOPS — for, foreach, while, until, do/while
# =============================================================================
# 'for' and 'foreach' are identical. $_ is the implicit loop variable.

say "STUDENT REPORT  (" . scalar(@students) . " students)";
say "-" x 60;

# foreach — iterate over a list with an explicit named variable
for my $student (@students) {
    printf "  %-18s  avg:%5.1f  %s  %s\n",
        $student->{name},
        $student->{avg},
        grade_emoji($student->{grade}),
        ($student->{pass} ? "passing" : "FAILING");
}

say "";

# C-style for loop — useful when you need the index
say "Top score per student:";
for (my $i = 0; $i < @students; $i++) {
    my $top = max( @{ $students[$i]{scores} } );
    printf "  [%d] %-18s  top score: %d\n", $i+1, $students[$i]{name}, $top;
}

say "";

# while — runs while condition is true
my $attempts = 0;
my $total    = 0;
while ($attempts < scalar(@students)) {
    $total += $students[$attempts]{avg};
    $attempts++;
}
printf "Class average (while loop): %.1f\n", $total / $attempts;

# until — runs while condition is FALSE (opposite of while)
my $idx = 0;
until ($idx >= scalar(@students)) {
    # do something with $students[$idx]
    $idx++;
}

# do/while — body always runs at least once, condition checked after
my $counter = 0;
do {
    $counter++;
} while ($counter < 3);
say "do/while ran $counter times";

say "";

# last = break, next = continue, redo = restart without re-evaluating condition
say "Students needing extra help (score below 65 at any point):";
STUDENT: for my $s (@students) {
    for my $score (@{ $s->{scores} }) {
        if ($score < 65) {
            say "  " . $s->{name};
            next STUDENT;     # Jump to next iteration of the OUTER loop
        }
    }
}

# Postfix for — iterate with the loop modifier after the statement
my @names = map { $_->{name} } @students;   # Extract names (we'll use map properly below)
say "\nAll names (postfix for):";
say "  $_" for @names;

say "";


# =============================================================================
# SECTION 8: map, grep, sort — Functional list operations
# =============================================================================
# These are the most powerful tools for working with lists in Perl.
# They never modify the original list — they return new ones.

# map: transform every element. The block runs once per element.
# $_ is the current element inside the block.
my @all_avgs = map {
    my @s = @{ $_->{scores} };
    calculate_average(@s)
} @students;

printf "All averages: %s\n", join(", ", map { sprintf("%.0f", $_) } @all_avgs);

# grep: filter — keeps elements where the block returns true
my @passing_students  = grep { $_->{pass}  } @students;
my @failing_students  = grep { !$_->{pass} } @students;
my @honor_roll        = grep { $_->{avg} >= 90 } @students;

say "Passing: "    . scalar(@passing_students) . " students";
say "Failing: "    . scalar(@failing_students) . " students";
say "Honor roll: " . scalar(@honor_roll)        . " students";

# sort: sort with a comparison block. $a and $b are the two elements being compared.
# <=> is numeric comparison returning -1, 0, or 1 (the spaceship operator)
# cmp is the same for strings
my @by_avg_desc = sort { $b->{avg}  <=> $a->{avg}  } @students;   # Descending by avg
my @by_name     = sort { $a->{name} cmp $b->{name} } @students;   # A-Z by name

say "\nRankings (sorted by average):";
my $rank = 1;
for my $s (@by_avg_desc) {
    printf "  %d. %-18s  %.1f  %s\n",
        $rank++, $s->{name}, $s->{avg}, $s->{grade};
}

# Chaining map/grep/sort — the Schwartzian Transform
# For expensive key computations, pre-compute the key before sorting
my @sorted_by_top = map  { $_->[0] }              # 3. Strip back to original
                    sort { $b->[1] <=> $a->[1] }  # 2. Sort by computed key
                    map  { [$_, max(@{$_->{scores}})] }  # 1. Attach the key
                    @students;

say "\nRanked by best single score:";
for my $s (@sorted_by_top) {
    printf "  %-18s  best: %d\n", $s->{name}, max(@{$s->{scores}});
}

# Build a frequency hash with map
my %grade_count;
$grade_count{ $_->{grade} }++ for @students;   # Count each grade letter

say "\nGrade distribution:";
for my $g (sort keys %grade_count) {
    my $bar = "█" x $grade_count{$g};
    printf "  %s: %s (%d)\n", $g, $bar, $grade_count{$g};
}

say "";


# =============================================================================
# SECTION 9: REGULAR EXPRESSIONS — Pattern matching
# =============================================================================
# Regex is built into Perl, not bolted on. =~ binds a string to an operation.
# // is the match operator. s/// is substitution. tr/// is transliteration.

say "REGULAR EXPRESSIONS";
say "-" x 50;

# Basic matching — returns true/false
my $email = 'alice@school.edu';
if ($email =~ /\@/)  { say "  '$email' contains an @ sign"     }
if ($email !~ /\d/)  { say "  '$email' contains no digits"      }

# Modifiers: i=case-insensitive, g=global, m=multiline, x=extended(allow spaces/comments)
my $text = "The student ALICE scored 95 points in MATH class.";
my @words = ($text =~ /\b[A-Z]{2,}\b/g);   # /g in list context = all matches
say "  All-caps words: " . join(", ", @words);

# Capture groups ( ) — matched text goes into $1, $2, ...
for my $student (@students) {
    if ($student->{name} =~ /^(\w+)\s+(.+)$/) {
        $student->{first} = $1;   # $1 = first capture group
        $student->{last}  = $2;   # $2 = second capture group
    }
}
say "  First names: " . join(", ", map { $_->{first} } @students);

# Named captures (?<name>...) — cleaner than positional $1, $2
my $date_str = "Report Date: 2025-09-15";
if ($date_str =~ /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/) {
    my ($y, $m, $d) = @+{qw(year month day)};   # %+ holds named captures
    say "  Date parsed: year=$y  month=$m  day=$d";
}

# Validate email with a regex sub
sub validate_email {
    my ($addr) = @_;
    # ^ = start, \w = word char, [\w.]+ = word chars or dots
    # \@ = literal @, [\w.]+ = domain, \. = dot, \w{2,} = TLD (2+ chars), $ = end
    return $addr =~ /^\w[\w.]*\@[\w.]+\.\w{2,}$/;
}

say "\n  Email validation:";
for my $s (@students) {
    my $ok = validate_email($s->{email}) ? "✓" : "✗";
    say "  $ok  $s->{email}";
}

# Substitution: s/PATTERN/REPLACEMENT/flags
# /g = replace all occurrences, /i = case-insensitive, /r = return copy (don't modify original)
my $report = "student scored EXCELLENT results in all SUBJECTS today.";
(my $cleaned = $report) =~ s/\b([A-Z]+)\b/\u\L$1/g;   # Fix ALLCAPS -> Title Case
say "\n  Original:  $report";
say "  Fixed:     $cleaned";

# s/// with /e flag — replacement is evaluated as Perl code
my $template = "Alice avg is AVG_alice and Bob avg is AVG_bob.";
my %lookup = (alice => $students[0]{avg}, bob => $students[1]{avg});
$template =~ s/AVG_(\w+)/sprintf("%.1f", $lookup{$1})/ge;
say "  Template:  $template";

# tr/// = transliterate (character mapping, not regex)
my $cipher = "Hello World";
(my $rot13 = $cipher) =~ tr/A-Za-z/N-ZA-Mn-za-m/;   # ROT13 encoding
say "\n  ROT13 of '$cipher': $rot13\n";


# =============================================================================
# SECTION 10: REFERENCES — Pointers to data and code
# =============================================================================
# A reference is a scalar that holds the address of another value.
# Think of it as a pointer. \ creates a reference to an existing variable.
# [ ] and { } create anonymous arrayrefs and hashrefs directly.

say "REFERENCES";
say "-" x 50;

# Creating references
my @original  = (10, 20, 30);
my $aref      = \@original;    # Reference to existing array
my $href      = \%grade_letter;# Reference to existing hash
my $anon_aref = [1, 2, 3];    # Anonymous arrayref — no separate variable needed
my $anon_href = {x => 1, y => 2};  # Anonymous hashref

# Dereferencing with -> (arrow notation — preferred for readability)
say "  Via ref: " . $aref->[0];          # Same as $original[0]
say "  Anon:    " . $anon_href->{x};

# Dereferencing the whole thing with @{} or %{}
my @copy    = @{$aref};         # Dereference to get the full array
my %hcopy   = %{$href};         # Dereference to get the full hash

# ref() tells you what kind of reference you have
say "  ref(aref): " . ref($aref);         # "ARRAY"
say "  ref(href): " . ref($href);         # "HASH"

# Passing by reference — modifies the original without copying
sub double_scores {
    my ($scores_ref) = @_;
    for my $s (@{$scores_ref}) {
        $s = min(100, $s * 2);    # Modify elements through the reference
    }
}

my @test_scores = (20, 35, 45);
double_scores(\@test_scores);    # Pass a reference
say "  Doubled: " . join(", ", @test_scores);  # Original is modified

# Code references — storing subroutines in variables
my $square  = sub { $_[0] ** 2  };   # Anonymous sub (lambda)
my $cube    = sub { $_[0] ** 3  };
my $doubled = sub { $_[0] * 2   };

for my $fn ($square, $cube, $doubled) {
    print "  fn(5) = " . $fn->(5) . "\n";
}

# Dispatch table — hash of code refs replaces big if/elsif chains
my %grade_action = (
    'A' => sub { "Excellent — scholarship eligible!" },
    'B' => sub { "Above average — keep it up."       },
    'C' => sub { "Average — room to improve."        },
    'D' => sub { "Below average — tutoring offered." },
    'F' => sub { "Failing — mandatory intervention." },
);

say "\n  Grade messages:";
for my $s (sort { $a->{grade} cmp $b->{grade} } @students) {
    my $msg = $grade_action{ $s->{grade} }->();
    printf "  %s (%s): %s\n", $s->{first}, $s->{grade}, $msg;
}

say "";


# =============================================================================
# SECTION 11: CLOSURES — Functions that remember their environment
# =============================================================================
# A closure is a subroutine that "closes over" variables from the enclosing
# scope. Those variables are captured and kept alive even after the outer
# function returns. This is Perl's version of lambdas / function factories.

say "CLOSURES";
say "-" x 50;

# Factory function — creates a customised filter closure each time it's called
sub make_grade_filter {
    my ($min_avg) = @_;
    # The returned sub remembers $min_avg — it's captured from the enclosing scope
    return sub {
        my ($student) = @_;
        return $student->{avg} >= $min_avg;
    };
}

my $honor_roll_filter = make_grade_filter(90);   # Closure: min=90 is locked in
my $pass_filter       = make_grade_filter(60);   # Closure: min=60 is locked in
my $struggling_filter = make_grade_filter(70);   # Closure: min=70

my @honor = grep { $honor_roll_filter->($_) } @students;
my @at_risk = grep { !$struggling_filter->($_) } @students;

say "  Honor roll: " . join(", ", map { $_->{first} } @honor);
say "  At risk:    " . join(", ", map { $_->{first} } @at_risk);

# State variables — persist between calls without being a global
sub call_counter {
    state $count = 0;     # Initialized once, remembered between calls
    state $total = 0;
    my ($val) = @_;
    $count++;
    $total += $val;
    return ($count, $total, $total / $count);
}

say "\n  Running stats (state variables):";
for my $s (@students) {
    my ($n, $tot, $mean) = call_counter($s->{avg});
    printf "  After %-12s: n=%d  total=%.0f  running_avg=%.1f\n",
        $s->{first}, $n, $tot, $mean;
}

say "";


# =============================================================================
# SECTION 12: FILE I/O — Reading and writing files
# =============================================================================
# Always use 3-argument open(). The 'or die $!' means: crash if open fails,
# printing the system error message stored in $!

say "FILE I/O";
say "-" x 50;

my $report_file = "grade_report.txt";
my $csv_file    = "students.csv";

# --- WRITING ---
open(my $fh, '>', $report_file) or die "Cannot write '$report_file': $!";

# Print to a filehandle — note the space, no comma between handle and string
print $fh "CLASS GRADE REPORT\n";
print $fh "=" x 60 . "\n";
printf $fh "%-15s %s\n", "Class:",    $class_name;
printf $fh "%-15s %s\n", "Teacher:",  $teacher;
printf $fh "%-15s %s\n", "Semester:", $semester;
print $fh "\n";

printf $fh "%-20s  %6s  %5s  %s\n", "Student", "Avg", "Grade", "Scores";
print $fh "-" x 60 . "\n";

for my $s (@students) {
    my $scores_str = join(", ", @{ $s->{scores} });
    printf $fh "%-20s  %6.1f  %5s  [%s]\n",
        $s->{name}, $s->{avg}, $s->{grade}, $scores_str;
}

my $class_avg = calculate_average(@all_avgs);
print $fh "\n" . "-" x 60 . "\n";
printf $fh "Class average: %.1f  (%s)\n", $class_avg, letter_grade($class_avg);
printf $fh "Passing: %d / %d students\n",
    scalar(@passing_students), scalar(@students);

close($fh);   # Always close explicitly when you're done
say "  Report written → $report_file";

# --- WRITING CSV ---
open(my $csv_fh, '>', $csv_file) or die "Cannot write '$csv_file': $!";
print $csv_fh "Name,Email,Average,Grade,Pass\n";   # Header row
for my $s (@students) {
    printf $csv_fh "%s,%s,%.1f,%s,%s\n",
        $s->{name}, $s->{email}, $s->{avg}, $s->{grade},
        ($s->{pass} ? "Y" : "N");
}
close($csv_fh);
say "  CSV written      → $csv_file";

# --- READING LINE BY LINE ---
open(my $in_fh, '<', $report_file) or die "Cannot read '$report_file': $!";
my $line_count = 0;
while (my $line = <$in_fh>) {
    chomp $line;    # Removes the trailing newline character
    $line_count++;
}
close($in_fh);
say "  Lines read:        $line_count";

# --- READING ALL LINES AT ONCE ---
open(my $csv_in, '<', $csv_file) or die "Cannot read '$csv_file': $!";
my @csv_lines = <$csv_in>;   # Slurp all lines into an array
close($csv_in);
chomp @csv_lines;            # chomp works on arrays too
my @csv_data = map { [split /,/, $_] } @csv_lines[1..$#csv_lines]; # Skip header
say "  CSV rows parsed:   " . scalar(@csv_data);
say "  First CSV row:     " . join(" | ", @{$csv_data[0]});

# --- SLURPING ENTIRE FILE INTO A STRING ---
open(my $slurp, '<', $report_file) or die $!;
my $content = do { local $/; <$slurp> };   # local $/ = undef disables line-mode
close($slurp);

my $word_count = scalar(split /\s+/, $content);
say "  Words in report:   $word_count\n";

# File tests — check properties without opening the file
say "  -e (exists):    " . (-e $report_file ? "yes" : "no");
say "  -f (is a file): " . (-f $report_file ? "yes" : "no");
say "  -r (readable):  " . (-r $report_file ? "yes" : "no");
say "  -s (size):      " . (-s $report_file) . " bytes\n";


# =============================================================================
# SECTION 13: ERROR HANDLING — eval, die, $@
# =============================================================================
# eval { } is Perl's try. die is throw. $@ holds the caught exception.
# Putting \n at the end of die's message suppresses the "at line N" suffix.

say "ERROR HANDLING";
say "-" x 50;

sub safe_divide {
    my ($a, $b) = @_;
    die "Division by zero!\n" if $b == 0;
    return $a / $b;
}

# Basic eval/die — catching string errors
for my $pair ([10, 2], [7, 0], [15, 4]) {
    my ($a, $b) = @$pair;
    my $result = eval { safe_divide($a, $b) };

    if ($@) {
        # $@ holds the die message after an eval block catches it
        printf "  CAUGHT: %d/%d — %s", $a, $b, $@;
    } else {
        printf "  OK:     %d / %d = %.2f\n", $a, $b, $result;
    }
}

# Die with a reference for structured/typed exceptions
sub load_student_file {
    my ($filename) = @_;
    unless (-e $filename) {
        die {
            type    => "FileNotFound",
            file    => $filename,
            message => "The file does not exist"
        };
    }
    open(my $fh, '<', $filename) or die {
        type    => "OpenFailed",
        file    => $filename,
        message => "Could not open: $!"
    };
    close $fh;
}

eval { load_student_file("ghost_file.csv") };
if (my $err = $@) {
    if (ref($err) eq 'HASH') {
        # Structured exception — access fields cleanly
        printf "\n  [%s] %s: %s\n", $err->{type}, $err->{file}, $err->{message};
    } else {
        print "\n  String error: $err";
    }
}

# warn is like die but doesn't stop execution — it prints to STDERR
warn "  This is a warning — execution continues.\n";
say "";


# =============================================================================
# SECTION 14: OBJECT-ORIENTED PERL — Packages, bless, methods, inheritance
# =============================================================================
# A package is a namespace/class. bless($hashref, $classname) makes an object.
# Methods are subroutines where the first argument is the object ($self).
# By convention, the constructor is named new().

package Student;

sub new {
    my ($class, %args) = @_;
    die "name is required\n"  unless defined $args{name};
    die "email is required\n" unless defined $args{email};

    my $self = {
        name   => $args{name},
        email  => $args{email},
        scores => $args{scores} // [],    # // is "defined-or": use [] if undef
    };

    return bless $self, $class;   # bless ties $self to this package (class)
}

# Accessor: read or write the name
sub name {
    my ($self, $new) = @_;
    $self->{name} = $new if defined $new;   # Set if argument given
    return $self->{name};                   # Always return current value
}

sub add_score {
    my ($self, $score) = @_;
    die "Score must be 0–100\n" unless $score >= 0 && $score <= 100;
    push @{ $self->{scores} }, $score;
    return $self;    # Return $self to allow method chaining: $s->add_score(90)->add_score(85)
}

sub average {
    my ($self) = @_;
    my @s = @{ $self->{scores} };
    return 0 unless @s;
    return List::Util::sum(@s) / scalar(@s);
}

sub grade {
    my ($self) = @_;
    my $avg = $self->average();
    return 'A' if $avg >= 90;
    return 'B' if $avg >= 80;
    return 'C' if $avg >= 70;
    return 'D' if $avg >= 60;
    return 'F';
}

# Stringification — called when the object is used as a string
sub to_string {
    my ($self) = @_;
    return sprintf("%-18s  avg:%.1f  grade:%s",
        $self->{name}, $self->average(), $self->grade());
}


# --- Subclass with inheritance ---
package HonorsStudent;
use parent -norequire, 'Student';   # -norequire: parent defined in this file

sub new {
    my ($class, %args) = @_;
    my $self = $class->SUPER::new(%args);   # Call Student::new
    $self->{bonus} = $args{bonus} // 5;     # Extra field for this subclass
    return $self;
}

# Override average() to add bonus points — super call keeps parent logic intact
sub average {
    my ($self) = @_;
    return $self->SUPER::average() + $self->{bonus};
}

sub to_string {
    my ($self) = @_;
    return $self->SUPER::to_string() . " [Honors +$self->{bonus}pts]";
}


# Back to main execution
package main;

say "OBJECT-ORIENTED PERL";
say "-" x 50;

# Instantiate with method chaining
my $s1 = Student->new(name => "Grace Lee", email => 'grace@school.edu');
$s1->add_score(88)->add_score(92)->add_score(95);   # Method chaining

my $s2 = HonorsStudent->new(name => "Henry Park", email => 'henry@school.edu', bonus => 5);
$s2->add_score(82)->add_score(86)->add_score(79);

say "  " . $s1->to_string();
say "  " . $s2->to_string();

# Polymorphism — same call, different behaviour
for my $student ($s1, $s2) {
    printf "  %-12s  class=%s  isa Student=%s\n",
        $student->name(),
        ref($student),                             # Returns class name
        ($student->isa('Student') ? "yes" : "no"); # Inheritance check
}

# Build objects from raw data
my @oo_students = map {
    Student->new(name => $_->{name}, email => $_->{email}, scores => $_->{scores})
} @students;

say "\n  OOP grade distribution:";
my %oo_grade_count;
$oo_grade_count{ $_->grade() }++ for @oo_students;
for my $g (sort keys %oo_grade_count) {
    say "  $g: " . $oo_grade_count{$g} . " student(s)";
}

say "";


# =============================================================================
# SECTION 15: SPECIAL VARIABLES & CONTEXT
# =============================================================================

say "SPECIAL VARIABLES & CONTEXT";
say "-" x 50;

# $_ — the default variable. Used implicitly by map, grep, for, print, chomp, etc.
my @things = qw(apple banana cherry);
say "  Before: @things";
for (@things) {
    s/a/\@/g;   # s/// without =~ operates on $_ by default
}
say "  After:  @things";

# $! — system error from last failed OS call
unless (open(my $bad, '<', 'no_such_file.txt')) {
    say "  \$! error: $!";
}

# $0 — name of the current script
say "  Script name (\$0): $0";

# wantarray() — tells you what context your sub was called in
sub context_demo {
    if (wantarray()) {
        return (1, 2, 3);        # List context: my @a = context_demo()
    } else {
        return "scalar result";  # Scalar context: my $s = context_demo()
    }
}

my @list_result   = context_demo();   say "  List context:   @list_result";
my $scalar_result = context_demo();   say "  Scalar context: $scalar_result";

# Context affects built-ins too
my @arr = (5, 3, 8, 1, 9);
my $count    = @arr;      # Scalar context: number of elements
my ($first)  = @arr;      # List context (parens!): first element
say "  \@arr in scalar: $count (element count)";
say "  (\$first) = \@arr: $first (first element)";

# Chained string operations using $_
say "\n  Chained on \$_:";
for (qw(hello WORLD fOo)) {
    say "  Original: $_  Uppercase: " . uc . "  Length: " . length;
}

say "";


# =============================================================================
# FINAL SUMMARY
# =============================================================================

say "=" x 60;
say "TOUR COMPLETE — Files written to current directory:";
say "  • $report_file";
say "  • $csv_file";
say "";
say "Topics covered:";
my @topics = (
    "Scalars, strings, numbers",
    "Arrays — push/pop/shift/unshift/splice/slice",
    "Hashes — keys/values/each/exists/delete",
    "Complex data structures (AoH, HoA, nested refs)",
    "Subroutines — unpacking \@_, guard clauses, return",
    "Control flow — if/elsif/unless/ternary/postfix",
    "Loops — for/foreach/while/until/do-while + last/next",
    "map — transform lists",
    "grep — filter lists",
    "sort — comparator block, Schwartzian Transform",
    "Regular expressions — match/substitute/capture",
    "References — \\, [], {}, sub{}, arrow notation ->",
    "Closures — captured variables, factory functions",
    "File I/O — open/close/chomp/slurp/csv/file tests",
    "Error handling — eval/die/\$\@/warn/structured exceptions",
    "OOP — package/bless/new/methods/inheritance/SUPER",
    "Special variables — \$_, \$!, \$\@, \$0, wantarray()",
);
printf "  %2d. %s\n", $_, $topics[$_-1] for 1..scalar(@topics);
say "=" x 60;
