#!/usr/bin/env ruby
# =============================================================================
#  RUBY ADVENTURE — A Comprehensive Beginner's Program
#  Run with:  ruby ruby_adventure.rb
#
#  This single file walks through nearly every core Ruby concept:
#    Variables & Types · Strings · Arrays · Hashes · Symbols
#    Control Flow · Loops · Methods · Blocks & Iterators
#    Classes & Inheritance · Modules/Mixins · Exception Handling
#    File I/O · Ranges · Procs & Lambdas · Comparable
# =============================================================================

puts "=" * 60
puts "  RUBY ADVENTURE — Learning Ruby One Concept at a Time"
puts "=" * 60
puts


# =============================================================================
# SECTION 1 — VARIABLES, DATA TYPES & TRUTHINESS
# =============================================================================
puts "── SECTION 1: Variables & Data Types ──────────────────────"

# Ruby is dynamically typed — no type declarations needed.
# Variables are created the moment you assign them.

integer_val  = 42
float_val    = 3.14159
string_val   = "Hello, Ruby!"
boolean_true = true
boolean_false= false
nil_val      = nil            # nil is Ruby's "nothing" — it IS an object
symbol_val   = :my_symbol     # Symbols: immutable, memory-efficient identifiers

puts "Integer  : #{integer_val}  (class: #{integer_val.class})"
puts "Float    : #{float_val}  (class: #{float_val.class})"
puts "String   : #{string_val}  (class: #{string_val.class})"
puts "Boolean  : #{boolean_true} / #{boolean_false}"
puts "Nil      : #{nil_val.inspect}  (class: #{nil_val.class})"
puts "Symbol   : #{symbol_val}  (class: #{symbol_val.class})"
puts

# ── IMPORTANT: Ruby's Truthiness Rule ───────────────────────────────────────
# ONLY false and nil are falsy. 0, "", [] — all TRUTHY! Different from Python/JS.
puts "Truthiness check:"
[0, "", [], false, nil, "hello"].each do |val|
  puts "  #{val.inspect.ljust(10)} is #{val ? 'TRUTHY' : 'FALSY'}"
end
puts


# =============================================================================
# SECTION 2 — STRINGS IN DEPTH
# =============================================================================
puts "── SECTION 2: Strings ──────────────────────────────────────"

name  = "Ruby"
year  = 1995

# String interpolation: only works in double-quoted strings
puts "#{name} was created in #{year}."           # interpolation
puts '#{name} — single quotes are LITERAL'       # no interpolation
puts "Math inside interpolation: #{2 ** 10}"      # => 1024

# Common string methods
sentence = "  the quick brown fox  "
puts sentence.strip                 # remove leading/trailing whitespace
puts sentence.strip.capitalize      # capitalize first letter
puts sentence.strip.upcase          # ALL CAPS
puts sentence.strip.split(" ").inspect   # split into array
puts "hello".center(20, "-")        # ------- hello -------
puts "ha" * 5                       # hahahahaha
puts "Ruby".chars.inspect           # ["R","u","b","y"]
puts "hello world".gsub("o", "0")  # replace all occurrences
puts "hello world".include?("fox") # => false

# Multiline string (heredoc)
poem = <<~HEREDOC
  Roses are red,
  Violets are blue,
  Ruby is awesome,
  And so are you.
HEREDOC
puts poem

# String formatting
printf "%-15s %5d\n", "Count:", 42          # left-align, right-align
puts "Pi is approximately %.4f" % Math::PI  # 4 decimal places


# =============================================================================
# SECTION 3 — NUMBERS & MATH
# =============================================================================
puts "── SECTION 3: Numbers & Math ───────────────────────────────"

puts 10 / 3           # => 3   (INTEGER division — watch out!)
puts 10.0 / 3         # => 3.333...  (Float division)
puts 10 % 3           # => 1   (modulo / remainder)
puts 2 ** 8           # => 256 (exponent)
puts -7.abs           # => 7
puts 3.7.ceil         # => 4
puts 3.7.floor        # => 3
puts 3.567.round(2)   # => 3.57

# Useful numeric methods
puts 1_000_000        # underscores for readability (one million)
puts 255.to_s(16)     # => "ff"  (convert to hex string)
puts 0xFF             # => 255   (hex literal)
puts 42.between?(1, 100)  # => true

