<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Computer Science Fundamentals</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600&family=Fraunces:ital,wght@0,300;0,600;0,800;1,300&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --ink: #0d0d0d;
    --page: #f5f2ea;
    --accent: #c84b2f;
    --accent2: #2a5f8f;
    --muted: #6b6560;
    --rule: #d4cfc6;
    --code-bg: #1a1a1a;
    --code-text: #e8e2d4;
    --highlight: #fff3cd;
    --green: #2d6a3f;
    --purple: #5c3d8f;
    --teal: #1a6b6b;
  }

  html { font-size: 16px; scroll-behavior: smooth; }

  body {
    background: var(--page);
    color: var(--ink);
    font-family: 'Fraunces', Georgia, serif;
    line-height: 1.7;
    font-weight: 300;
  }

  /* ── COVER ─────────────────────────────────── */
  .cover {
    min-height: 100vh;
    background: var(--ink);
    color: var(--page);
    display: grid;
    grid-template-rows: 1fr auto;
    padding: 4rem 3rem 2rem;
    position: relative;
    overflow: hidden;
  }

  .cover::before {
    content: '';
    position: absolute;
    top: -60px; right: -80px;
    width: 520px; height: 520px;
    border-radius: 50%;
    border: 1px solid rgba(245,242,234,0.08);
  }
  .cover::after {
    content: '';
    position: absolute;
    bottom: 80px; left: -120px;
    width: 380px; height: 380px;
    border-radius: 50%;
    border: 1px solid rgba(200,75,47,0.2);
  }

  .cover-number {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 3rem;
  }

  .cover-title {
    font-size: clamp(3.2rem, 8vw, 7rem);
    font-weight: 800;
    line-height: 0.92;
    letter-spacing: -0.02em;
    max-width: 900px;
    margin-bottom: 1.5rem;
  }

  .cover-title em {
    font-style: italic;
    font-weight: 300;
    color: rgba(245,242,234,0.5);
  }

  .cover-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: rgba(245,242,234,0.55);
    max-width: 480px;
    line-height: 1.6;
    margin-top: 2rem;
  }

  .cover-bottom {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-top: 1px solid rgba(245,242,234,0.12);
    padding-top: 1.5rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: rgba(245,242,234,0.35);
    letter-spacing: 0.06em;
  }

  .cover-toc {
    display: flex; gap: 2rem;
  }

  .toc-item {
    display: flex; flex-direction: column; gap: 2px;
  }
  .toc-item span:first-child {
    color: var(--accent);
  }

  /* ── LAYOUT ─────────────────────────────────── */
  .page {
    max-width: 860px;
    margin: 0 auto;
    padding: 4rem 2.5rem;
  }

  /* ── NAV ─────────────────────────────────────── */
  nav {
    position: sticky;
    top: 0;
    background: rgba(245,242,234,0.95);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid var(--rule);
    z-index: 100;
    padding: 0.75rem 2.5rem;
    display: flex;
    gap: 0.25rem;
    flex-wrap: wrap;
    align-items: center;
  }

  nav a {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    text-decoration: none;
    padding: 0.3rem 0.6rem;
    border-radius: 3px;
    letter-spacing: 0.04em;
    transition: all 0.15s;
  }
  nav a:hover { background: var(--ink); color: var(--page); }
  nav .nav-brand {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--accent);
    margin-right: 1rem;
  }

  /* ── SECTION ─────────────────────────────────── */
  .section {
    margin-bottom: 6rem;
    padding-top: 2rem;
  }

  .section-header {
    display: flex;
    align-items: flex-start;
    gap: 1.5rem;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 2px solid var(--ink);
  }

  .section-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--accent);
    letter-spacing: 0.1em;
    padding-top: 0.5rem;
    min-width: 2.5rem;
  }

  .section-title {
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.02em;
  }

  h3 {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 2rem 0 0.75rem;
    letter-spacing: -0.01em;
  }

  h4 {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    color: var(--accent2);
    text-transform: uppercase;
    margin: 1.5rem 0 0.5rem;
  }

  p { margin-bottom: 1rem; font-size: 1rem; }

  /* ── CODE ─────────────────────────────────────── */
  pre {
    background: var(--code-bg);
    color: var(--code-text);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.83rem;
    line-height: 1.6;
    padding: 1.5rem;
    border-radius: 4px;
    overflow-x: auto;
    margin: 1.25rem 0;
    border-left: 3px solid var(--accent);
  }

  code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88em;
    background: rgba(200,75,47,0.1);
    color: var(--accent);
    padding: 0.15em 0.35em;
    border-radius: 3px;
  }

  pre code { background: none; color: inherit; padding: 0; font-size: inherit; }

  .comment { color: #6b7280; }
  .kw { color: #c084fc; }
  .fn { color: #60a5fa; }
  .str { color: #86efac; }
  .num { color: #fbbf24; }
  .type { color: #f0abfc; }

  /* ── CARDS ─────────────────────────────────────── */
  .card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
  }

  .card {
    background: white;
    border: 1px solid var(--rule);
    border-radius: 4px;
    padding: 1.25rem;
    position: relative;
    overflow: hidden;
  }

  .card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
  }

  .card.red::before { background: var(--accent); }
  .card.blue::before { background: var(--accent2); }
  .card.green::before { background: var(--green); }
  .card.purple::before { background: var(--purple); }
  .card.teal::before { background: var(--teal); }

  .card-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.4rem;
  }

  .card h4 { margin: 0 0 0.5rem; font-size: 1rem; color: var(--ink); text-transform: none; letter-spacing: 0; font-family: 'Fraunces', serif; }
  .card p { font-size: 0.9rem; color: var(--muted); margin: 0; }

  /* ── COMPLEXITY TABLE ─────────────────────────── */
  .table-wrap { overflow-x: auto; margin: 1.5rem 0; }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
  }

  th {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    background: var(--ink);
    color: var(--page);
    padding: 0.75rem 1rem;
    text-align: left;
  }

  td {
    padding: 0.65rem 1rem;
    border-bottom: 1px solid var(--rule);
    vertical-align: middle;
  }

  tr:hover td { background: rgba(200,75,47,0.04); }

  .badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    padding: 0.2rem 0.55rem;
    border-radius: 2px;
    font-weight: 600;
  }

  .badge.fast { background: #dcfce7; color: #166534; }
  .badge.medium { background: #fef9c3; color: #854d0e; }
  .badge.slow { background: #fee2e2; color: #991b1b; }

  /* ── CALLOUT ─────────────────────────────────── */
  .callout {
    border: 1px solid var(--rule);
    border-left: 4px solid var(--accent2);
    background: white;
    padding: 1.25rem 1.5rem;
    margin: 1.5rem 0;
    border-radius: 0 4px 4px 0;
  }

  .callout-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--accent2);
    margin-bottom: 0.5rem;
    font-weight: 600;
  }

  .callout p { margin: 0; font-size: 0.92rem; }

  /* ── DIAGRAM ─────────────────────────────────── */
  .diagram {
    background: var(--ink);
    color: var(--code-text);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.8;
    padding: 2rem;
    border-radius: 4px;
    margin: 1.5rem 0;
    overflow-x: auto;
  }

  /* ── BIG QUOTE ─────────────────────────────────── */
  .pull-quote {
    font-size: 1.7rem;
    font-weight: 600;
    font-style: italic;
    line-height: 1.3;
    letter-spacing: -0.01em;
    border-top: 3px solid var(--ink);
    border-bottom: 3px solid var(--ink);
    padding: 1.5rem 0;
    margin: 2.5rem 0;
    color: var(--ink);
  }

  /* ── DIVIDER ─────────────────────────────────── */
  .divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 3rem 0;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
  }
  .divider::before, .divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--rule);
  }

  /* ── LIST ─────────────────────────────────────── */
  ul, ol {
    padding-left: 1.5rem;
    margin: 0.75rem 0 1rem;
  }
  li { margin-bottom: 0.4rem; font-size: 1rem; }
  li::marker { color: var(--accent); }

  /* ── ALGO STEPS ─────────────────────────────── */
  .steps {
    counter-reset: step;
    list-style: none;
    padding: 0;
    margin: 1rem 0;
  }
  .steps li {
    counter-increment: step;
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    margin-bottom: 0.75rem;
    font-size: 0.95rem;
  }
  .steps li::before {
    content: counter(step, decimal-leading-zero);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    color: white;
    background: var(--accent);
    min-width: 2rem;
    height: 1.6rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 2px;
    margin-top: 0.15rem;
    flex-shrink: 0;
  }

  /* ── FOOTER ─────────────────────────────────── */
  footer {
    background: var(--ink);
    color: rgba(245,242,234,0.4);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    text-align: center;
    padding: 2rem;
    letter-spacing: 0.06em;
  }

  @media (max-width: 640px) {
    .cover { padding: 2.5rem 1.5rem 1.5rem; }
    .page { padding: 2.5rem 1.25rem; }
    nav { padding: 0.6rem 1.25rem; }
    .section-title { font-size: 1.8rem; }
    .cover-title { font-size: 2.8rem; }
    .cover-toc { flex-wrap: wrap; gap: 1rem; }
  }

  @media print {
    nav { display: none; }
    .cover { page-break-after: always; }
    .section { page-break-inside: avoid; }
  }
