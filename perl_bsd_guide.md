# The Comprehensive Perl Programming Guide
## Including FreeBSD 16 GUI Development via Lima &amp; Perl/Tk

> **How to use this guide:** Read each section, then open the matching tutorial file.
> Run the core language tutorial with `perl perl_tutorial.pl`.
> Run each GUI example with `perl perl_gui_XX_name.pl` (requires a display).

---

## Table of Contents

### Part I — The Perl Language
1. [Introduction to Perl](#1-introduction-to-perl)
2. [Running Perl Programs](#2-running-perl-programs)
3. [Scalars — The Basic Variable](#3-scalars--the-basic-variable)
4. [Strings & String Operators](#4-strings--string-operators)
5. [Numbers & Numeric Operators](#5-numbers--numeric-operators)
6. [Arrays](#6-arrays)
7. [Hashes](#7-hashes)
8. [Control Flow](#8-control-flow)
9. [Loops](#9-loops)
10. [Regular Expressions](#10-regular-expressions)
11. [Subroutines (Functions)](#11-subroutines-functions)
12. [References & Complex Data Structures](#12-references--complex-data-structures)
13. [File I/O](#13-file-io)
14. [Modules & Packages](#14-modules--packages)
15. [Error Handling](#15-error-handling)
16. [Object-Oriented Perl](#16-object-oriented-perl)
17. [Useful Built-in Functions](#17-useful-built-in-functions)
18. [Command-Line Arguments](#18-command-line-arguments)
19. [Perl Best Practices](#19-perl-best-practices)

### Part II — GUI Development on FreeBSD 16 via Lima
20. [GUI Overview & Toolkit Choices on FreeBSD](#20-gui-overview--toolkit-choices-on-freebsd)
21. [Setting Up FreeBSD 16 via Lima](#21-setting-up-freebsd-16-via-lima)
22. [Perl/Tk Core Concepts](#22-perltk-core-concepts)
23. [Widgets — The Building Blocks](#23-widgets--the-building-blocks)
24. [Layout Managers: pack, grid, place](#24-layout-managers-pack-grid-place)
25. [Events, Bindings & Callbacks](#25-events-bindings--callbacks)
26. [Menus & Dialogs](#26-menus--dialogs)
27. [The Canvas Widget](#27-the-canvas-widget)
28. [Building a Complete Application](#28-building-a-complete-application)
29. [FreeBSD-Specific Tips & Best Practices](#29-freebsd-specific-tips--best-practices)

---

# PART I — THE PERL LANGUAGE

---

## 1. Introduction to Perl

**Perl** (Practical Extraction and Report Language) was created by Larry Wall in 1987. It excels at:
- **Text processing** and pattern matching
- **System administration** scripting
- **Web/CGI** development
- **Rapid prototyping**
- **GUI applications** (via Tk, Wx, and other toolkits)

Perl's motto: **"There's More Than One Way To Do It" (TMTOWTDI)**

| Feature | Description |
|---|---|
| Interpreted | Runs via the Perl interpreter |
| Dynamically typed | Variables need no type declarations |
| Garbage collected | Automatic memory management |
| CPAN | 25,000+ reusable modules available |
| Tk integration | Mature GUI toolkit, tightly bound to Perl |

---

## 2. Running Perl Programs

### The Shebang Line
```perl
#!/usr/bin/perl
# On FreeBSD with ports Perl (recommended):
#!/usr/local/bin/perl
# Portable (searches PATH — works everywhere):
#!/usr/bin/env perl
```

### Always Use These
```perl
use strict;
use warnings;
```

### Running Scripts
```bash
perl myscript.pl               # Run normally
perl -c myscript.pl            # Syntax check only
perl -w myscript.pl            # Warnings on
perl -e 'print "Hello\n";'     # One-liner
```

### Comments
```perl
# Single-line comment

=pod
Multi-line POD documentation block —
acts as a block comment and generates docs.
=cut
```

---

## 3. Scalars — The Basic Variable

A **scalar** holds one value: a number, string, or reference. Names begin with `$`.

```perl
my $name    = "Alice";
my $age     = 30;
my $pi      = 3.14159;
my $nothing = undef;
```

### Interpolation
```perl
my $city = "San Francisco";
print "Welcome to $city!\n";        # Interpolates
print 'No interpolation: $city\n';  # Literal
```

### Escape Sequences
| Sequence | Meaning |
|---|---|
| `\n` | Newline |
| `\t` | Tab |
| `\\` | Backslash |
| `\"` | Double-quote |
| `\$` | Literal dollar sign |

### Checking Defined
```perl
print defined($nothing) ? "defined" : "undef";
```

---

## 4. Strings & String Operators

```perl
my $full = "Hello" . ", " . "World!";   # Concatenation
my $line = "-" x 40;                     # Repetition
```

### Key String Functions
| Function | Description |
|---|---|
| `length($s)` | Character count |
| `uc($s)` / `lc($s)` | Upper / lower case |
| `ucfirst($s)` | Capitalize first char |
| `substr($s, $off, $len)` | Extract substring |
| `index($s, $sub)` | Find position |
| `chomp($s)` | Remove trailing newline |
| `chop($s)` | Remove last character |
| `reverse($s)` | Reverse string |
| `sprintf(fmt, ...)` | Formatted string |
| `trim` | Use regex: `s/^\s+|\s+$//g` |

### String Comparison
| Operator | Meaning |
|---|---|
| `eq` / `ne` | Equal / not equal |
| `lt` / `gt` | Less / greater than |
| `le` / `ge` | Less-or-equal / greater-or-equal |
| `cmp` | Returns -1, 0, or 1 |

### Here-Docs
```perl
my $text = <<END;
Line one
Line two
END
```

### sprintf Format Reference
| Spec | Type | Example |
|---|---|---|
| `%s` | String | `"hello"` |
| `%d` | Integer | `42` |
| `%f` | Float | `3.14` |
| `%e` | Scientific | `1.23e+04` |
| `%x` / `%X` | Hex | `ff` / `FF` |
| `%b` | Binary | `1010` |
| `%08d` | Zero-padded 8-wide | `00000042` |
| `%-10s` | Left-justified 10-wide | `"hello     "` |
| `%+d` | Show sign | `+5` or `-3` |

---

## 5. Numbers & Numeric Operators

```perl
my $hex  = 0xFF;       # 255
my $oct  = 0755;       # 493
my $bin  = 0b1010;     # 10
my $big  = 1_000_000;  # Readable millions
```

### Arithmetic
| Op | Meaning | Example |
|---|---|---|
| `+` `-` `*` `/` | Basic math | `5 + 3` → 8 |
| `%` | Modulus | `10 % 3` → 1 |
| `**` | Exponent | `2 ** 8` → 256 |
| `++` `--` | Inc / dec | `$n++` |

### Numeric Comparison
`==`  `!=`  `<`  `>`  `<=`  `>=`  `<=>`

### Math Functions
```perl
use POSIX qw(floor ceil);
abs(-5)       # 5
int(3.9)      # 3
sqrt(16)      # 4
floor(3.7)    # 3
ceil(3.2)     # 4
log(exp(1))   # 1 (natural log)
```

---

## 6. Arrays

Ordered lists. Names begin with `@`. Elements accessed with `$arr[idx]`.

```perl
my @colors = ("red", "green", "blue");
my @range  = (1..10);
my @words  = qw(one two three four);
```

### Essential Operations
```perl
push @arr, $val;         # Add to end
my $v = pop @arr;        # Remove from end
unshift @arr, $val;      # Add to front
my $v = shift @arr;      # Remove from front
splice(@arr, $idx, $n);  # Remove n elements at idx
my $size = scalar @arr;  # Count elements
my $last = $#arr;        # Last index
```

### Functional Operations
```perl
my @evens   = grep { $_ % 2 == 0 } @nums;
my @doubled = map  { $_ * 2 }      @nums;
my @sorted  = sort { $a <=> $b }   @nums;   # Numeric
my @alpha   = sort                 @words;  # String
my $csv     = join(",", @words);
my @parts   = split(/,/, $csv);
```

---

## 7. Hashes

Key-value stores. Names begin with `%`. Elements accessed with `$hash{key}`.

```perl
my %person = (
    name  => "Bob",
    age   => 25,
    city  => "Austin",
);
```

### Operations
```perl
$person{email} = "b@x.com";    # Add key
delete $person{city};            # Remove key
exists $person{name};            # Key present?
defined $person{age};            # Value defined?

foreach my $key (sort keys %person) {
    print "$key: $person{$key}\n";
}
```

### qw() — Quote Words
```perl
my @days = qw(Mon Tue Wed Thu Fri Sat Sun);
```

---

## 8. Control Flow

```perl
if ($x > 10)    { ... }
elsif ($x > 5)  { ... }
else            { ... }

unless ($error) { ... }           # Opposite of if

# Postfix (statement modifier)
print "ok\n" if $flag;
print "no\n" unless $flag;

# Ternary
my $label = ($n > 0) ? "positive" : "non-positive";

# Defined-or
my $val = $input // "default";

# Logical operators
&&  ||  !    (high precedence)
and or  not  (low precedence — good for flow control)
//           (defined-or)
```

---

## 9. Loops

```perl
# while
while ($i < 10) { $i++; }

# until (opposite of while)
until ($done) { ... }

# C-style for
for (my $i = 0; $i < 10; $i++) { ... }

# foreach
foreach my $item (@array) { ... }

# Postfix
print "$_\n" for @array;

# Loop control
next;           # Skip to next iteration
last;           # Break out of loop
redo;           # Restart iteration
next OUTER;     # Jump to outer loop label
```

---

## 10. Regular Expressions

```perl
# Match
if ($str =~ /pattern/i)  { ... }    # i = case-insensitive
if ($str !~ /pattern/)   { ... }    # Negated match

# Substitution
$str =~ s/old/new/g;     # Global replace
$str =~ s/old/new/gi;    # Global, case-insensitive

# Transliteration
$str =~ tr/a-z/A-Z/;     # To uppercase

# Capture groups
if ($date =~ /(\d{4})-(\d{2})-(\d{2})/) {
    my ($y, $m, $d) = ($1, $2, $3);
}

# Named captures
$str =~ /(?<year>\d{4})-(?<month>\d{2})/;
print $+{year};

# Global capture to list
my @nums = ("a1b2c3" =~ /(\d)/g);   # (1, 2, 3)
```

### Quick Reference
| Pattern | Matches |
|---|---|
| `.` | Any char (not newline) |
| `\d` `\D` | Digit / non-digit |
| `\w` `\W` | Word char / non-word |
| `\s` `\S` | Whitespace / non-space |
| `^` `$` | Start / end of string |
| `\b` | Word boundary |
| `*` `+` `?` | 0+, 1+, 0 or 1 |
| `{n,m}` | Between n and m |
| `*?` `+?` | Non-greedy |

---

## 11. Subroutines (Functions)

```perl
sub add {
    my ($x, $y) = @_;
    return $x + $y;
}

# Multiple return values
sub divmod {
    my ($a, $b) = @_;
    return (int($a/$b), $a % $b);
}

# Named parameters via hash
sub connect {
    my (%args) = @_;
    my $host = $args{host} // "localhost";
    my $port = $args{port} // 8080;
}

# Anonymous sub / closure
my $square = sub { $_[0] ** 2 };
print $square->(5);   # 25

# Factory (closure over variable)
sub make_adder {
    my ($n) = @_;
    return sub { $_[0] + $n };
}
my $add5 = make_adder(5);
print $add5->(3);     # 8
```

---

## 12. References & Complex Data Structures

```perl
# Create references
my $aref = \@array;       # Ref to array
my $href = \%hash;        # Ref to hash
my $aref = [1, 2, 3];    # Anonymous array ref
my $href = {a => 1};     # Anonymous hash ref

# Arrow notation (dereference)
$aref->[0]               # Array element
$href->{key}             # Hash value
$cref->()                # Call sub ref

# Array of hashes (record list)
my @people = (
    { name => "Alice", age => 30 },
    { name => "Bob",   age => 25 },
);
foreach my $p (@people) {
    print "$p->{name} is $p->{age}\n";
}

# Hash of arrays
my %groups = (
    admins => ["Alice", "Bob"],
    users  => ["Carol", "Dave"],
);
push @{ $groups{admins} }, "Eve";
```

---

## 13. File I/O

```perl
# Three-argument open — always use this form
open(my $fh, "<",  $file) or die "Cannot open: $!";  # Read
open(my $fh, ">",  $file) or die "Cannot open: $!";  # Write
open(my $fh, ">>", $file) or die "Cannot open: $!";  # Append

# Read line by line
while (my $line = <$fh>) {
    chomp $line;
    # process $line
}

# Slurp whole file
my $content = do { local $/; <$fh> };

# Write
print $fh "Hello\n";
printf $fh "Value: %d\n", 42;
close($fh);

# File tests
-e $f   # Exists
-f $f   # Regular file
-d $f   # Directory
-r $f   # Readable
-w $f   # Writable
-s $f   # Size in bytes
```

---

## 14. Modules & Packages

```perl
use ModuleName;                        # Import all defaults
use ModuleName qw(func1 func2);       # Import specific
use strict; use warnings;             # Always

# Key standard modules
use POSIX        qw(floor ceil);
use List::Util   qw(sum min max first any all reduce);
use Scalar::Util qw(looks_like_number blessed);
use Data::Dumper;
use Carp         qw(carp croak confess);
use File::Basename qw(basename dirname);
```

### Creating a Module
```perl
# MyModule.pm
package MyModule;
use strict; use warnings;
use Exporter qw(import);
our @EXPORT_OK = qw(my_func);

sub my_func { ... }
1;   # Must end with true value
```

### CPAN — Installing Modules on FreeBSD
```bash
# Via pkg — fastest, pre-built binaries (preferred for common modules)
pkg install p5-Module-Name

# Via cpanminus — builds from source
cpanm Module::Name

# Via ports
cd /usr/ports/category/p5-Module && make install clean
```

---

## 15. Error Handling

```perl
# die and warn
die  "Fatal error\n";       # Exits, prints to STDERR
warn "Non-fatal\n";         # Continues, prints to STDERR

# eval — catch exceptions
eval {
    die "oops\n";
};
print "Caught: $@" if $@;

# die with a hash object
eval {
    die { code => 404, msg => "Not found" };
};
if (ref $@ eq 'HASH') {
    print "Error $@->{code}: $@->{msg}\n";
}

# or die pattern
open(my $fh, "<", $file) or die "Cannot open $file: $!";
```

---

## 16. Object-Oriented Perl

```perl
package Animal;

sub new {
    my ($class, %args) = @_;
    return bless {
        name  => $args{name}  // "Unknown",
        sound => $args{sound} // "...",
    }, $class;
}

sub name  { $_[0]->{name}  }
sub sound { $_[0]->{sound} }
sub speak { printf "%s says %s\n", $_[0]->name, $_[0]->sound }

package Dog;
our @ISA = ('Animal');

sub new {
    my ($class, %args) = @_;
    $args{sound} = "Woof";
    return $class->Animal::new(%args);
}
sub fetch { print "$_[0]->{name} fetches!\n" }

# Usage
package main;
my $d = Dog->new(name => "Rex");
$d->speak;          # Rex says Woof
ref($d);            # "Dog"
$d->isa("Animal");  # true
```

---

## 17. Useful Built-in Functions

```perl
# String
sprintf("%-10s %5.2f", "item", 3.14)
substr($s, $start, $len, $replacement)   # 4-arg replaces in place
index($s, $sub, $pos)
scalar reverse("hello")

# List
sort { $a cmp $b  } @words    # String sort
sort { $a <=> $b  } @nums     # Numeric sort
sort { length($a) <=> length($b) } @words   # By length

# Reduce (List::Util)
use List::Util qw(reduce);
my $product = reduce { $a * $b } 1..5;    # 120

# Unique elements
my %seen; my @unique = grep { !$seen{$_}++ } @arr;

# Frequency count
my %freq; $freq{$_}++ for @arr;

# Time
time()              # Unix timestamp
scalar localtime()  # Human-readable string

# System
system("cmd");         # Run command
my $out = `cmd`;       # Capture output
exit(0);               # Terminate
```

---

## 18. Command-Line Arguments

```perl
# @ARGV holds all arguments
my ($file, $count) = @ARGV;

# Getopt::Long for flags
use Getopt::Long;
GetOptions(
    "verbose|v"  => \$verbose,
    "output|o=s" => \$output,
    "count|n=i"  => \$count,
) or die "Usage: $0 [--verbose] [--output FILE]\n";
```

---

## 19. Perl Best Practices

✅ Always `use strict; use warnings;`
✅ Declare every variable with `my`
✅ Three-argument `open` with `or die`
✅ `chomp` input from files and STDIN
✅ Use `//` (defined-or) for defaults
✅ `Data::Dumper` for debugging complex structures
✅ `Carp` (`croak`/`carp`) over `die`/`warn` inside modules
🔵 Prefer `foreach` over C-style `for` loops
🔵 Use hash-based args for functions with 3+ parameters
🔵 Schwartzian Transform for expensive sorts
❌ Avoid two-argument `open`
❌ Never declare `my $a` or `my $b` — they shadow sort's globals
❌ Avoid deeply nested structures without clear documentation

---

---

# PART II — GUI DEVELOPMENT ON FreeBSD 16 VIA LIMA

---

## 20. GUI Overview & Toolkit Choices on FreeBSD

**Lima** (Linux Machines — despite the name it supports BSD guests) runs
FreeBSD 16 as a QEMU virtual machine on a macOS host, exposing a full
shell and forwarding X11 so Perl/Tk windows render natively via XQuartz.

### Why FreeBSD for Perl/Tk?
FreeBSD ships an excellent ports/packages tree with pre-compiled Perl/Tk
binaries. The X11 environment is first-class, Tk renders crisply under
Xorg, and FreeBSD's base system is stable and predictable.

### Perl/Tk (Recommended for Learning)
| Pros | Cons |
|---|---|
| Mature, huge documentation | Not themed to a specific desktop |
| Tightly integrated with Perl | Requires Tcl/Tk under the hood |
| 40+ widget types | Older API design |
| Cross-platform (FreeBSD, Linux, macOS, Windows) | |

### Other Options on FreeBSD
| Toolkit | Package | Notes |
|---|---|---|
| **Tkx** | `p5-Tkx` | Modern Tk binding, cleaner API |
| **wxPerl** | `p5-Wx` | Native look via wxWidgets |
| **Prima** | `p5-Prima` | Full-featured, cross-platform |
| **Gtk3** | `p5-Gtk3` | GTK3, looks native under GNOME/XFCE |

> **For learning**, Perl/Tk (`p5-Tk`) is the best starting point — largest
> community, most examples, and it works perfectly over Lima's X11 bridge.

---

## 21. Setting Up FreeBSD 16 via Lima

Lima runs on macOS and manages QEMU-based VMs. After setup, every
`limactl shell freebsd16` session gives you a full FreeBSD 16 environment
with X11 forwarding pre-configured.

### Step 1 — Install Lima on your macOS host
```bash
brew install lima
```

### Step 2 — Create a FreeBSD 16 VM
Lima ships a ready-made FreeBSD template. Create and start the VM:
```bash
limactl create --name freebsd16 template://freebsd
limactl start freebsd16
```

The first start downloads the FreeBSD disk image (≈ 500 MB) and boots the VM.
Progress is shown in the terminal.

### Step 3 — Install XQuartz on your macOS host
XQuartz is the X11 server that receives GUI windows from the Lima VM:
```bash
brew install --cask xquartz
```
Then **log out and log back in** to activate XQuartz's X11 socket.

### Step 4 — Connect to the VM
```bash
limactl shell freebsd16
```
Lima automatically sets `DISPLAY` for X11 forwarding. Verify it:
```bash
echo $DISPLAY     # Should print something like :0 or localhost:10.0
```

### Step 5 — Inside FreeBSD: Update the package database
```bash
pkg update
pkg upgrade        # optional but recommended
```

### Step 6 — Install Perl 5
FreeBSD 16 includes a minimal Perl in base. Install the full ports Perl:
```bash
pkg install perl5
```
Verify:
```bash
perl -v            # Should show v5.36 or newer
which perl         # /usr/local/bin/perl
```

### Step 7 — Install Perl/Tk
```bash
pkg install p5-Tk
```
This installs Perl/Tk and all Tcl/Tk dependencies in one step.

### Step 8 — Install cpanminus (for extra modules)
```bash
pkg install p5-App-cpanminus
# or fetch directly:
fetch -o /tmp/cpanm https://cpanmin.us && perl /tmp/cpanm App::cpanminus
```

### Step 9 — Test Perl/Tk with X11 forwarding
```bash
perl -e '
    use Tk;
    my $mw = MainWindow->new;
    $mw->title("Tk on FreeBSD 16 via Lima");
    $mw->Label(-text => "Hello from Perl/Tk!")->pack;
    $mw->Button(-text => "Close", -command => sub { exit })->pack;
    MainLoop;
'
```
A window should appear on your macOS desktop via XQuartz. If it does, you're ready.

### Step 10 — Install Useful Extra Modules
```bash
pkg install p5-Tk-Pod          # Browse Tk documentation
cpanm Tk::ToolBar              # Toolbar widget
cpanm Tk::ProgressBar          # Progress bar widget
```

### Lima X11 Troubleshooting
```bash
# If the window doesn't appear, try:
export DISPLAY=:0
# or
export DISPLAY=$(grep nameserver /etc/resolv.conf | awk '{print $2}'):0

# Confirm XQuartz is running on the macOS host:
# Applications → Utilities → XQuartz  (or: open -a XQuartz)

# Test basic X11 connectivity:
pkg install xterm
xterm &    # Should open a terminal window on your macOS desktop
```

---

## 22. Perl/Tk Core Concepts

### The Event Loop
A GUI program is fundamentally different from a script. Instead of running top-to-bottom, it:
1. Builds all its widgets
2. Enters `MainLoop`
3. Waits for events (mouse clicks, key presses, timers)
4. Calls your callback subroutines in response
5. Exits when the main window closes

```
Build Widgets → MainLoop → [wait] → Event fires → Callback runs → [back to wait]
```

### Every Tk Program Has This Structure
```perl
#!/usr/bin/env perl
use strict;
use warnings;
use Tk;

# 1. Create the main window
my $mw = MainWindow->new;
$mw->title("My App");
$mw->geometry("400x300");   # WxH in pixels

# 2. Create widgets
my $label = $mw->Label(-text => "Hello!")->pack;

# 3. Enter the event loop — never returns until window closes
MainLoop;
```

### The Widget Hierarchy
All widgets are children of a parent. The main window is the root:
```
MainWindow
  └── Frame (container)
       ├── Label
       ├── Entry
       └── Button
```

### Option Syntax
Widgets are configured with **-option => value** pairs:
```perl
$mw->Label(
    -text       => "Name:",
    -font       => "Helvetica 14 bold",
    -foreground => "blue",
    -background => "#f0f0f0",
    -width      => 20,
    -anchor     => "w",        # west = left-align
)->pack;
```

### Configuring After Creation
```perl
my $lbl = $mw->Label(-text => "original");
$lbl->configure(-text => "updated", -foreground => "red");
my $current = $lbl->cget(-text);   # Get current value
```

### Variable Tracing with -textvariable
```perl
my $message = "Hello";
$mw->Label(-textvariable => \$message)->pack;

# Changing $message later automatically updates the label:
$message = "World";   # Label immediately shows "World"
```

---

## 23. Widgets — The Building Blocks

### Widget Quick Reference

| Widget | Purpose |
|---|---|
| `Label` | Display text or images |
| `Button` | Clickable button |
| `Entry` | Single-line text input |
| `Text` | Multi-line text area |
| `Frame` | Container / grouping box |
| `LabelFrame` | Frame with a title border |
| `Checkbutton` | Toggle checkbox |
| `Radiobutton` | Mutually exclusive option |
| `Scale` | Slider / range selector |
| `Listbox` | Scrollable list of items |
| `BrowseEntry` | Entry with dropdown list |
| `Scrollbar` | Scroll another widget |
| `Canvas` | Drawing surface |
| `Menu` | Menubar / popup menu |
| `Toplevel` | Additional window |
| `NoteBook` | Tabbed panels |

### Label
```perl
my $lbl = $parent->Label(
    -text       => "Username:",
    -font       => "Helvetica 12",
    -foreground => "#333333",
    -width      => 15,
    -anchor     => "e",        # Right-align text
)->pack(-side => "left");
```

### Button
```perl
my $btn = $parent->Button(
    -text    => "Click Me",
    -command => \&my_callback,   # Ref to subroutine
    -width   => 10,
    -relief  => "raised",        # raised, flat, groove, sunken, ridge
)->pack;

# Inline callback
my $btn2 = $parent->Button(
    -text    => "Quit",
    -command => sub { exit },
)->pack;
```

### Entry (Single-Line Input)
```perl
my $username = "";   # Tied variable
my $entry = $parent->Entry(
    -textvariable => \$username,
    -width        => 25,
    -font         => "Courier 12",
    -relief       => "sunken",
)->pack;

# Get value
my $val = $entry->get;

# Set value
$entry->delete(0, "end");
$entry->insert(0, "new text");

# Show password field
$parent->Entry(-show => "*", -textvariable => \$password)->pack;
```

### Text (Multi-Line)
```perl
my $text = $parent->Text(
    -width  => 60,
    -height => 20,
    -font   => "Courier 12",
    -wrap   => "word",    # none, char, word
)->pack;

$text->insert("end", "Hello\n");         # Append
my $content = $text->get("1.0", "end");  # Get all (row.col format)
$text->delete("1.0", "end");             # Clear all

# Tags for styled text
$text->tagConfigure("bold",  -font       => "Courier 12 bold");
$text->tagConfigure("red",   -foreground => "red");
$text->insert("end", "Bold text", "bold");
$text->insert("end", "Red text",  "red");
```

### Checkbutton
```perl
my $checked = 0;
$parent->Checkbutton(
    -text     => "Enable feature",
    -variable => \$checked,
    -command  => sub { print "State: $checked\n" },
)->pack;
```

### Radiobutton
```perl
my $choice = "opt1";
foreach my $opt (qw(opt1 opt2 opt3)) {
    $parent->Radiobutton(
        -text     => $opt,
        -value    => $opt,
        -variable => \$choice,
    )->pack(-anchor => "w");
}
```

### Scale (Slider)
```perl
my $volume = 50;
$parent->Scale(
    -label    => "Volume",
    -from     => 0,
    -to       => 100,
    -orient   => "horizontal",   # or "vertical"
    -variable => \$volume,
    -length   => 200,
    -tickinterval => 25,
    -command  => sub { print "Vol: $volume\n" },
)->pack;
```

### Listbox
```perl
my $lb = $parent->Listbox(
    -height       => 8,
    -width        => 30,
    -selectmode   => "single",   # single, browse, multiple, extended
    -font         => "Helvetica 11",
)->pack;

$lb->insert("end", "Item One", "Item Two", "Item Three");
my @selected = $lb->curselection;    # Returns indices
my $item     = $lb->get($selected[0]);
$lb->delete($selected[0]);
```

### Scrollbar (Linked to Listbox or Text)
```perl
my $frame = $parent->Frame->pack;
my $lb = $frame->Listbox(-height => 10)->pack(-side => "left");
my $sb = $frame->Scrollbar(-command => [$lb, "yview"])->pack(
    -side => "right", -fill => "y"
);
$lb->configure(-yscrollcommand => [$sb, "set"]);
```

### Frame and LabelFrame
```perl
# Frame — invisible container
my $fr = $parent->Frame(
    -relief      => "groove",
    -borderwidth => 2,
)->pack(-fill => "x", -padx => 5, -pady => 5);

# LabelFrame — bordered box with title
my $lf = $parent->LabelFrame(
    -text        => "Options",
    -font        => "Helvetica 11 bold",
)->pack(-fill => "both", -padx => 10, -pady => 5);

$lf->Checkbutton(-text => "Option A")->pack(-anchor => "w");
$lf->Checkbutton(-text => "Option B")->pack(-anchor => "w");
```

---

## 24. Layout Managers: pack, grid, place

Tk has three geometry managers. **Never mix them in the same container.**

### pack — Flow Layout
`pack` arranges widgets in a box, flowing in one direction.

```perl
$widget->pack(
    -side   => "top",    # top (default), bottom, left, right
    -fill   => "x",      # x, y, both, none — fill available space
    -expand => 1,        # 1 = grow to fill extra space
    -anchor => "w",      # n, ne, e, se, s, sw, w, nw, center
    -padx   => 5,        # Horizontal outer padding
    -pady   => 3,        # Vertical outer padding
    -ipadx  => 2,        # Horizontal inner padding
    -ipady  => 2,        # Vertical inner padding
);
```

**Common pack patterns:**
```perl
# Horizontal row of buttons
$btn1->pack(-side => "left");
$btn2->pack(-side => "left");

# Full-width label at top
$label->pack(-side => "top", -fill => "x");

# Text area that expands to fill window
$text->pack(-expand => 1, -fill => "both");

# Right-align a button
$btn->pack(-side => "right", -anchor => "e");
```

### grid — Table Layout
`grid` places widgets in rows and columns — best for forms.

```perl
$widget->grid(
    -row        => 0,
    -column     => 1,
    -rowspan    => 1,     # Span multiple rows
    -columnspan => 2,     # Span multiple columns
    -sticky     => "nsew", # n, s, e, w — stick to edges
    -padx       => 5,
    -pady       => 3,
);

# Make columns resize proportionally
$parent->gridColumnconfigure(1, -weight => 1);
$parent->gridRowconfigure(2, -weight => 1);
```

**Form layout example:**
```perl
my @fields = (["Name:", \$name], ["Email:", \$email], ["Phone:", \$phone]);
for my $i (0 .. $#fields) {
    my ($label, $var) = @{ $fields[$i] };
    $parent->Label(-text => $label)->grid(-row => $i, -column => 0, -sticky => "e");
    $parent->Entry(-textvariable => $var)->grid(-row => $i, -column => 1, -sticky => "ew");
}
```

### place — Absolute Positioning
`place` positions widgets at exact pixel coordinates.

```perl
$widget->place(-x => 100, -y => 50, -width => 120, -height => 30);
# or relative (0.0 to 1.0):
$widget->place(-relx => 0.5, -rely => 0.5, -anchor => "center");
```

> **Tip:** `grid` is best for forms. `pack` is best for toolbars and stacked layouts. `place` is best for custom drawing-board UIs.

---

## 25. Events, Bindings & Callbacks

### The `-command` Option
Most interactive widgets have a `-command` option:
```perl
$button->configure(-command => \&on_click);
$button->configure(-command => sub { print "clicked\n" });
```

### `bind` — Keyboard and Mouse Events
```perl
$widget->bind("<Button-1>",   \&on_left_click);    # Left mouse button
$widget->bind("<Button-3>",   \&on_right_click);   # Right click
$widget->bind("<Double-1>",   \&on_double_click);  # Double-click
$widget->bind("<Return>",     \&on_enter_key);     # Enter key
$widget->bind("<Escape>",     sub { exit });
$widget->bind("<KeyPress>",   \&on_any_key);
$widget->bind("<Motion>",     \&on_mouse_move);    # Mouse movement
$widget->bind("<Enter>",      \&on_mouse_enter);   # Cursor enters widget
$widget->bind("<Leave>",      \&on_mouse_leave);   # Cursor leaves widget
$widget->bind("<Configure>",  \&on_resize);        # Widget resized
```

### Accessing Event Data
```perl
$canvas->bind("<Button-1>", sub {
    my ($widget, $x, $y) = @_;
    print "Clicked at $x, $y\n";
});

# Alternative — event object
$widget->bind("<KeyPress>", sub {
    my $event = $widget->XEvent;
    print "Key: ", $event->K, "\n";   # Key symbol
});
```

### Modifier Keys
```perl
$widget->bind("<Control-s>",       \&save);
$widget->bind("<Control-z>",       \&undo);
$widget->bind("<Control-q>",       sub { exit });
$widget->bind("<Shift-Return>",    \&submit);
$widget->bind("<Control-a>",       sub { $entry->selectAll });
```

> **FreeBSD/X11 Note:** On FreeBSD under Xorg/Lima, use `<Control-key>` for standard
> application shortcuts. The `<Meta-key>` binding maps to the Alt key on most keyboards —
> useful for less common shortcuts but `<Control-*>` is the Unix convention.

### `after` — Timers
```perl
# Run once after 2000ms
$mw->after(2000, sub { print "2 seconds passed\n" });

# Repeating timer
my $timer_id;
sub start_timer {
    $timer_id = $mw->after(1000, \&tick);
}
sub tick {
    update_display();
    $timer_id = $mw->after(1000, \&tick);   # Re-schedule
}
sub stop_timer {
    $mw->afterCancel($timer_id) if $timer_id;
}
```

### `update` and `update idletasks`
```perl
# Force Tk to process pending events (e.g., update display during long ops)
$mw->update;
$mw->idletasks;   # Process only idle (drawing) tasks
```

---

## 26. Menus & Dialogs

### Menubar
```perl
my $menu = $mw->Menu;
$mw->configure(-menu => $menu);

# File menu
my $file = $menu->cascade(-label => "File", -underline => 0, -tearoff => 0);
$file->command(-label => "New",   -accelerator => "Cmd+N", -command => \&new_file);
$file->command(-label => "Open…", -accelerator => "Cmd+O", -command => \&open_file);
$file->command(-label => "Save",  -accelerator => "Cmd+S", -command => \&save_file);
$file->separator;
$file->command(-label => "Quit",  -accelerator => "Cmd+Q", -command => sub { exit });

# Edit menu
my $edit = $menu->cascade(-label => "Edit", -tearoff => 0);
$edit->command(-label => "Cut",   -command => \&cut);
$edit->command(-label => "Copy",  -command => \&copy);
$edit->command(-label => "Paste", -command => \&paste);

# Checkbutton in menu
my $word_wrap = 0;
$edit->checkbutton(-label => "Word Wrap", -variable => \$word_wrap);

# Radio items
my $theme = "light";
my $view = $menu->cascade(-label => "View", -tearoff => 0);
$view->radiobutton(-label => "Light", -variable => \$theme, -value => "light");
$view->radiobutton(-label => "Dark",  -variable => \$theme, -value => "dark");
```

### Context (Right-Click) Menu
```perl
my $ctx = $mw->Menu(-tearoff => 0);
$ctx->command(-label => "Copy",   -command => \&copy);
$ctx->command(-label => "Paste",  -command => \&paste);
$ctx->command(-label => "Delete", -command => \&delete_sel);

$text_widget->bind("<Button-3>", sub {
    my $e = $text_widget->XEvent;
    $ctx->popup($e->X, $e->Y);
});
```

### Built-in Dialog Boxes
```perl
use Tk::Dialog;

# Message box
my $answer = $mw->messageBox(
    -title   => "Confirm",
    -message => "Are you sure?",
    -type    => "YesNo",        # YesNo, OKCancel, AbortRetryIgnore
    -icon    => "question",     # question, warning, error, info
);
if ($answer eq "Yes") { ... }

# Error dialog
$mw->messageBox(
    -title   => "Error",
    -message => "File not found: $filename",
    -type    => "OK",
    -icon    => "error",
);
```

### File Open/Save Dialogs
```perl
# Open dialog
my $file = $mw->getOpenFile(
    -title      => "Open File",
    -initialdir => $ENV{HOME},
    -filetypes  => [
        ["Text Files", ".txt"],
        ["Perl Files", ".pl"],
        ["All Files",  "*"],
    ],
);

# Save dialog
my $file = $mw->getSaveFile(
    -title       => "Save As",
    -initialfile => "untitled.txt",
    -filetypes   => [["Text Files", ".txt"], ["All Files", "*"]],
);

# Directory chooser
my $dir = $mw->chooseDirectory(-title => "Choose Folder");
```

### Color Chooser
```perl
my $color = $mw->chooseColor(
    -title       => "Pick a Color",
    -initialcolor => "#ff0000",
);
```

### Custom Dialog with Toplevel
```perl
sub show_dialog {
    my ($parent, $title) = @_;
    my $dlg = $parent->Toplevel;
    $dlg->title($title);
    $dlg->transient($parent);        # Keep above parent
    $dlg->grab;                       # Modal — block parent

    $dlg->Label(-text => "Enter value:")->pack(-pady => 10);
    my $val = "";
    $dlg->Entry(-textvariable => \$val)->pack;
    $dlg->Button(
        -text    => "OK",
        -command => sub { $dlg->destroy },
    )->pack(-pady => 5);

    $dlg->waitWindow;   # Block until dialog closes
    return $val;
}
```

---

## 27. The Canvas Widget

The Canvas is a free-form drawing surface for graphics, charts, and custom UIs.

### Creating and Drawing
```perl
my $canvas = $mw->Canvas(
    -width      => 600,
    -height     => 400,
    -background => "white",
)->pack(-fill => "both", -expand => 1);

# Lines
my $line_id = $canvas->createLine(
    10, 10, 200, 100,
    -fill  => "blue",
    -width => 2,
    -arrow => "last",    # none, first, last, both
);

# Rectangle
$canvas->createRectangle(
    50, 50, 200, 150,
    -fill    => "lightblue",
    -outline => "navy",
    -width   => 2,
);

# Oval / Circle
$canvas->createOval(
    250, 50, 400, 200,
    -fill    => "yellow",
    -outline => "orange",
    -width   => 3,
);

# Text
$canvas->createText(
    300, 250,
    -text   => "Hello Canvas!",
    -font   => "Helvetica 16 bold",
    -fill   => "darkgreen",
    -anchor => "center",
);

# Polygon
$canvas->createPolygon(
    100, 300,   200, 250,   300, 300,   250, 380,   150, 380,
    -fill    => "pink",
    -outline => "red",
    -smooth  => 1,   # Curved edges
);

# Image (create a PhotoImage first)
my $img = $mw->Photo(-file => "logo.png");
$canvas->createImage(400, 200, -image => $img, -anchor => "center");
```

### Moving and Modifying Items
```perl
$canvas->move($item_id, $dx, $dy);           # Move by delta
$canvas->coords($item_id, @new_coords);      # Set absolute coords
$canvas->itemconfigure($item_id, -fill => "red");  # Reconfigure
$canvas->delete($item_id);                   # Remove item
$canvas->delete("all");                      # Clear canvas
my @ids = $canvas->find("all");             # Get all item IDs
```

### Canvas Tags
```perl
# Tag items for group operations
$canvas->createOval(... -tags => ["ball", "moving"]);
$canvas->move("moving", 5, 0);         # Move all "moving" items
$canvas->itemconfigure("ball", -fill => "red");  # Recolor group
```

### Canvas Mouse Interaction
```perl
$canvas->bind("all", "<Button-1>", sub {
    my $id = $canvas->find("withtag", "current");
    print "Clicked item: $id\n";
});

$canvas->bind("<Motion>", sub {
    my $e = $canvas->XEvent;
    print "Mouse at: ", $e->x, ",", $e->y, "\n";
});
```

### Scrollable Canvas
```perl
my $frame = $mw->Frame->pack(-fill => "both", -expand => 1);
my $cv = $frame->Canvas(-scrollregion => [0, 0, 2000, 2000])->pack(
    -side => "left", -fill => "both", -expand => 1
);
my $yscroll = $frame->Scrollbar(-command => [$cv, "yview"])->pack(
    -side => "right", -fill => "y"
);
$cv->configure(-yscrollcommand => [$yscroll, "set"]);
```

---

## 28. Building a Complete Application

A well-structured Perl/Tk application follows this layout:

```perl
#!/usr/bin/env perl
use strict;
use warnings;
use Tk;
use Tk::Text;

# ── State variables ──────────────────────────────────────────────
my $current_file = undef;
my $modified     = 0;
my $status_msg   = "Ready";

# ── Main window ──────────────────────────────────────────────────
my $mw = MainWindow->new;
$mw->title("My App");
$mw->geometry("800x600");
$mw->protocol("WM_DELETE_WINDOW", \&on_quit);  # Intercept close

# ── Build UI ─────────────────────────────────────────────────────
build_menu($mw);
build_toolbar($mw);
build_body($mw);
build_status($mw);

# ── Keyboard shortcuts ───────────────────────────────────────────
$mw->bind("<Control-n>",  \&new_file);
$mw->bind("<Control-o>",  \&open_file);
$mw->bind("<Control-s>",  \&save_file);
$mw->bind("<Control-q>",  \&on_quit);

# ── Start event loop ─────────────────────────────────────────────
MainLoop;

# ── Subroutines ──────────────────────────────────────────────────
sub new_file  { ... }
sub open_file { ... }
sub save_file { ... }
sub on_quit   {
    if ($modified) {
        my $ans = $mw->messageBox(
            -type => "YesNoCancel", -icon => "question",
            -message => "Save before quitting?"
        );
        return if $ans eq "Cancel";
        save_file() if $ans eq "Yes";
    }
    exit;
}
```

### Application Architecture Tips

1. **Separate state from UI** — Keep data in plain variables/hashes, not mixed into widget callbacks.
2. **Use `-textvariable`** to bind display to data — updates automatically.
3. **One `MainLoop` per program** — Never nest or call it twice.
4. **Avoid `sleep` in callbacks** — Use `after` timers instead.
5. **Long operations** — Run with `after(0, sub {...})` so the UI stays responsive, or fork a child process.
6. **`WM_DELETE_WINDOW`** — Always intercept the close button for unsaved-data prompts.

---

## 29. FreeBSD-Specific Tips & Best Practices

### Keyboard Shortcuts — Control Key
On FreeBSD under Xorg, Unix convention uses `Control` for application shortcuts:
```perl
$mw->bind("<Control-n>", \&new_file);    # Ctrl+N
$mw->bind("<Control-o>", \&open_file);   # Ctrl+O
$mw->bind("<Control-s>", \&save_file);   # Ctrl+S
$mw->bind("<Control-z>", \&undo);        # Ctrl+Z
$mw->bind("<Control-q>", sub { exit });  # Ctrl+Q
$mw->bind("<Control-w>", sub { $mw->destroy }); # Ctrl+W

# Meta (Alt key on most keyboards) for secondary bindings
$mw->bind("<Meta-F4>",   sub { exit });  # Alt+F4 (window manager)
```

### Shebang on FreeBSD
```perl
#!/usr/local/bin/perl      # Absolute path for ports Perl
#!/usr/bin/env perl        # Portable — searches PATH (preferred)
```

### Fonts Available on FreeBSD via Xorg
```perl
# Core X11 fonts — always available with xorg-fonts:
-font => "Helvetica 13"
-font => "Helvetica 11 bold"
-font => "Courier 12"

# DejaVu fonts (install with: pkg install dejavu)
-font => "DejaVu Sans 13"
-font => "DejaVu Sans Mono 12"

# Liberation fonts (install with: pkg install liberation-fonts-ttf)
-font => "Liberation Mono 12"

# List all available fonts:
# xlsfonts | grep helvetica
# fc-list    (if fontconfig is installed)
```

### Colors — Works Identically to Any X11 System
```perl
-background => "#f5f5f5"    # Light gray
-foreground => "#1a1a1a"    # Near-black text
-background => "#005faf"    # FreeBSD-themed blue
-background => "#00af5f"    # Green
-background => "#d70000"    # Red
```

### Installing More Perl Modules
```perl
# Via pkg (fastest — pre-built binaries)
pkg install p5-LWP-UserAgent
pkg install p5-DBI
pkg install p5-JSON

# Via cpanm (builds from source — for modules not in ports)
cpanm Some::Module

# Via ports (maximum control)
cd /usr/ports/www/p5-LWP-UserAgent && make install clean
```

### Running GUI Scripts over Lima X11
```bash
# Always verify DISPLAY is set before running GUI programs:
echo $DISPLAY          # Must be non-empty

# Run your Perl/Tk script:
perl perl_gui_01_basics.pl

# If DISPLAY is missing inside the shell:
export DISPLAY=:0
# or query Lima's SSH config for the forwarded port:
limactl show-ssh freebsd16 --format '{{.Config.SSH}}'
```

### Making a Script Executable on FreeBSD
```bash
chmod +x myscript.pl
./myscript.pl

# Or add to PATH and run by name:
cp myscript.pl /usr/local/bin/myscript
myscript
```

### Desktop Integration (XFCE / KDE on FreeBSD)
```bash
# Create a .desktop file for a Perl/Tk app:
cat > ~/.local/share/applications/perlpad.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=PerlPad
Exec=/usr/local/bin/perl /home/user/perl_gui_04_app.pl
Icon=text-editor
Terminal=false
Categories=Utility;TextEditor;
EOF
```

### Debugging on FreeBSD
```bash
perl -w myscript.pl 2>&1    # Warnings to terminal
perl -d myscript.pl          # Interactive debugger
DISPLAY=:0 perl myscript.pl  # Force X11 display

---

## Quick Reference — Tk Geometry

```
PACK:  -side top/bottom/left/right  -fill x/y/both  -expand 0/1
GRID:  -row N  -column N  -sticky nsew  -columnspan N
PLACE: -x N  -y N  -relx 0.0-1.0  -rely 0.0-1.0

COMMON OPTIONS:
  -text   -textvariable  -font    -foreground  -background
  -width  -height        -relief  -borderwidth -cursor
  -state  normal/disabled/active  -anchor n/ne/e/se/s/sw/w/nw/center
  -padx   -pady          -ipadx   -ipady

EVENTS:
  <Button-1>   <Button-3>   <Double-1>   <Return>   <Escape>
  <KeyPress>   <Motion>     <Enter>      <Leave>    <Configure>
  <Control-x>  <Alt-x>      <Shift-x>   <Meta-x>
```

---

*See the companion files `perl_tutorial.pl` (core language) and `perl_gui_01_basics.pl` through `perl_gui_04_app.pl` for runnable examples.*