# Random numbers
puts rand(10)         # random 0..9
puts rand(1.0..2.0).round(3)  # random float in range
puts [*1..10].sample  # random element from range-array
puts


# =============================================================================
# SECTION 4 — SYMBOLS
# =============================================================================
puts "── SECTION 4: Symbols ──────────────────────────────────────"

# Symbols are immutable, interned identifiers.
# The same symbol always refers to the SAME object in memory.
a = :status
b = :status
puts "Same object? #{a.object_id == b.object_id}"  # => true

# Common uses: hash keys, method names, state flags
status = :active
puts status           # active
puts status.to_s      # "active"
puts "active".to_sym  # :active
puts :hello.upcase    # :HELLO — symbols have string-like methods too
puts


# =============================================================================
# SECTION 5 — ARRAYS
# =============================================================================
puts "── SECTION 5: Arrays ───────────────────────────────────────"

fruits = ["apple", "banana", "cherry", "date", "elderberry"]

# Accessing elements
puts fruits[0]           # first
puts fruits[-1]          # last (negative index from end)
puts fruits[1, 3].inspect  # start at index 1, take 3 items
puts fruits[0..2].inspect  # range slice

# Modifying
fruits.push("fig")       # add to end
fruits << "grape"        # << is the append operator (same as push)
fruits.unshift("avocado")# add to front
popped = fruits.pop      # remove & return last
shifted = fruits.shift   # remove & return first
puts "Removed from end: #{popped}, from front: #{shifted}"
puts fruits.inspect

# Querying
puts fruits.length       # count of elements
puts fruits.include?("banana")  # true/false
puts fruits.first(2).inspect    # first 2 elements
puts fruits.last(2).inspect     # last 2 elements

# Transformation (returns a NEW array — non-destructive)
puts fruits.map { |f| f.upcase }.inspect          # transform each element
puts fruits.select { |f| f.length > 5 }.inspect   # keep elements matching condition
puts fruits.reject { |f| f.include?("a") }.inspect # keep elements NOT matching
puts fruits.sort.inspect                           # alphabetical
puts fruits.sort_by { |f| f.length }.inspect      # sort by string length

# Aggregating
nums = [4, 8, 15, 16, 23, 42]
puts nums.sum                               # => 108
puts nums.min                               # => 4
puts nums.max                               # => 42
puts nums.reduce(:+)                        # sum via reduce
puts nums.reduce(1, :*)                     # product
puts nums.count { |n| n.even? }            # count evens
puts nums.any? { |n| n > 40 }             # => true
puts nums.all? { |n| n > 0 }              # => true
puts nums.none? { |n| n > 100 }           # => true

# Flatten and compact
nested  = [1, [2, 3], [4, [5, 6]]]
puts nested.flatten.inspect               # [1, 2, 3, 4, 5, 6]
with_nils = [1, nil, 2, nil, 3]
puts with_nils.compact.inspect            # [1, 2, 3]  (nils removed)

# Zip and combination
puts [1, 2, 3].zip([4, 5, 6]).inspect    # [[1,4],[2,5],[3,6]]
puts [1, 2, 3].product([0, 1]).inspect   # all combinations
puts


# =============================================================================
# SECTION 6 — HASHES
# =============================================================================
puts "── SECTION 6: Hashes ───────────────────────────────────────"

# A hash is a dictionary of key => value pairs.
# Modern style uses symbol keys:
person = {
  name: "Alice",
  age: 30,
  city: "Atlanta",
  hobbies: ["reading", "hiking", "ruby"]
}

# Accessing
puts person[:name]                      # => "Alice"
puts person[:missing]                   # => nil (no error)
puts person.fetch(:age)                 # => 30
puts person.fetch(:missing, "unknown")  # => "unknown" (safe default)

# Modifying
person[:email] = "alice@example.com"   # add new key
person[:age]   = 31                    # update existing key
person.delete(:city)                   # remove a key
puts person.inspect

# Iterating
puts "\nAll key-value pairs:"
person.each { |key, val| puts "  #{key}: #{val}" }

# Useful methods
puts "\nKeys:   #{person.keys.inspect}"
puts "Values: #{person.values.inspect}"
puts "Has :name? #{person.key?(:name)}"
puts "Has 31?    #{person.value?(31)}"