</style>
</head>
<body>

<!-- ══════════ COVER ══════════ -->
<div class="cover">
  <div>
    <div class="cover-number">CS — 101 &nbsp;·&nbsp; Fundamentals Guide &nbsp;·&nbsp; 2025</div>
    <h1 class="cover-title">Computer<br><em>Science</em><br>Fundamentals</h1>
    <p class="cover-sub">A complete reference covering data structures, algorithms, systems, networking, and theory — designed for students and practitioners alike.</p>
  </div>
  <div class="cover-bottom">
    <span>10 Chapters &nbsp;·&nbsp; Core Concepts</span>
    <div class="cover-toc">
      <div class="toc-item"><span>01</span><span>Data Structures</span></div>
      <div class="toc-item"><span>02</span><span>Algorithms</span></div>
      <div class="toc-item"><span>03</span><span>Complexity</span></div>
      <div class="toc-item"><span>04</span><span>Systems</span></div>
      <div class="toc-item"><span>05</span><span>Networking</span></div>
    </div>
  </div>
</div>

<!-- ══════════ NAV ══════════ -->
<nav>
  <span class="nav-brand">CS·101</span>
  <a href="#data-structures">Data Structures</a>
  <a href="#algorithms">Algorithms</a>
  <a href="#complexity">Complexity</a>
  <a href="#systems">Systems</a>
  <a href="#networking">Networking</a>
  <a href="#os">OS</a>
  <a href="#databases">Databases</a>
  <a href="#oop">OOP</a>
  <a href="#logic">Logic</a>
  <a href="#security">Security</a>
</nav>

<!-- ══════════ CONTENT ══════════ -->
<main class="page">

  <!-- ── 01 DATA STRUCTURES ── -->
  <section class="section" id="data-structures">
    <div class="section-header">
      <span class="section-num">01</span>
      <h2 class="section-title">Data Structures</h2>
    </div>

    <p>A data structure is a way of organizing and storing data in memory so that it can be accessed and modified efficiently. Choosing the right structure is often the difference between an algorithm that runs in milliseconds and one that takes hours.</p>

    <h3>Arrays</h3>
    <p>The most fundamental structure: a contiguous block of memory holding elements of the same type, accessed by index in O(1) time.</p>

    <pre><code><span class="comment">// Array: O(1) access, O(n) insert at arbitrary position</span>
<span class="kw">int</span> arr[5] = {10, 20, 30, 40, 50};
arr[2];   <span class="comment">// → 30, direct index</span>

<span class="comment">// Dynamic Array (Python list / Java ArrayList)</span>
nums = [1, 2, 3]
nums.append(4)    <span class="comment">// O(1) amortized</span>
nums.insert(0, 0) <span class="comment">// O(n) — must shift</span></code></pre>

    <h3>Linked Lists</h3>
    <p>A chain of nodes, each holding a value and a pointer to the next node. Enables O(1) insertion at known positions, but O(n) search.</p>

    <pre><code><span class="comment">// Singly Linked List Node</span>
<span class="kw">class</span> <span class="type">Node</span>:
    <span class="kw">def</span> <span class="fn">__init__</span>(self, val):
        self.val  = val
        self.next = <span class="kw">None</span>

<span class="comment">// 1 → 2 → 3 → None</span>
head = <span class="type">Node</span>(1)
head.next = <span class="type">Node</span>(2)
head.next.next = <span class="type">Node</span>(3)</code></pre>

    <div class="card-grid">
      <div class="card red">
        <div class="card-label">Stack</div>
        <h4>Last-In, First-Out</h4>
        <p>Push and pop from the top. Used for function call stacks, undo systems, expression parsing.</p>
      </div>
      <div class="card blue">
        <div class="card-label">Queue</div>
        <h4>First-In, First-Out</h4>
        <p>Enqueue at back, dequeue at front. Used in BFS, job schedulers, print queues.</p>
      </div>
      <div class="card green">
        <div class="card-label">Deque</div>
        <h4>Double-Ended Queue</h4>
        <p>Insert and remove from both ends in O(1). Combines benefits of stack and queue.</p>
      </div>
    </div>

    <h3>Hash Tables</h3>
    <p>Maps keys to values using a hash function. Average O(1) for get/set. The backbone of dictionaries in Python, objects in JavaScript, and maps in Java.</p>

    <pre><code><span class="comment">// Hash function concept: key → index in array</span>
