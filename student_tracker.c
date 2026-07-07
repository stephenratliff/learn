/*
 * ============================================================
 *  C LANGUAGE TOUR — Student Grade Tracker
 *  A single program that demonstrates the core features of C:
 *
 *   1.  #includes & preprocessor macros
 *   2.  enum  — named integer constants
 *   3.  struct — custom data types
 *   4.  Functions & prototypes
 *   5.  Arrays (fixed-size)
 *   6.  Pointers & the -> operator
 *   7.  Strings (<string.h>)
 *   8.  Control flow  (if/else, switch, for, while, do-while)
 *   9.  Dynamic memory (malloc / realloc / free)
 *  10.  File I/O (fopen / fprintf / fscanf / fclose)
 *  11.  scanf / printf format specifiers
 *  12.  Operators (arithmetic, comparison, logical, ternary)
 *
 *  Compile:  gcc -Wall -Wextra -std=c11 -o tracker student_tracker.c
 *  Run:      ./tracker
 * ============================================================
 */

/* ── 1. PREPROCESSOR DIRECTIVES ─────────────────────────────
 *  #include pulls in standard library headers.
 *  #define creates a compile-time constant (no semicolon!).
 *  The preprocessor does pure text substitution before the
 *  compiler ever sees your code.
 */
#include <stdio.h>    /* printf, scanf, fopen, fclose, FILE   */
#include <stdlib.h>   /* malloc, realloc, free, exit          */
#include <string.h>   /* strcpy, strcmp, strlen, strncpy      */
#include <ctype.h>    /* toupper — convert char to uppercase  */

#define MAX_NAME      64     /* max characters in a student name   */
#define SAVE_FILE     "students.dat"   /* name of the save file    */
#define PASSING_SCORE 60.0   /* scores below this are failing      */

/* ── 2. ENUM — Named Integer Constants ──────────────────────
 *  An enum assigns readable names to integers.
 *  By default: ADD=0, VIEW=1, SEARCH=2, ...
 *  Use enums instead of bare magic numbers — far more readable.
 */
typedef enum {
    ADD    = 1,   /* we start at 1 so the menu numbers match */
    VIEW   = 2,
    SEARCH = 3,
    SAVE   = 4,
    LOAD   = 5,
    STATS  = 6,
    QUIT   = 7
} MenuChoice;

/* ── 3. STRUCT — Custom Composite Data Type ─────────────────
 *  A struct groups related fields into one named type.
 *  'typedef struct { ... } TypeName;' lets us write
 *  'Student s;' instead of 'struct Student s;' everywhere.
 */
typedef struct {
    char   name[MAX_NAME];  /* fixed-size char array = C string */
    int    id;              /* student ID number                */
    double score;           /* exam score 0.0 – 100.0          */
    char   grade;           /* letter grade: A B C D F         */
} Student;

/* ── 4. FUNCTION PROTOTYPES ──────────────────────────────────
 *  In C, a function must be declared (or defined) before it
 *  is called.  Prototypes at the top tell the compiler the
 *  function signature; the full definition can come later.
 */
char   calculateGrade(double score);
void   printStudent(const Student *s);          /* const ptr: we promise not to modify *s */
void   addStudent(Student **roster, int *count, int *capacity);
void   viewAll(const Student *roster, int count);
void   searchByName(const Student *roster, int count);
void   showStats(const Student *roster, int count);
void   saveToFile(const Student *roster, int count);
void   loadFromFile(Student **roster, int *count, int *capacity);
void   printMenu(void);
void   clearInputBuffer(void);

/* ═══════════════════════════════════════════════════════════
 *  MAIN — Program Entry Point
 *  int main(void) returns an int to the OS:
 *    0 = success,  non-zero = error code
 * ═══════════════════════════════════════════════════════════
 */