# Merge two hashes (second hash wins on conflicts)
defaults = { role: "user", active: true, score: 0 }
settings = { score: 100, theme: "dark" }
merged = defaults.merge(settings)
puts "\nMerged: #{merged.inspect}"

# Transform with map, select on hashes
scores = { alice: 95, bob: 72, carol: 88, dave: 55 }
passing = scores.select { |_, score| score >= 70 }
puts "Passing: #{passing.inspect}"

doubled = scores.transform_values { |v| v * 2 }
puts "Doubled: #{doubled.inspect}"
puts


# =============================================================================
# SECTION 7 — CONTROL FLOW
# =============================================================================
puts "── SECTION 7: Control Flow ─────────────────────────────────"

temperature = 72

# Standard if/elsif/else
if temperature > 90
  puts "Hot day!"
elsif temperature > 70
  puts "Nice day — #{temperature}°F"
else
  puts "Cool day"
end

# unless = "if not" — reads naturally for negative conditions
unless temperature < 60
  puts "No jacket needed"
end

# Postfix (one-liner) — very idiomatic Ruby
puts "Perfect temperature!" if temperature.between?(68, 76)
puts "Bring a coat!"       unless temperature > 60

# Ternary operator
label = temperature > 80 ? "Warm" : "Comfortable"
puts "It's: #{label}"

# case/when — Ruby's switch statement
# Uses === internally, so ranges and regex work too
grade_score = 87

grade = case grade_score
  when 90..100 then "A"
  when 80..89  then "B"
  when 70..79  then "C"
  when 60..69  then "D"
  else              "F"
end
puts "\nScore #{grade_score} => Grade #{grade}"

# case with no argument (acts like if/elsif)
x = 42
case
when x < 0   then puts "Negative"
when x == 0  then puts "Zero"
when x < 100 then puts "#{x} is a smallish positive number"
else               puts "Large"
end
puts


# =============================================================================
# SECTION 8 — LOOPS & ITERATION
# =============================================================================
puts "── SECTION 8: Loops & Iteration ────────────────────────────"

# times — simplest counted loop
print "times:   "
5.times { |i| print "#{i} " }
puts

# upto / downto
print "upto:    "
1.upto(5) { |i| print "#{i} " }
puts

print "downto:  "
5.downto(1) { |i| print "#{i} " }
puts

# step — like range(start, stop, step) in Python
print "step:    "
(0..20).step(5) { |n| print "#{n} " }
puts

# while
print "while:   "
i = 1
while i <= 5
  print "#{i} "
  i += 1
end
puts

# until = "while not"
print "until:   "
i = 5
until i == 0
  print "#{i} "
  i -= 1
end
puts

# loop with break — explicit infinite loop
print "loop:    "
count = 0
loop do
  print "#{count} "
  count += 1
  break if count >= 5
end
puts

# each — the most common Ruby loop (works on any Enumerable)
print "each:    "
[10, 20, 30, 40, 50].each { |n| print "#{n} " }
puts

# each_with_index — when you need the index too
puts "\nWith index:"
["alpha", "beta", "gamma"].each_with_index do |word, idx|
  puts "  [#{idx}] #{word}"
end

# next and break
print "\nnext/break: "
(1..10).each do |n|
  next if n.even?    # skip even numbers
  break if n > 7     # stop at 7
  print "#{n} "
end
puts
puts


# =============================================================================
# SECTION 9 — METHODS
# =============================================================================
puts "── SECTION 9: Methods ──────────────────────────────────────"

# Basic method — last expression is automatically returned
def square(n)
  n ** 2
end
puts "square(7) = #{square(7)}"

# Default parameters
def greet(name, greeting = "Hello", punctuation = "!")
  "#{greeting}, #{name}#{punctuation}"
end
puts greet("Alice")
puts greet("Bob", "Hi")
puts greet("Carol", "Hey", "?")

# Keyword arguments (named, order-independent, self-documenting)
def create_profile(name:, age:, city: "Unknown", active: true)
  "#{name}, #{age}, #{city} [active: #{active}]"
end
puts create_profile(name: "Dave", age: 28, city: "Denver")
puts create_profile(age: 22, name: "Eve")   # order doesn't matter