index = hash(key) % table_size

<span class="comment">// Collision resolution: chaining</span>
table[5] = [("apple", 1), ("grape", 3)]  <span class="comment">// both hash to 5</span>

<span class="comment">// Python dict is a hash table</span>
freq = {}
<span class="kw">for</span> word <span class="kw">in</span> words:
    freq[word] = freq.get(word, 0) + 1</code></pre>

    <h3>Trees</h3>
    <p>Hierarchical structures where each node has at most one parent and any number of children.</p>

    <div class="diagram">
Binary Search Tree (BST):
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[8]&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;← root
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
&nbsp;&nbsp;&nbsp;&nbsp;[3]&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[10]&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;← depth 1
&nbsp;&nbsp;&nbsp;/&nbsp;&nbsp;&nbsp;\&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
&nbsp;[1]&nbsp;&nbsp;&nbsp;[6]&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[14]&nbsp;&nbsp;&nbsp;← depth 2
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/&nbsp;&nbsp;&nbsp;\&nbsp;&nbsp;&nbsp;/
&nbsp;&nbsp;&nbsp;[4]&nbsp;[7]&nbsp;[13]&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;← depth 3

Rule: left child < parent < right child
Search: O(log n) average, O(n) worst (skewed)</div>

    <h3>Heaps &amp; Priority Queues</h3>
    <p>A complete binary tree satisfying the heap property: in a max-heap, every parent is ≥ its children. Enables O(1) peek at max/min and O(log n) insert/remove.</p>

    <h3>Graphs</h3>
    <p>A set of vertices (V) connected by edges (E). The most general data structure — almost any relationship can be modeled as a graph.</p>

    <div class="card-grid">
      <div class="card purple">
        <div class="card-label">Directed Graph</div>
        <h4>Edges have direction</h4>
        <p>A → B does not imply B → A. Models: web links, dependencies, social follows.</p>
      </div>
      <div class="card teal">
        <div class="card-label">Undirected Graph</div>
        <h4>Edges are bidirectional</h4>
        <p>If A–B exists, you can traverse both ways. Models: friendships, roads, networks.</p>
      </div>
      <div class="card red">
        <div class="card-label">Weighted Graph</div>
        <h4>Edges carry a cost</h4>
        <p>Used for shortest path, minimum spanning tree, and network flow problems.</p>
      </div>
    </div>

    <pre><code><span class="comment">// Adjacency list representation</span>
graph = {
    <span class="str">'A'</span>: [<span class="str">'B'</span>, <span class="str">'C'</span>],
    <span class="str">'B'</span>: [<span class="str">'D'</span>],
    <span class="str">'C'</span>: [<span class="str">'D'</span>, <span class="str">'E'</span>],
    <span class="str">'D'</span>: [],
    <span class="str">'E'</span>: []
}</code></pre>
  </section>

  <div class="divider">§</div>

  <!-- ── 02 ALGORITHMS ── -->
  <section class="section" id="algorithms">
    <div class="section-header">
      <span class="section-num">02</span>
      <h2 class="section-title">Algorithms</h2>
    </div>

    <p>An algorithm is a finite, deterministic sequence of well-defined instructions that solves a class of problems. Good algorithm design is the foundation of efficient software.</p>

    <h3>Sorting Algorithms</h3>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Algorithm</th>
            <th>Best</th>
            <th>Average</th>
            <th>Worst</th>
            <th>Space</th>
            <th>Stable?</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Bubble Sort</td><td><span class="badge fast">O(n)</span></td><td><span class="badge slow">O(n²)</span></td><td><span class="badge slow">O(n²)</span></td><td>O(1)</td><td>✓</td></tr>
          <tr><td>Selection Sort</td><td><span class="badge slow">O(n²)</span></td><td><span class="badge slow">O(n²)</span></td><td><span class="badge slow">O(n²)</span></td><td>O(1)</td><td>✗</td></tr>
          <tr><td>Insertion Sort</td><td><span class="badge fast">O(n)</span></td><td><span class="badge slow">O(n²)</span></td><td><span class="badge slow">O(n²)</span></td><td>O(1)</td><td>✓</td></tr>
          <tr><td>Merge Sort</td><td><span class="badge medium">O(n log n)</span></td><td><span class="badge medium">O(n log n)</span></td><td><span class="badge medium">O(n log n)</span></td><td>O(n)</td><td>✓</td></tr>
          <tr><td>Quick Sort</td><td><span class="badge medium">O(n log n)</span></td><td><span class="badge medium">O(n log n)</span></td><td><span class="badge slow">O(n²)</span></td><td>O(log n)</td><td>✗</td></tr>
          <tr><td>Heap Sort</td><td><span class="badge medium">O(n log n)</span></td><td><span class="badge medium">O(n log n)</span></td><td><span class="badge medium">O(n log n)</span></td><td>O(1)</td><td>✗</td></tr>
          <tr><td>Counting Sort</td><td><span class="badge fast">O(n+k)</span></td><td><span class="badge fast">O(n+k)</span></td><td><span class="badge fast">O(n+k)</span></td><td>O(k)</td><td>✓</td></tr>
        </tbody>
      </table>
    </div>

    <pre><code><span class="comment"># Merge Sort — divide and conquer</span>
<span class="kw">def</span> <span class="fn">merge_sort</span>(arr):
    <span class="kw">if</span> len(arr) <= 1:
        <span class="kw">return</span> arr
    mid = len(arr) // 2
    left  = <span class="fn">merge_sort</span>(arr[:mid])
    right = <span class="fn">merge_sort</span>(arr[mid:])
    <span class="kw">return</span> <span class="fn">merge</span>(left, right)

<span class="kw">def</span> <span class="fn">merge</span>(L, R):
    result, i, j = [], 0, 0
    <span class="kw">while</span> i < len(L) <span class="kw">and</span> j < len(R):
        <span class="kw">if</span> L[i] <= R[j]: result.append(L[i]); i += 1
        <span class="kw">else</span>:             result.append(R[j]); j += 1
    <span class="kw">return</span> result + L[i:] + R[j:]</code></pre>

    <h3>Searching Algorithms</h3>

    <div class="card-grid">
      <div class="card red">
        <div class="card-label">Linear Search</div>
        <h4>O(n)</h4>
        <p>Check each element. Works on unsorted data. Simple but slow for large inputs.</p>
      </div>
      <div class="card blue">
        <div class="card-label">Binary Search</div>
        <h4>O(log n)</h4>
        <p>Halve the search space each step. Requires sorted data. Extremely fast in practice.</p>
      </div>
    </div>

    <pre><code><span class="comment"># Binary Search (iterative)</span>