int main(void) {

    /* ── 9. DYNAMIC MEMORY ────────────────────────────────
     *  We don't know how many students there will be at
     *  compile time, so we allocate on the heap with malloc.
     *
     *  malloc(n * sizeof(T)) returns void* — a raw pointer
     *  to n*sizeof(T) bytes of uninitialized memory, or NULL
     *  if allocation fails.  We cast it to Student*.
     *
     *  'capacity' is how much space we've reserved;
     *  'count' is how many slots are actually used.
     */
    int      capacity = 4;   /* start small to demo realloc */
    int      count    = 0;
    Student *roster   = malloc(capacity * sizeof(Student));

    if (roster == NULL) {   /* ALWAYS check malloc's return value */
        fprintf(stderr, "Fatal: could not allocate memory.\n");
        return 1;           /* return non-zero = failure */
    }

    printf("╔══════════════════════════════════════╗\n");
    printf("║    C Language Tour: Grade Tracker    ║\n");
    printf("╚══════════════════════════════════════╝\n\n");

    /* ── 8. CONTROL FLOW: do-while loop ──────────────────
     *  do { ... } while (condition);
     *  Runs the body AT LEAST once before checking the
     *  condition.  Perfect for menu loops where you always
     *  want to show the menu at least one time.
     */
    int running = 1;   /* flag variable — 1=true, 0=false */
    do {
        printMenu();

        /* ── 11. scanf — Read Formatted Input ────────────
         *  %d reads one integer.
         *  & gives scanf the ADDRESS of 'choice' so it can
         *  write the value there.  (Remember: C is pass-by-
         *  value; without &, scanf gets a copy, not the var.)
         */
        int choice;
        if (scanf("%d", &choice) != 1) {  /* scanf returns number of items read */
            clearInputBuffer();
            printf("  Invalid input. Enter a number.\n\n");
            continue;   /* jump back to top of loop */
        }
        clearInputBuffer();  /* discard trailing newline */

        /* ── 8. CONTROL FLOW: switch ─────────────────────
         *  switch(expr) jumps directly to the matching case.
         *  'break' exits the switch; without it, execution
         *  FALLS THROUGH to the next case (usually a bug!).
         *  'default' runs when no case matches.
         */
        switch (choice) {
            case ADD:    addStudent(&roster, &count, &capacity); break;
            case VIEW:   viewAll(roster, count);                 break;
            case SEARCH: searchByName(roster, count);            break;
            case SAVE:   saveToFile(roster, count);              break;
            case LOAD:   loadFromFile(&roster, &count, &capacity); break;
            case STATS:  showStats(roster, count);               break;
            case QUIT:
                printf("  Goodbye!\n\n");
                running = 0;   /* set flag to exit do-while */
                break;
            default:
                printf("  Unknown option. Try 1-%d.\n\n", QUIT);
        }

    } while (running);  /* loop continues while running == 1 */

    /* ── FREE DYNAMIC MEMORY ────────────────────────────
     *  Every malloc must have exactly one matching free.
     *  After free, set pointer to NULL to prevent accidental
     *  use-after-free bugs.
     */
    free(roster);
    roster = NULL;

    return 0;  /* 0 = success */
}

/* ═══════════════════════════════════════════════════════════
 *  FUNCTION DEFINITIONS  (implementations below main)
 * ═══════════════════════════════════════════════════════════
 */

/* ── calculateGrade ──────────────────────────────────────────
 *  Demonstrates: if/else if/else chain, comparison operators,
 *  returning a char value.
 */
char calculateGrade(double score) {
    /* ── 12. OPERATORS ──────────────────────────────────
     *  >=  (greater-than-or-equal) is a comparison operator.
     *  &&  is logical AND — both conditions must be true.
     *  The chain stops at the first true branch.
     */
    if      (score >= 90.0)               return 'A';
    else if (score >= 80.0 && score < 90) return 'B';
    else if (score >= 70.0 && score < 80) return 'C';
    else if (score >= 60.0 && score < 70) return 'D';
    else                                  return 'F';
}

/* ── printStudent ────────────────────────────────────────────
 *  Demonstrates: pointer parameter, -> operator, ternary,
 *  printf format specifiers.
 *
 *  'const Student *s' means s is a pointer we CAN'T modify the
 *  pointed-to data through — safe read-only access.
 */