# Splat — variable number of positional arguments (*args → Array)
def sum_all(*numbers)
  numbers.reduce(0, :+)
end
puts "sum_all(1,2,3,4,5) = #{sum_all(1, 2, 3, 4, 5)}"

# Double splat — variable keyword arguments (**kwargs → Hash)
def log_event(event, **metadata)
  puts "EVENT: #{event}"
  metadata.each { |k, v| puts "  #{k}: #{v}" }
end
log_event("login", user: "alice", ip: "192.168.1.1", success: true)

# Predicate methods (? suffix — convention: returns boolean)
def palindrome?(str)
  str == str.reverse
end
puts "\npalindrome?('racecar') = #{palindrome?('racecar')}"
puts "palindrome?('hello')   = #{palindrome?('hello')}"

# Bang methods (! suffix — convention: mutates or raises)
words = ["banana", "apple", "cherry"]
words.sort!           # sorts in-place (mutates original)
puts "\nAfter sort!: #{words.inspect}"

# Multiple return values (via array)
def min_max(arr)
  [arr.min, arr.max]   # returns array, caller unpacks it
end
low, high = min_max([4, 1, 9, 2, 7])
puts "min=#{low}, max=#{high}"
puts


# =============================================================================
# SECTION 10 — BLOCKS, PROCS & LAMBDAS
# =============================================================================
puts "── SECTION 10: Blocks, Procs & Lambdas ─────────────────────"

# A block is an anonymous chunk of code passed to a method.
# { } for single-line, do..end for multi-line.

# yield — calls the block from inside a method
def measure(label)
  start = Time.now
  result = yield              # execute the block, capture return value
  elapsed = Time.now - start
  puts "#{label}: #{result.inspect} (took #{elapsed.round(6)}s)"
end

measure("square of 1000") { 1000 ** 2 }
measure("sort array")     { (1..20).to_a.shuffle.sort }

# block_given? — check if a block was passed
def optional_block(x)
  if block_given?
    yield(x)
  else
    x * 2          # default behavior
  end
end
puts "\noptional_block(5)          = #{optional_block(5)}"
puts "optional_block(5) { |n| n+100 } = #{optional_block(5) { |n| n + 100 }}"

# Proc — a saved, reusable block object
double = Proc.new { |n| n * 2 }
triple = proc { |n| n * 3 }         # shorthand
puts "\nProc: double.call(7) = #{double.call(7)}"
puts "Proc: triple.(4)     = #{triple.(4)}"    # .() is shorthand for .call()
puts "Proc: double[9]      = #{double[9]}"     # [] also calls

# Lambda — like a Proc but:
#   1. Strict argument checking
#   2. return exits the lambda, not the enclosing method
square_it = lambda { |n| n ** 2 }
add_one   = ->(n) { n + 1 }         # stabby lambda (preferred modern style)
puts "\nLambda: square_it.call(6) = #{square_it.call(6)}"
puts "Lambda: add_one.(9)        = #{add_one.(9)}"

# & operator — convert symbol to a block (VERY idiomatic Ruby)
words_mixed = ["hello", "WORLD", "Ruby"]
puts "\n& symbol-to-proc:"
puts words_mixed.map(&:downcase).inspect   # equivalent to .map { |w| w.downcase }
puts words_mixed.map(&:length).inspect
puts [1, nil, 2, nil, 3].select(&:itself).inspect  # remove nils

# Chaining iterators — functional pipeline
result = (1..20)
  .select(&:odd?)                   # keep odd numbers
  .map { |n| n ** 2 }              # square them
  .reject { |n| n > 100 }          # remove those over 100
  .reduce(:+)                       # sum them all
puts "\nChained pipeline result: #{result}"
puts


# =============================================================================
# SECTION 11 — RANGES
# =============================================================================
puts "── SECTION 11: Ranges ──────────────────────────────────────"

inclusive = (1..10)     # 1 to 10 (includes 10)
exclusive = (1...10)    # 1 to 9  (excludes 10)
letters   = ('a'..'f')  # works on strings too!

puts inclusive.to_a.inspect
puts exclusive.to_a.inspect
puts letters.to_a.inspect

puts inclusive.include?(10)  # => true
puts exclusive.include?(10)  # => false
puts inclusive.min           # => 1
puts inclusive.max           # => 10
puts inclusive.sum           # => 55