<span class="kw">def</span> <span class="fn">binary_search</span>(arr, target):
    lo, hi = 0, len(arr) - 1
    <span class="kw">while</span> lo <= hi:
        mid = (lo + hi) // 2
        <span class="kw">if</span>   arr[mid] == target: <span class="kw">return</span> mid
        <span class="kw">elif</span> arr[mid] <  target: lo = mid + 1
        <span class="kw">else</span>:                    hi = mid - 1
    <span class="kw">return</span> -1</code></pre>

    <h3>Graph Traversal</h3>

    <h4>BFS — Breadth-First Search</h4>
    <p>Explore all neighbors at the current depth before moving deeper. Uses a queue. Finds shortest paths in unweighted graphs.</p>

    <pre><code><span class="kw">from</span> collections <span class="kw">import</span> deque

<span class="kw">def</span> <span class="fn">bfs</span>(graph, start):
    visited, queue = {start}, deque([start])
    <span class="kw">while</span> queue:
        node = queue.popleft()
        <span class="fn">print</span>(node)
        <span class="kw">for</span> nbr <span class="kw">in</span> graph[node]:
            <span class="kw">if</span> nbr <span class="kw">not in</span> visited:
                visited.add(nbr)
                queue.append(nbr)</code></pre>

    <h4>DFS — Depth-First Search</h4>
    <p>Explore as deep as possible before backtracking. Uses a stack (or recursion). Used for cycle detection, topological sort, and connected components.</p>

    <h3>Dynamic Programming</h3>
    <p>Break a problem into overlapping subproblems and store solutions to avoid recomputation. Two approaches: top-down (memoization) and bottom-up (tabulation).</p>

    <pre><code><span class="comment"># Fibonacci: naive O(2^n) → DP O(n)</span>
<span class="kw">def</span> <span class="fn">fib</span>(n, memo={}):
    <span class="kw">if</span> n <= 1: <span class="kw">return</span> n
    <span class="kw">if</span> n <span class="kw">not in</span> memo:
        memo[n] = <span class="fn">fib</span>(n-1) + <span class="fn">fib</span>(n-2)
    <span class="kw">return</span> memo[n]

<span class="comment"># Knapsack (bottom-up tabulation)</span>
<span class="kw">def</span> <span class="fn">knapsack</span>(weights, values, W):
    n  = len(weights)
    dp = [[0]*(W+1) <span class="kw">for</span> _ <span class="kw">in</span> range(n+1)]
    <span class="kw">for</span> i <span class="kw">in</span> range(1, n+1):
        <span class="kw">for</span> w <span class="kw">in</span> range(W+1):
            dp[i][w] = dp[i-1][w]
            <span class="kw">if</span> weights[i-1] <= w:
                dp[i][w] = max(dp[i][w],
                    dp[i-1][w-weights[i-1]] + values[i-1])
    <span class="kw">return</span> dp[n][W]</code></pre>

    <h3>Divide &amp; Conquer</h3>
    <p>Split the problem into independent subproblems, solve each recursively, and combine. Merge sort, quick sort, and binary search all use this paradigm.</p>

    <h3>Greedy Algorithms</h3>
    <p>Make the locally optimal choice at each step, hoping to find a global optimum. Works for problems with the greedy-choice property (e.g., Dijkstra, Huffman encoding, activity selection).</p>

  </section>

  <div class="divider">§</div>

  <!-- ── 03 COMPLEXITY ── -->
  <section class="section" id="complexity">
    <div class="section-header">
      <span class="section-num">03</span>
      <h2 class="section-title">Complexity &amp; Big-O</h2>
    </div>

    <p>Computational complexity describes how resource usage (time or space) grows as input size increases. Big-O notation gives an upper bound on this growth, ignoring constants and lower-order terms.</p>

    <div class="pull-quote">"The goal is not to write fast code — it is to write code whose slowness is predictable."</div>

    <div class="table-wrap">
      <table>
        <thead>
          <tr><th>Notation</th><th>Name</th><th>Example</th><th>n=1000</th></tr>
        </thead>
        <tbody>
          <tr><td><code>O(1)</code></td><td>Constant</td><td>Array index, hash lookup</td><td><span class="badge fast">1 op</span></td></tr>
          <tr><td><code>O(log n)</code></td><td>Logarithmic</td><td>Binary search, BST lookup</td><td><span class="badge fast">~10 ops</span></td></tr>
          <tr><td><code>O(n)</code></td><td>Linear</td><td>Linear scan, single loop</td><td><span class="badge fast">1,000</span></td></tr>
          <tr><td><code>O(n log n)</code></td><td>Linearithmic</td><td>Merge sort, heap sort</td><td><span class="badge medium">~10,000</span></td></tr>
          <tr><td><code>O(n²)</code></td><td>Quadratic</td><td>Nested loops, bubble sort</td><td><span class="badge slow">1,000,000</span></td></tr>
          <tr><td><code>O(2ⁿ)</code></td><td>Exponential</td><td>Subset enumeration</td><td><span class="badge slow">2^1000 ≈ ∞</span></td></tr>
          <tr><td><code>O(n!)</code></td><td>Factorial</td><td>Permutations, brute TSP</td><td><span class="badge slow">n! ≈ ∞</span></td></tr>
        </tbody>
      </table>
    </div>

    <h3>Rules for Calculating Big-O</h3>
    <ol>
      <li>Drop constants: <code>O(2n)</code> → <code>O(n)</code></li>
      <li>Drop non-dominant terms: <code>O(n² + n)</code> → <code>O(n²)</code></li>
      <li>Sequential steps add: <code>O(n) + O(m)</code> → <code>O(n + m)</code></li>
      <li>Nested steps multiply: a loop inside a loop → <code>O(n × m)</code></li>
      <li>Recursive algorithms: often analyzed with the Master Theorem</li>
    </ol>

    <div class="callout">
      <div class="callout-title">The Master Theorem</div>
      <p>For <code>T(n) = aT(n/b) + O(n^d)</code>: if d > log_b(a) → O(n^d); if d = log_b(a) → O(n^d log n); if d &lt; log_b(a) → O(n^(log_b a)). Merge sort has a=2, b=2, d=1 → O(n log n).</p>
    </div>

    <h3>Space Complexity</h3>
    <p>Measures memory usage as a function of input size. An in-place algorithm uses O(1) extra space. Recursion uses O(depth) stack space — a key hidden cost.</p>

    <h3>P vs NP</h3>
    <p><strong>P</strong> is the class of problems solvable in polynomial time. <strong>NP</strong> is the class of problems whose solutions can be verified in polynomial time. Whether P = NP is the most famous unsolved problem in computer science. NP-complete problems (like SAT, TSP, 3-coloring) are the hardest in NP — if any one is in P, then all of NP is in P.</p>

  </section>

  <div class="divider">§</div>

  <!-- ── 04 SYSTEMS ── -->
  <section class="section" id="systems">
    <div class="section-header">
      <span class="section-num">04</span>
      <h2 class="section-title">Computer Systems</h2>
    </div>

    <p>A computer system is a hierarchy of abstractions — from transistors switching billions of times per second, all the way up to the applications you run.</p>

    <h3>Von Neumann Architecture</h3>

    <div class="diagram">