void printStudent(const Student *s) {
    /* ── 6. POINTER: -> operator ─────────────────────────
     *  s->name  is shorthand for  (*s).name
     *  (dereference the pointer, then access the field)
     */
    printf("  %-20s  ID: %04d  Score: %6.2f  Grade: %c  [%s]\n",
        s->name,
        s->id,
        s->score,
        s->grade,
        /* ── 12. TERNARY OPERATOR ─────────────────────────
         *  condition ? value_if_true : value_if_false
         *  Here: if score >= PASSING_SCORE print PASS else FAIL
         */
        s->score >= PASSING_SCORE ? "PASS" : "FAIL"
    );
}

/* ── addStudent ──────────────────────────────────────────────
 *  Demonstrates: pointer-to-pointer (**), realloc, strncpy,
 *  scanf with strings, input validation while loop.
 *
 *  We take Student **roster because we may need to resize the
 *  array (which changes the pointer itself).  A pointer-to-
 *  pointer lets us update the caller's pointer variable.
 */
void addStudent(Student **roster, int *count, int *capacity) {
    /* ── GROW THE ARRAY IF FULL ───────────────────────────
     *  realloc resizes an existing heap block.
     *  We double capacity each time — an O(1) amortized
     *  growth strategy (same as std::vector in C++).
     *
     *  IMPORTANT: assign to a temp pointer first.  If realloc
     *  fails it returns NULL but the original block is still
     *  valid.  Writing  roster = realloc(roster,...) would
     *  overwrite the only pointer to the old block → memory leak.
     */
    if (*count >= *capacity) {
        int       newCap    = *capacity * 2;
        Student  *newBlock  = realloc(*roster, newCap * sizeof(Student));
        if (newBlock == NULL) {
            printf("  Error: memory allocation failed.\n");
            return;
        }
        *roster   = newBlock;  /* update the caller's pointer */
        *capacity = newCap;
        printf("  (Array grown to capacity %d)\n", newCap);
    }

    /* Work directly with the next empty slot via a pointer */
    Student *s = &(*roster)[*count];

    /* Read name ─────────────────────────────────────────── */
    printf("\n  Enter student name: ");
    /* ── 7. STRINGS: fgets ────────────────────────────────
     *  fgets(buffer, size, stream) reads up to size-1 chars
     *  and always adds '\0'.  Safer than gets() (never use gets!).
     *  We read from stdin here.
     */
    if (fgets(s->name, MAX_NAME, stdin) == NULL) return;
    /* Strip trailing newline that fgets includes */
    s->name[strcspn(s->name, "\n")] = '\0';

    if (strlen(s->name) == 0) {
        printf("  Name cannot be empty.\n\n");
        return;
    }

    /* Auto-assign ID = count + 1001 */
    s->id = *count + 1001;

    /* Read score with input validation ───────────────────── */
    /* ── 8. CONTROL FLOW: while loop with validation ─────
     *  Keep asking until the user gives a valid number.
     */
    while (1) {   /* 'while(1)' = infinite loop; exit via break */
        printf("  Enter score (0 – 100): ");
        if (scanf("%lf", &s->score) == 1          /* %lf reads a double */
                && s->score >= 0.0
                && s->score <= 100.0) {
            clearInputBuffer();
            break;  /* valid input — exit the loop */
        }
        clearInputBuffer();
        printf("  Invalid. Please enter a number between 0 and 100.\n");
    }

    /* Calculate letter grade from score */
    s->grade = calculateGrade(s->score);

    (*count)++;   /* increment the count in the caller */

    printf("\n  Added: ");
    printStudent(s);
    printf("\n");
}

/* ── viewAll ─────────────────────────────────────────────────
 *  Demonstrates: for loop, array iteration via pointer,
 *  early-return guard clause.
 */