# Ranges as case conditions (uses ===)
puts "\nAge groups:"
[5, 13, 25, 67].each do |age|
  category = case age
    when 0..12   then "Child"
    when 13..17  then "Teenager"
    when 18..64  then "Adult"
    else              "Senior"
  end
  puts "  #{age} => #{category}"
end
puts


# =============================================================================
# SECTION 12 — CLASSES & OBJECT-ORIENTED PROGRAMMING
# =============================================================================
puts "── SECTION 12: Classes & OOP ───────────────────────────────"

class BankAccount
  # Class-level constant — shared, never changes
  INTEREST_RATE = 0.035

  # attr_accessor creates both getter and setter methods
  # attr_reader  = getter only (read-only)
  # attr_writer  = setter only (write-only)
  attr_reader   :owner, :account_number
  attr_accessor :balance

  # Class variable — shared across ALL instances
  @@total_accounts = 0

  # Constructor
  def initialize(owner, initial_balance = 0)
    @owner          = owner
    @balance        = initial_balance.to_f
    @@total_accounts += 1
    @account_number  = "ACC-%04d" % @@total_accounts
    @transactions   = []      # private data, no accessor
  end

  # Instance methods
  def deposit(amount)
    raise ArgumentError, "Deposit must be positive" unless amount > 0
    @balance += amount
    @transactions << { type: :deposit, amount: amount }
    puts "  Deposited $#{"%.2f" % amount} → Balance: $#{"%.2f" % @balance}"
  end

  def withdraw(amount)
    raise ArgumentError, "Withdrawal must be positive"  unless amount > 0
    raise "Insufficient funds (balance: $#{"%.2f" % @balance})" if amount > @balance
    @balance -= amount
    @transactions << { type: :withdrawal, amount: amount }
    puts "  Withdrew  $#{"%.2f" % amount} → Balance: $#{"%.2f" % @balance}"
  end

  def apply_interest
    interest = @balance * INTEREST_RATE
    deposit(interest)
    puts "  (interest applied at #{INTEREST_RATE * 100}%)"
  end

  def transaction_history
    @transactions.map.with_index(1) do |t, i|
      "  #{i}. #{t[:type].to_s.capitalize.ljust(12)} $#{"%.2f" % t[:amount]}"
    end.join("\n")
  end

  # Predicate method
  def overdrawn?
    @balance < 0
  end

  # Class method (called on BankAccount, not an instance)
  def self.total_accounts
    @@total_accounts
  end

  # to_s — called automatically when object is printed
  def to_s
    "#{@account_number} [#{@owner}] Balance: $#{"%.2f" % @balance}"
  end
end

puts "Creating accounts..."
alice_acc = BankAccount.new("Alice", 1000)
bob_acc   = BankAccount.new("Bob",   500)
puts "Total accounts: #{BankAccount.total_accounts}"
puts

puts "Alice's account: #{alice_acc}"
alice_acc.deposit(250)
alice_acc.deposit(500)
alice_acc.withdraw(150)
alice_acc.apply_interest
puts "\nAlice transaction history:\n#{alice_acc.transaction_history}"
puts

# Exception handling in action
puts "Testing error handling:"
begin
  alice_acc.withdraw(999_999)
rescue RuntimeError => e
  puts "  ✗ Error: #{e.message}"
end
begin
  alice_acc.deposit(-50)
rescue ArgumentError => e
  puts "  ✗ Error: #{e.message}"
end
puts


# =============================================================================
# SECTION 13 — INHERITANCE
# =============================================================================
puts "── SECTION 13: Inheritance ─────────────────────────────────"

class Animal
  attr_accessor :name, :age

  def initialize(name, age)
    @name = name
    @age  = age
  end

  def speak
    "..."                  # base implementation — to be overridden
  end

  def describe
    "#{@name} (#{@age} yrs) says: #{speak}"
  end

  def to_s
    "#{self.class.name}(#{@name})"
  end
end

class Dog < Animal
  attr_accessor :breed

  def initialize(name, age, breed)
    super(name, age)       # calls Animal's initialize
    @breed = breed
  end

  def speak = "Woof! Woof!"   # one-line method (Ruby 3+)
  def fetch(item) = "#{@name} fetches the #{item}!"

  def to_s
    "#{super} — #{@breed}"  # super calls parent's to_s
  end