┌─────────────────────────────────────────────────────┐
│                    CPU                              │
│  ┌────────────┐   ┌──────────────────────────────┐  │
│  │    ALU     │   │         Control Unit         │  │
│  │ +  -  &amp;  | │   │  Fetch → Decode → Execute    │  │
│  └────────────┘   └──────────────────────────────┘  │
│            ↕  Registers (PC, IR, MAR, MDR)          │
└─────────────────────┬───────────────────────────────┘
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│  System Bus
┌────────────────┐    │    ┌───────────────────────────┐
│   Main Memory  │────┘    │        I/O Devices        │
│  (RAM / DRAM)  │         │  Disk, Keyboard, Display  │
└────────────────┘         └───────────────────────────┘</div>

    <h3>Memory Hierarchy</h3>
    <p>Speed and size trade off against each other. The closer to the CPU, the faster and smaller (and more expensive).</p>

    <div class="table-wrap">
      <table>
        <thead>
          <tr><th>Level</th><th>Type</th><th>Latency</th><th>Typical Size</th></tr>
        </thead>
        <tbody>
          <tr><td>Registers</td><td>CPU internal</td><td>~0.3 ns</td><td>32–256 bytes</td></tr>
          <tr><td>L1 Cache</td><td>SRAM</td><td>~1 ns</td><td>32–64 KB</td></tr>
          <tr><td>L2 Cache</td><td>SRAM</td><td>~4 ns</td><td>256 KB – 1 MB</td></tr>
          <tr><td>L3 Cache</td><td>SRAM</td><td>~30 ns</td><td>4–64 MB</td></tr>
          <tr><td>Main RAM</td><td>DRAM</td><td>~100 ns</td><td>8–64 GB</td></tr>
          <tr><td>SSD</td><td>Flash</td><td>~100 µs</td><td>256 GB – 4 TB</td></tr>
          <tr><td>HDD</td><td>Magnetic</td><td>~10 ms</td><td>1–20 TB</td></tr>
        </tbody>
      </table>
    </div>

    <h3>Instruction Set Architecture (ISA)</h3>
    <p>The ISA is the contract between hardware and software — it defines the instructions a CPU can execute. RISC (ARM, RISC-V) uses simple, uniform instructions. CISC (x86) uses complex variable-length instructions. Modern CPUs internally translate CISC to RISC-like micro-ops.</p>

    <h3>Pipelining &amp; Parallelism</h3>
    <div class="card-grid">
      <div class="card blue">
        <div class="card-label">Pipelining</div>
        <h4>Instruction-level</h4>
        <p>Overlap fetch/decode/execute of different instructions. 5-stage pipeline: IF → ID → EX → MEM → WB.</p>
      </div>
      <div class="card green">
        <div class="card-label">Superscalar</div>
        <h4>Multiple execution units</h4>
        <p>Issue multiple instructions per clock cycle. Modern CPUs issue 3–6 instructions per cycle.</p>
      </div>
      <div class="card purple">
        <div class="card-label">Out-of-Order</div>
        <h4>Dynamic scheduling</h4>
        <p>Execute instructions as operands become ready, not in program order. Hides latency dramatically.</p>
      </div>
    </div>

    <h3>Compilation Pipeline</h3>
    <ol class="steps">
      <li>Lexical analysis (tokenization) — source text → token stream</li>
      <li>Parsing — token stream → Abstract Syntax Tree (AST)</li>
      <li>Semantic analysis — type checking, scope resolution</li>
      <li>Intermediate code generation — AST → IR (e.g., LLVM IR)</li>
      <li>Optimization — constant folding, inlining, loop unrolling</li>
      <li>Code generation — IR → target assembly/machine code</li>
    </ol>

  </section>

  <div class="divider">§</div>

  <!-- ── 05 NETWORKING ── -->
  <section class="section" id="networking">
    <div class="section-header">
      <span class="section-num">05</span>
      <h2 class="section-title">Networking</h2>
    </div>

    <p>Computer networks enable communication between billions of devices. Understanding network fundamentals is essential for building distributed systems, web applications, and secure services.</p>

    <h3>The OSI Model</h3>

    <div class="diagram">
Layer 7 — APPLICATION  &nbsp;&nbsp;HTTP, DNS, SMTP, FTP, SSH
Layer 6 — PRESENTATION &nbsp;Encryption, compression, encoding
Layer 5 — SESSION      &nbsp;&nbsp;&nbsp;Connection management, checkpoints
Layer 4 — TRANSPORT    &nbsp;&nbsp;&nbsp;TCP / UDP — ports, reliability
Layer 3 — NETWORK      &nbsp;&nbsp;&nbsp;IP — routing, addressing
Layer 2 — DATA LINK    &nbsp;&nbsp;&nbsp;Ethernet, Wi-Fi — MAC addresses
Layer 1 — PHYSICAL     &nbsp;&nbsp;&nbsp;Cables, radio waves, voltage</div>

    <div class="callout">
      <div class="callout-title">Mnemonic</div>
      <p><strong>A</strong>ll <strong>P</strong>eople <strong>S</strong>eem <strong>T</strong>o <strong>N</strong>eed <strong>D</strong>ata <strong>P</strong>rocessing — layers 7 down to 1. Or bottom-up: <strong>P</strong>lease <strong>D</strong>o <strong>N</strong>ot <strong>T</strong>hrow <strong>S</strong>ausage <strong>P</strong>izza <strong>A</strong>way.</p>
    </div>

    <h3>TCP vs UDP</h3>
    <div class="card-grid">
      <div class="card blue">
        <div class="card-label">TCP</div>
        <h4>Transmission Control Protocol</h4>
        <p>Connection-oriented. Guarantees delivery and order via 3-way handshake, ACKs, and retransmits. Used by HTTP, SMTP, SSH.</p>
      </div>
      <div class="card red">
        <div class="card-label">UDP</div>
        <h4>User Datagram Protocol</h4>
        <p>Connectionless. Fire-and-forget. No guarantees but very low overhead. Used by DNS, video streaming, gaming.</p>
      </div>
    </div>

    <h3>The HTTP Request-Response Cycle</h3>
    <ol class="steps">
      <li>DNS lookup — resolve hostname to IP address</li>
      <li>TCP handshake (SYN → SYN-ACK → ACK) + TLS handshake for HTTPS</li>
      <li>Client sends HTTP request (verb, headers, optional body)</li>
      <li>Server processes request and sends HTTP response (status, headers, body)</li>
      <li>Connection kept alive (HTTP/1.1 keep-alive) or multiplexed (HTTP/2 streams)</li>
    </ol>

    <pre><code><span class="comment"># HTTP Request</span>