void viewAll(const Student *roster, int count) {
    /* Guard clause — return early if nothing to show */
    if (count == 0) {
        printf("\n  No students on record yet.\n\n");
        return;
    }

    printf("\n  %-20s  %-8s  %-10s  %-7s  %s\n",
           "Name", "ID", "Score", "Grade", "Result");
    printf("  %s\n", "─────────────────────────────────────────────────────");

    /* ── 8. CONTROL FLOW: for loop ───────────────────────
     *  Classic C for loop:
     *    init      → int i = 0
     *    condition → i < count  (checked before each iteration)
     *    update    → i++        (runs after each iteration body)
     */
    for (int i = 0; i < count; i++) {
        /* roster[i] accesses element i.
         * &roster[i] gives a pointer to that element,
         * which printStudent expects. */
        printStudent(&roster[i]);
    }
    printf("\n");
}

/* ── searchByName ────────────────────────────────────────────
 *  Demonstrates: string comparison (strcmp), boolean flag,
 *  for loop with early break.
 */
void searchByName(const Student *roster, int count) {
    if (count == 0) { printf("\n  No students on record.\n\n"); return; }

    char query[MAX_NAME];
    printf("\n  Enter name to search: ");
    if (fgets(query, MAX_NAME, stdin) == NULL) return;
    query[strcspn(query, "\n")] = '\0';  /* strip newline */

    int found = 0;  /* boolean flag — 0=false, 1=true */

    for (int i = 0; i < count; i++) {
        /* ── 7. STRINGS: strcmp ───────────────────────────
         *  strcmp(a, b) returns 0 if strings are equal,
         *  < 0 if a comes before b, > 0 if a comes after b.
         *  We CANNOT use == to compare C strings (that
         *  compares pointer addresses, not the contents!).
         */
        if (strcmp(roster[i].name, query) == 0) {
            if (!found) printf("\n  Search results:\n");
            printStudent(&roster[i]);
            found = 1;
        }
    }

    if (!found) printf("\n  No student named \"%s\" found.\n", query);
    printf("\n");
}

/* ── showStats ───────────────────────────────────────────────
 *  Demonstrates: running min/max/sum, integer division,
 *  modulo, printf field widths, casting.
 */
void showStats(const Student *roster, int count) {
    if (count == 0) { printf("\n  No students on record.\n\n"); return; }

    double sum  = 0.0;
    double high = roster[0].score;
    double low  = roster[0].score;
    int    pass = 0;
    int    fail = 0;

    /* ── 8. CONTROL FLOW: for loop with accumulation ─────*/
    for (int i = 0; i < count; i++) {
        sum += roster[i].score;   /* += accumulate */

        if (roster[i].score > high) high = roster[i].score;
        if (roster[i].score < low)  low  = roster[i].score;

        /* ── 12. TERNARY inside expression ───────────────*/
        (roster[i].score >= PASSING_SCORE) ? pass++ : fail++;
    }

    double avg = sum / count;   /* floating-point division */

    printf("\n  ┌─────────────────────────────┐\n");
    printf("  │         CLASS STATS         │\n");
    printf("  ├─────────────────────────────┤\n");
    printf("  │  Students  : %-4d           │\n", count);
    printf("  │  Average   : %-6.2f         │\n", avg);
    printf("  │  Highest   : %-6.2f         │\n", high);
    printf("  │  Lowest    : %-6.2f         │\n", low);
    printf("  │  Passing   : %-4d           │\n", pass);
    printf("  │  Failing   : %-4d           │\n", fail);
    /* ── 12. OPERATORS: cast & modulo ────────────────────
     *  (double)pass  casts int→double so division is
     *  floating-point, not integer (which would truncate).
     *  % is modulo (remainder): 7 % 3 == 1
     */
    printf("  │  Pass Rate : %5.1f%%         │\n",
           count > 0 ? (double)pass / count * 100.0 : 0.0);
    printf("  └─────────────────────────────┘\n\n");
}

/* ── saveToFile ──────────────────────────────────────────────
 *  Demonstrates: FILE*, fopen("w"), fprintf, fclose.
 */