end

class Cat < Animal
  def initialize(name, age, indoor: true)
    super(name, age)
    @indoor = indoor
  end

  def speak = "Meow~"
  def indoor? = @indoor
end

class Parrot < Animal
  def initialize(name, age, phrase)
    super(name, age)
    @phrase = phrase
  end

  def speak = "#{@phrase}! Squawk!"
end

animals = [
  Dog.new("Rex", 3, "Labrador"),
  Cat.new("Whiskers", 5, indoor: true),
  Parrot.new("Polly", 7, "Pretty bird"),
  Dog.new("Buddy", 2, "Poodle"),
  Cat.new("Shadow", 4, indoor: false)
]

animals.each { |a| puts "  #{a.describe}" }
puts

# Polymorphism — same method, different behavior
puts "All speak: #{animals.map(&:speak).inspect}"
puts "Only dogs: #{animals.select { |a| a.is_a?(Dog) }.map(&:to_s).inspect}"
puts "is_a?:     Rex is_a? Animal = #{animals[0].is_a?(Animal)}"
puts "class:     #{animals[0].class}"
puts


# =============================================================================
# SECTION 14 — MODULES & MIXINS
# =============================================================================
puts "── SECTION 14: Modules & Mixins ────────────────────────────"

# Modules as mixins: share behavior across unrelated classes
# without using inheritance (which Ruby limits to one parent)

module Describable
  def full_description
    vars = instance_variables.map do |var|
      "#{var}=#{instance_variable_get(var).inspect}"
    end
    "#{self.class.name}(#{vars.join(', ')})"
  end
end

module Serializable
  def to_csv
    instance_variables.map { |v| instance_variable_get(v) }.join(",")
  end

  def serialize
    { class: self.class.name }.tap do |h|
      instance_variables.each { |v| h[v.to_s.delete("@").to_sym] = instance_variable_get(v) }
    end
  end
end

module Taggable
  def tag_list
    @tags ||= []          # ||= : assign only if nil/false
  end

  def add_tag(tag)
    tag_list << tag.to_sym unless tag_list.include?(tag.to_sym)
  end

  def tagged_with?(tag)
    tag_list.include?(tag.to_sym)
  end
end

class Product
  include Describable     # adds instance methods from module
  include Serializable
  include Taggable

  attr_accessor :name, :price, :category

  def initialize(name, price, category)
    @name     = name
    @price    = price
    @category = category
  end
end

laptop = Product.new("ThinkPad X1", 1299.99, :electronics)
laptop.add_tag("portable")
laptop.add_tag("business")
laptop.add_tag("tech")

puts laptop.full_description
puts "CSV:    #{laptop.to_csv}"
puts "Tags:   #{laptop.tag_list.inspect}"
puts "Tech?   #{laptop.tagged_with?(:tech)}"
puts "Gaming? #{laptop.tagged_with?(:gaming)}"
puts "Hash:   #{laptop.serialize.inspect}"
puts


# =============================================================================
# SECTION 15 — COMPARABLE MIXIN (sort, <, >, ==)
# =============================================================================
puts "── SECTION 15: Comparable ──────────────────────────────────"

class Student
  include Comparable     # gives: <, >, <=, >=, ==, between?, clamp, .sort

  attr_accessor :name, :gpa

  def initialize(name, gpa)
    @name = name
    @gpa  = gpa
  end

  # Define <=> and Comparable does the rest for FREE
  def <=>(other)
    @gpa <=> other.gpa
  end

  def to_s = "#{@name}(#{@gpa})"
end

students = [
  Student.new("Alice", 3.9),
  Student.new("Bob",   3.1),
  Student.new("Carol", 3.7),
  Student.new("Dave",  2.8),
  Student.new("Eve",   3.5)
]

puts "Sorted by GPA:  #{students.sort.map(&:to_s).inspect}"
puts "Top student:    #{students.max}"
puts "Lowest GPA:     #{students.min}"
puts "GPA honor roll: #{students.select { |s| s.gpa >= 3.5 }.map(&:name).inspect}"
puts "Alice > Bob?    #{students[0] > students[1]}"
puts


# =============================================================================
# SECTION 16 — EXCEPTION HANDLING
# =============================================================================
puts "── SECTION 16: Exception Handling ──────────────────────────"