GET /api/users HTTP/1.1
Host: api.example.com
Authorization: Bearer &lt;token&gt;
Accept: application/json

<span class="comment"># HTTP Response</span>
HTTP/1.1 200 OK
Content-Type: application/json
{"users": [{"id": 1, "name": "Alice"}]}</code></pre>

    <h3>IP Addressing &amp; Subnetting</h3>
    <p>IPv4 uses 32-bit addresses (e.g., 192.168.1.1). CIDR notation <code>/24</code> means 24 bits for network, 8 for hosts (256 addresses). IPv6 uses 128-bit addresses, providing 2¹²⁸ ≈ 3.4×10³⁸ unique addresses.</p>

  </section>

  <div class="divider">§</div>

  <!-- ── 06 OS ── -->
  <section class="section" id="os">
    <div class="section-header">
      <span class="section-num">06</span>
      <h2 class="section-title">Operating Systems</h2>
    </div>

    <p>The OS is the master control program that manages hardware resources and provides a clean abstraction layer for applications.</p>

    <h3>Processes &amp; Threads</h3>
    <div class="card-grid">
      <div class="card red">
        <div class="card-label">Process</div>
        <h4>Isolated execution unit</h4>
        <p>Has its own virtual address space, file handles, and resources. Costly to create/switch. Failure is isolated.</p>
      </div>
      <div class="card blue">
        <div class="card-label">Thread</div>
        <h4>Lightweight unit</h4>
        <p>Shares address space with siblings. Cheap to create. One crash can kill the whole process. Needs synchronization.</p>
      </div>
    </div>

    <h3>Process Scheduling</h3>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Algorithm</th><th>Description</th><th>Preemptive?</th></tr></thead>
        <tbody>
          <tr><td>FCFS</td><td>First-Come First-Served — simple queue</td><td>No</td></tr>
          <tr><td>SJF</td><td>Shortest-Job-First — minimize average wait</td><td>No</td></tr>
          <tr><td>Round Robin</td><td>Each process gets a time quantum in turn</td><td>Yes</td></tr>
          <tr><td>Priority</td><td>Highest priority runs first; risk of starvation</td><td>Yes/No</td></tr>
          <tr><td>MLFQ</td><td>Multi-Level Feedback Queue — adaptive priority</td><td>Yes</td></tr>
        </tbody>
      </table>
    </div>

    <h3>Memory Management</h3>
    <p>The OS divides physical RAM into pages (typically 4 KB) and gives each process a virtual address space. The MMU (Memory Management Unit) translates virtual → physical addresses via page tables. Virtual memory allows processes to use more memory than physically available by paging to disk.</p>

    <h3>Synchronization</h3>
    <pre><code><span class="comment"># Race condition — two threads increment a counter</span>
<span class="comment"># Thread A reads x=5, Thread B reads x=5</span>
<span class="comment"># Both write x=6 instead of x=7 ← data race!</span>

<span class="comment"># Mutex (Mutual Exclusion) fixes this</span>
<span class="kw">import</span> threading
lock = threading.Lock()

<span class="kw">with</span> lock:          <span class="comment"># acquire → critical section → release</span>
    counter += 1</code></pre>

    <div class="callout">
      <div class="callout-title">Deadlock — Four Necessary Conditions (Coffman)</div>
      <p>Mutual exclusion · Hold and wait · No preemption · Circular wait. All four must hold simultaneously for deadlock to occur. Break any one to prevent it.</p>
    </div>

    <h3>File Systems</h3>
    <p>File systems organize persistent storage into a logical hierarchy. Key concepts include inodes (metadata records), directory entries, block allocation, journaling for crash recovery, and copy-on-write (used by ZFS, Btrfs).</p>

  </section>

  <div class="divider">§</div>

  <!-- ── 07 DATABASES ── -->
  <section class="section" id="databases">
    <div class="section-header">
      <span class="section-num">07</span>
      <h2 class="section-title">Databases</h2>
    </div>

    <p>Databases provide organized, persistent storage with mechanisms for querying, updating, and ensuring the consistency of data.</p>

    <h3>Relational Databases &amp; SQL</h3>
    <p>Data is organized into tables with rows and columns. Relationships are expressed through foreign keys. The structured query language SQL handles all operations.</p>

    <pre><code><span class="comment">-- Create and query a relational schema</span>
<span class="kw">CREATE TABLE</span> users (
    id       <span class="type">INTEGER PRIMARY KEY</span>,
    name     <span class="type">TEXT NOT NULL</span>,
    email    <span class="type">TEXT UNIQUE</span>,
    joined   <span class="type">DATE DEFAULT</span> CURRENT_DATE
);