void saveToFile(const Student *roster, int count) {
    /* ── 10. FILE I/O: opening a file for writing ────────
     *  fopen(path, mode) returns FILE* or NULL on error.
     *  Mode "w" creates the file (or overwrites if it exists).
     */
    FILE *fp = fopen(SAVE_FILE, "w");
    if (fp == NULL) {
        perror("  Error opening file");  /* perror prints the OS error message */
        return;
    }

    /* Write count on the first line so load knows how many to read */
    fprintf(fp, "%d\n", count);

    for (int i = 0; i < count; i++) {
        /* fprintf works just like printf but writes to fp */
        fprintf(fp, "%s\n%d\n%.2f\n%c\n",
                roster[i].name,
                roster[i].id,
                roster[i].score,
                roster[i].grade);
    }

    fclose(fp);   /* ALWAYS close — flushes buffer to disk */
    printf("\n  Saved %d student(s) to \"%s\".\n\n", count, SAVE_FILE);
}

/* ── loadFromFile ────────────────────────────────────────────
 *  Demonstrates: fopen("r"), fscanf, fgets for strings,
 *  realloc to fit the loaded count.
 */
void loadFromFile(Student **roster, int *count, int *capacity) {
    /* ── 10. FILE I/O: opening for reading ───────────────
     *  Mode "r" opens an existing file for reading.
     *  Returns NULL if the file doesn't exist.
     */
    FILE *fp = fopen(SAVE_FILE, "r");
    if (fp == NULL) {
        printf("\n  No save file found (\"%s\").\n\n", SAVE_FILE);
        return;
    }

    int newCount;
    if (fscanf(fp, "%d\n", &newCount) != 1) {
        printf("\n  Error reading save file.\n\n");
        fclose(fp);
        return;
    }

    /* Reallocate roster to exactly fit the loaded data */
    Student *newBlock = realloc(*roster, newCount * sizeof(Student));
    if (newBlock == NULL && newCount > 0) {
        printf("\n  Memory error during load.\n\n");
        fclose(fp);
        return;
    }
    *roster   = newBlock;
    *capacity = newCount;

    for (int i = 0; i < newCount; i++) {
        /* fgets reads the name line (includes '\n', then we strip it) */
        if (fgets((*roster)[i].name, MAX_NAME, fp) == NULL) break;
        (*roster)[i].name[strcspn((*roster)[i].name, "\n")] = '\0';

        /* fscanf reads the remaining fields */
        fscanf(fp, "%d\n",  &(*roster)[i].id);
        fscanf(fp, "%lf\n", &(*roster)[i].score);
        fscanf(fp, " %c\n", &(*roster)[i].grade);  /* space before %c skips whitespace */
    }

    fclose(fp);
    *count = newCount;
    printf("\n  Loaded %d student(s) from \"%s\".\n\n", newCount, SAVE_FILE);
}

/* ── printMenu ───────────────────────────────────────────────
 *  A simple display function — nothing new here, just
 *  showing that printf can draw structured UI.
 */
void printMenu(void) {
    printf("  ┌────────────────────────┐\n");
    printf("  │         MENU           │\n");
    printf("  ├────────────────────────┤\n");
    printf("  │  %d. Add student       │\n", ADD);
    printf("  │  %d. View all          │\n", VIEW);
    printf("  │  %d. Search by name    │\n", SEARCH);
    printf("  │  %d. Save to file      │\n", SAVE);
    printf("  │  %d. Load from file    │\n", LOAD);
    printf("  │  %d. Show statistics   │\n", STATS);
    printf("  │  %d. Quit              │\n", QUIT);
    printf("  └────────────────────────┘\n");
    printf("  Choice: ");
}

/* ── clearInputBuffer ────────────────────────────────────────
 *  After scanf reads a number it leaves '\n' in stdin's buffer.
 *  The next fgets would immediately read that '\n' and return "".
 *  This function discards everything up to and including '\n'.
 *
 *  getchar() reads one character; we loop until we hit '\n' or EOF.
 */
void clearInputBuffer(void) {
    int c;
    while ((c = getchar()) != '\n' && c != EOF)
        ;   /* empty body — the work is done in the condition */
}