# Custom exception class
class InsufficientFundsError < StandardError
  def initialize(needed, available)
    super("Need $#{needed}, but only $#{available} available")
    @needed    = needed
    @available = available
  end
end

# Full begin/rescue/else/ensure/retry structure
def safe_divide(a, b)
  begin
    result = a / b
  rescue ZeroDivisionError => e
    puts "  ✗ ZeroDivision: #{e.message}"
    result = nil
  rescue TypeError => e
    puts "  ✗ TypeError: #{e.message}"
    result = nil
  else
    puts "  ✓ #{a} / #{b} = #{result}"   # only runs if NO exception
  ensure
    puts "  (ensure always runs)"         # always runs, like finally
  end
  result
end

puts "Division tests:"
safe_divide(10, 2)
safe_divide(10, 0)
safe_divide(10, "2") rescue nil
puts

# retry — reattempt the block (useful for transient failures)
attempts = 0
begin
  attempts += 1
  raise "Simulated flaky error" if attempts < 3
  puts "Succeeded after #{attempts} attempt(s)"
rescue RuntimeError => e
  puts "  Attempt #{attempts} failed: #{e.message}. Retrying..."
  retry if attempts < 3
  puts "  Gave up after #{attempts} attempts"
end

# raise with custom exception
def transfer(amount, from_balance)
  raise ArgumentError,         "Amount must be positive"       if amount <= 0
  raise InsufficientFundsError.new(amount, from_balance)       if amount > from_balance
  from_balance - amount
end

puts "\nTransfer tests:"
[[-50, 500], [200, 100], [100, 500]].each do |amount, balance|
  begin
    new_balance = transfer(amount, balance)
    puts "  ✓ Transferred $#{amount}. New balance: $#{new_balance}"
  rescue ArgumentError, InsufficientFundsError => e
    puts "  ✗ #{e.class}: #{e.message}"
  end
end
puts


# =============================================================================
# SECTION 17 — FILE I/O
# =============================================================================
puts "── SECTION 17: File I/O ────────────────────────────────────"

filename = "ruby_adventure_output.txt"

# Writing to a file
File.open(filename, "w") do |f|
  f.puts "Ruby Adventure Output File"
  f.puts "Generated at: #{Time.now}"
  f.puts "-" * 40
  students.sort.reverse.each_with_index do |s, i|
    f.puts "#{i+1}. #{s.name.ljust(10)} GPA: #{s.gpa}"
  end
end
puts "Wrote: #{filename}"

# Appending to a file
File.open(filename, "a") do |f|
  f.puts "\nProduct catalog:"
  f.puts laptop.to_csv
end

# Reading entire file at once
content = File.read(filename)
puts "File contents:"
puts content

# Reading line by line (memory-efficient for large files)
line_count = 0
File.foreach(filename) { |_| line_count += 1 }
puts "Total lines: #{line_count}"

# File metadata
puts "File size: #{File.size(filename)} bytes"
puts "Exists?    #{File.exist?(filename)}"

# Clean up
File.delete(filename)
puts "Deleted #{filename}"
puts


# =============================================================================
# SECTION 18 — PUTTING IT ALL TOGETHER: Mini Text RPG
# =============================================================================
puts "── SECTION 18: Mini Text RPG Demo ──────────────────────────"
puts "(Runs automatically — no user input needed for the demo)\n\n"

module Combatant
  def alive?   = @hp > 0
  def dead?    = !alive?
  def hp_bar
    filled = (@hp.to_f / @max_hp * 20).round
    "[" + "█" * filled + "░" * (20 - filled) + "] #{@hp}/#{@max_hp}"
  end
end