<span class="comment">-- JOIN: combine rows from two tables</span>
<span class="kw">SELECT</span> u.name, COUNT(o.id) AS orders
<span class="kw">FROM</span>   users u
<span class="kw">LEFT JOIN</span> orders o <span class="kw">ON</span> u.id = o.user_id
<span class="kw">GROUP BY</span> u.id
<span class="kw">HAVING</span>  COUNT(o.id) > 5
<span class="kw">ORDER BY</span> orders DESC;</code></pre>

    <h3>ACID Properties</h3>
    <div class="card-grid">
      <div class="card red">
        <div class="card-label">Atomicity</div>
        <h4>All or nothing</h4>
        <p>A transaction either fully commits or fully rolls back. No partial writes.</p>
      </div>
      <div class="card blue">
        <div class="card-label">Consistency</div>
        <h4>Valid state only</h4>
        <p>Transactions bring the DB from one valid state to another, honoring all constraints.</p>
      </div>
      <div class="card green">
        <div class="card-label">Isolation</div>
        <h4>Concurrent safety</h4>
        <p>Concurrent transactions appear serial to each other. Prevents dirty reads and phantom reads.</p>
      </div>
      <div class="card purple">
        <div class="card-label">Durability</div>
        <h4>Committed = persistent</h4>
        <p>Once committed, data survives crashes. Achieved via write-ahead logging.</p>
      </div>
    </div>

    <h3>Indexing</h3>
    <p>Indexes are auxiliary data structures (usually B-trees) that allow the database to find rows without scanning the entire table. A B-tree index reduces lookup from O(n) to O(log n). Trade-off: indexes speed up reads but slow down writes and consume space.</p>

    <h3>NoSQL Databases</h3>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Type</th><th>Example</th><th>Data Model</th><th>Use Case</th></tr></thead>
        <tbody>
          <tr><td>Document</td><td>MongoDB</td><td>JSON documents</td><td>Content, catalogs, user profiles</td></tr>
          <tr><td>Key-Value</td><td>Redis</td><td>Dictionary</td><td>Caching, sessions, leaderboards</td></tr>
          <tr><td>Column-family</td><td>Cassandra</td><td>Wide rows</td><td>Time-series, IoT, analytics</td></tr>
          <tr><td>Graph</td><td>Neo4j</td><td>Nodes + edges</td><td>Social graphs, recommendations</td></tr>
        </tbody>
      </table>
    </div>

    <h3>CAP Theorem</h3>
    <p>In a distributed system, you can guarantee at most two of: <strong>Consistency</strong> (all nodes see the same data), <strong>Availability</strong> (every request gets a response), and <strong>Partition tolerance</strong> (the system works despite network splits). Since partitions are unavoidable in distributed systems, the real trade-off is CP vs AP.</p>

  </section>

  <div class="divider">§</div>

  <!-- ── 08 OOP ── -->
  <section class="section" id="oop">
    <div class="section-header">
      <span class="section-num">08</span>
      <h2 class="section-title">Object-Oriented Programming</h2>
    </div>

    <p>OOP organizes software around objects — bundles of data (attributes) and behavior (methods). It models the real world and enables code reuse, modularity, and maintainability.</p>

    <h3>Four Pillars</h3>
    <div class="card-grid">
      <div class="card red">
        <div class="card-label">Encapsulation</div>
        <h4>Bundle data + behavior</h4>
        <p>Hide internal state. Expose only what's needed via a public interface. Prevents misuse and coupling.</p>
      </div>
      <div class="card blue">
        <div class="card-label">Abstraction</div>
        <h4>Hide complexity</h4>
        <p>Work with high-level concepts, not implementation details. Interfaces and abstract classes define contracts.</p>
      </div>
      <div class="card green">
        <div class="card-label">Inheritance</div>
        <h4>Reuse via hierarchy</h4>
        <p>A subclass inherits attributes/methods from its parent. Enables code reuse and polymorphic behavior.</p>
      </div>
      <div class="card purple">
        <div class="card-label">Polymorphism</div>
        <h4>One interface, many forms</h4>
        <p>The same method call behaves differently based on the object's actual type. Enables extensible systems.</p>
      </div>
    </div>

    <pre><code><span class="kw">class</span> <span class="type">Animal</span>:
    <span class="kw">def</span> <span class="fn">__init__</span>(self, name: <span class="type">str</span>):
        self._name = name            <span class="comment"># encapsulated</span>

    <span class="kw">def</span> <span class="fn">speak</span>(self) -> <span class="type">str</span>:          <span class="comment"># overridable</span>
        <span class="kw">raise</span> NotImplementedError

<span class="kw">class</span> <span class="type">Dog</span>(<span class="type">Animal</span>):                   <span class="comment"># inheritance</span>
    <span class="kw">def</span> <span class="fn">speak</span>(self): <span class="kw">return</span> <span class="str">"Woof!"</span>  <span class="comment"># polymorphism</span>

<span class="kw">class</span> <span class="type">Cat</span>(<span class="type">Animal</span>):
    <span class="kw">def</span> <span class="fn">speak</span>(self): <span class="kw">return</span> <span class="str">"Meow!"</span>

animals = [<span class="type">Dog</span>(<span class="str">"Rex"</span>), <span class="type">Cat</span>(<span class="str">"Luna"</span>)]
<span class="kw">for</span> a <span class="kw">in</span> animals: <span class="fn">print</span>(a.<span class="fn">speak</span>()) <span class="comment"># Woof! / Meow!</span></code></pre>

    <h3>SOLID Principles</h3>
    <ul>
      <li><strong>S</strong>ingle Responsibility — a class should have one reason to change</li>
      <li><strong>O</strong>pen/Closed — open for extension, closed for modification</li>
      <li><strong>L</strong>iskov Substitution — subclasses must be usable where parents are expected</li>
      <li><strong>I</strong>nterface Segregation — many small interfaces beat one large one</li>
      <li><strong>D</strong>ependency Inversion — depend on abstractions, not concretions</li>
    </ul>

    <h3>Common Design Patterns</h3>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Pattern</th><th>Category</th><th>Intent</th></tr></thead>
        <tbody>
          <tr><td>Singleton</td><td>Creational</td><td>Ensure a class has only one instance</td></tr>
          <tr><td>Factory</td><td>Creational</td><td>Delegate instantiation to a method/class</td></tr>
          <tr><td>Observer</td><td>Behavioral</td><td>Notify dependents when state changes</td></tr>
          <tr><td>Strategy</td><td>Behavioral</td><td>Encapsulate interchangeable algorithms</td></tr>
          <tr><td>Decorator</td><td>Structural</td><td>Add responsibilities without subclassing</td></tr>
          <tr><td>Adapter</td><td>Structural</td><td>Bridge incompatible interfaces</td></tr>
        </tbody>
      </table>
    </div>

  </section>

  <div class="divider">§</div>

  <!-- ── 09 LOGIC ── -->
  <section class="section" id="logic">
    <div class="section-header">
      <span class="section-num">09</span>
      <h2 class="section-title">Logic &amp; Theory</h2>
    </div>

    <p>The theoretical foundations of computer science draw from mathematics, logic, and formal language theory. These underpin compiler design, cryptography, AI, and the fundamental limits of computation.</p>

    <h3>Boolean Algebra</h3>
    <p>All digital circuits are built from Boolean logic operations on binary values (0/1, false/true). Boolean algebra's axioms underlie everything from simple gates to CPUs.</p>

    <div class="table-wrap">
      <table>
        <thead><tr><th>Operation</th><th>Symbol</th><th>Truth (A,B → out)</th><th>Gate</th></tr></thead>
        <tbody>
          <tr><td>AND</td><td>&amp;</td><td>1,1→1; else→0</td><td>Both inputs must be 1</td></tr>
          <tr><td>OR</td><td>|</td><td>0,0→0; else→1</td><td>At least one input must be 1</td></tr>
          <tr><td>NOT</td><td>~</td><td>0→1; 1→0</td><td>Inverts input (unary)</td></tr>
          <tr><td>XOR</td><td>^</td><td>same→0; diff→1</td><td>Exactly one input is 1</td></tr>
          <tr><td>NAND</td><td>~&</td><td>NOT(AND)</td><td>Universal gate</td></tr>
        </tbody>
      </table>
    </div>

    <h3>Number Systems</h3>
    <pre><code><span class="comment"># Decimal 42 expressed in different bases</span>
Binary  (base-2):  0b101010  → 32+8+2 = 42
Octal   (base-8):  0o52      → 5×8+2  = 42
Hex     (base-16): 0x2A      → 2×16+10 = 42

<span class="comment"># Bit manipulation (fast, low-level tricks)</span>
n &amp; 1          <span class="comment"># check if odd</span>
n &lt;&lt; 1         <span class="comment"># multiply by 2</span>
n >> 1         <span class="comment"># integer divide by 2</span>
n &amp; (n - 1)   <span class="comment"># clear lowest set bit</span>
n ^ n          <span class="comment"># always 0 (same value XOR itself)</span></code></pre>

    <h3>Formal Languages &amp; Automata</h3>
    <div class="card-grid">
      <div class="card teal">
        <div class="card-label">Regular Languages</div>
        <h4>Finite Automata</h4>
        <p>Recognized by DFA/NFA. Described by regular expressions. Used for lexers, pattern matching.</p>
      </div>
      <div class="card blue">
        <div class="card-label">Context-Free Languages</div>
        <h4>Pushdown Automata</h4>
        <p>Described by context-free grammars. Used by parsers for programming languages. Not all CFL can be parsed in O(n).</p>
      </div>
      <div class="card purple">
        <div class="card-label">Recursively Enumerable</div>
        <h4>Turing Machines</h4>
        <p>The most powerful class. Describes everything a computer can do. Some problems are undecidable even here.</p>
      </div>
    </div>

    <h3>Turing Machines &amp; Undecidability</h3>
    <p>A Turing machine is an abstract model of computation: an infinite tape, a read/write head, and a finite state table. Church-Turing thesis: any effectively computable function can be computed by a Turing machine. The Halting Problem — "will this program halt on this input?" — is famously undecidable: no algorithm can solve it in general.</p>

  </section>

  <div class="divider">§</div>

  <!-- ── 10 SECURITY ── -->
  <section class="section" id="security">
    <div class="section-header">
      <span class="section-num">10</span>
      <h2 class="section-title">Security</h2>
    </div>

    <p>Security is not a feature you add at the end — it is a mindset applied throughout the entire software lifecycle. The CIA triad guides security thinking.</p>

    <div class="card-grid">
      <div class="card red">
        <div class="card-label">Confidentiality</div>
        <h4>Data is private</h4>
        <p>Only authorized parties can read data. Enforced by encryption, access control, and authentication.</p>
      </div>
      <div class="card blue">
        <div class="card-label">Integrity</div>
        <h4>Data is unmodified</h4>
        <p>Data has not been tampered with. Enforced by cryptographic hashes, MACs, and digital signatures.</p>
      </div>
      <div class="card green">
        <div class="card-label">Availability</div>
        <h4>Services are reachable</h4>
        <p>Legitimate users can access the system. Threatened by DoS attacks, failures, and ransomware.</p>
      </div>
    </div>

    <h3>Cryptography</h3>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Type</th><th>Example</th><th>Key</th><th>Use</th></tr></thead>
        <tbody>
          <tr><td>Symmetric</td><td>AES-256</td><td>Same key enc/dec</td><td>Fast bulk encryption</td></tr>
          <tr><td>Asymmetric</td><td>RSA, ECC</td><td>Public/private pair</td><td>Key exchange, signatures</td></tr>
          <tr><td>Hash</td><td>SHA-256</td><td>None (one-way)</td><td>Integrity checks, passwords</td></tr>
          <tr><td>MAC</td><td>HMAC-SHA256</td><td>Shared secret</td><td>Message authentication</td></tr>
        </tbody>
      </table>
    </div>

    <h3>Common Vulnerabilities (OWASP Top 10)</h3>
    <pre><code><span class="comment">-- SQL Injection (NEVER do this)</span>
query = <span class="str">"SELECT * FROM users WHERE name = '"</span> + user_input + <span class="str">"'"</span>
<span class="comment">-- Input: ' OR '1'='1 → returns all rows!</span>

<span class="comment">-- Safe: parameterized queries</span>
cursor.execute(<span class="str">"SELECT * FROM users WHERE name = ?"</span>, (user_input,))

<span class="comment">-- XSS: inject script into page</span>
&lt;input value="&lt;script&gt;steal(document.cookie)&lt;/script&gt;"&gt;
<span class="comment">-- Defense: HTML-encode output, use Content-Security-Policy</span></code></pre>

    <h3>TLS / HTTPS</h3>
    <ol class="steps">
      <li>Client sends ClientHello with supported cipher suites</li>
      <li>Server sends certificate (signed by trusted CA) + ServerHello</li>
      <li>Client verifies certificate chain against root CA store</li>
      <li>Key exchange (ECDHE) establishes a shared session secret</li>
      <li>All subsequent communication encrypted with AES + authenticated with HMAC</li>
    </ol>

    <h3>Authentication &amp; Authorization</h3>
    <div class="callout">
      <div class="callout-title">Key Distinction</div>
      <p><strong>Authentication</strong> (AuthN) — who are you? Passwords, TOTP, biometrics, OAuth tokens.<br>
      <strong>Authorization</strong> (AuthZ) — what can you do? RBAC, ACLs, policy engines (OPA, Cedar).</p>
    </div>

    <div class="card-grid">
      <div class="card teal">
        <div class="card-label">Zero Trust</div>
        <h4>"Never trust, always verify"</h4>
        <p>Authenticate and authorize every request, even internal ones. Assume the network is hostile.</p>
      </div>
      <div class="card purple">
        <div class="card-label">Defense in Depth</div>
        <h4>Multiple layers</h4>
        <p>No single control is sufficient. Layer firewall, WAF, app security, encryption, monitoring, and alerting.</p>
      </div>
    </div>
  </section>

</main>

<footer>
  Computer Science Fundamentals Guide &nbsp;·&nbsp; 10 Chapters &nbsp;·&nbsp; Built for learners &amp; practitioners &nbsp;·&nbsp; 2025
</footer>

</body>
</html>