class Hero
  include Combatant
  attr_reader :name, :hp, :level, :gold, :inventory

  LEVEL_XP = [0, 100, 250, 450, 700]  # XP needed per level

  def initialize(name)
    @name      = name
    @level     = 1
    @hp        = @max_hp = 30
    @attack    = 8
    @xp        = 0
    @gold      = 10
    @inventory = []
  end

  def attack_roll
    base   = rand(@attack..@attack * 2)
    bonus  = @inventory.include?(:sword) ? 5 : 0
    base + bonus
  end

  def take_damage(dmg)
    @hp = [@hp - dmg, 0].max   # clamp to 0
  end

  def heal(amount)
    @hp = [@hp + amount, @max_hp].min  # clamp to max_hp
  end

  def gain_xp(xp)
    @xp += xp
    threshold = LEVEL_XP[@level] || 999
    if @xp >= threshold && @level < 4
      @level += 1
      @max_hp += 10
      @hp      = @max_hp
      @attack += 3
      puts "  ⬆  #{@name} reached Level #{@level}! HP ↑ ATK ↑"
    end
  end

  def to_s
    "#{@name} Lv#{@level} #{hp_bar} ATK:#{@attack} GOLD:#{@gold}g"
  end
end

class Monster
  include Combatant
  attr_reader :name, :xp_reward, :gold_reward

  TYPES = {
    slime:   { hp: 8,  atk: 2..4,  xp: 30,  gold: 2..5  },
    goblin:  { hp: 15, atk: 3..7,  xp: 60,  gold: 5..10 },
    orc:     { hp: 25, atk: 5..10, xp: 120, gold: 8..15 },
    dragon:  { hp: 50, atk: 8..18, xp: 300, gold: 20..40 }
  }

  def self.random(min_type = :slime)
    types  = TYPES.keys
    idx    = [types.index(min_type) || 0, types.length - 1]
    chosen = types[rand(idx[0]..idx[1])]
    new(chosen)
  end

  def initialize(type)
    data       = TYPES[type]
    @name      = type.to_s.capitalize
    @hp        = @max_hp = data[:hp]
    @atk_range = data[:atk]
    @xp_reward = data[:xp]
    @gold_reward = rand(data[:gold])
  end

  def attack_roll = rand(@atk_range)

  def to_s = "#{@name} #{hp_bar}"
end

# --- battle method (uses blocks, symbols, ranges, classes, modules) ---
def battle(hero, monster)
  puts "  ⚔  #{hero.name} VS #{monster.name}!"
  round = 0
  while hero.alive? && monster.alive?
    round += 1
    # Hero attacks
    dmg_to_monster = hero.attack_roll
    monster.take_damage(dmg_to_monster)
    # Monster attacks back (if still alive)
    dmg_to_hero = monster.alive? ? monster.attack_roll : 0
    hero.take_damage(dmg_to_hero)

    puts "  Round #{round}: Hero hits #{dmg_to_monster} / #{monster.name} hits #{dmg_to_hero}"
    break unless monster.alive?
  end

  if hero.alive?
    hero.gain_xp(monster.xp_reward)
    puts "  ✓ #{hero.name} wins! +#{monster.xp_reward}XP +#{monster.gold_reward}G"
  else
    puts "  ✗ #{hero.name} was defeated..."
  end
  puts "  Hero: #{hero}"
  puts
  hero.alive?
end

# --- Run a short demo adventure ---
hero = Hero.new("Rubyist")
puts "#{hero.name} begins their adventure!"
puts hero
puts

encounter_types = [:slime, :slime, :goblin, :orc]
encounter_types.each do |type|
  monster = Monster.new(type)
  break unless battle(hero, monster)
  hero.heal(5)   # small heal between fights
  hero.instance_variable_set(:@gold, hero.gold + monster.gold_reward)
end

puts "Adventure complete! Final status:"
puts hero


# =============================================================================
# DONE
# =============================================================================
puts
puts "=" * 60
puts "  End of Ruby Adventure — #{RubyVM::YJIT.enabled? rescue false ? "YJIT ON" : "Ruby #{RUBY_VERSION}"}"
puts "  Concepts covered:"
[
  "Variables & Types", "Strings & Heredocs", "Numbers & Math",
  "Symbols", "Arrays (full API)", "Hashes (full API)",
  "Control Flow (if/case/unless)", "Loops (all forms)",
  "Methods (defaults/kwargs/splat)", "Blocks, Procs & Lambdas",
  "Symbol-to-proc (&:method)", "Ranges", "Classes & OOP",
  "Inheritance & super", "Modules & Mixins (include)",
  "Comparable mixin", "Exception Handling (retry/custom)",
  "File I/O", "Mini RPG (all concepts combined)"
].each_with_index { |c, i| puts "  #{(i+1).to_s.rjust(2)}. #{c}" }
puts "=" * 60
