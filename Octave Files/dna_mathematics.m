% =========================================================================
%  dna_mathematics.m  --  The Mathematics of DNA
% =========================================================================
%  A self-contained GNU Octave lab exploring the quantitative structure of
%  DNA. Nothing here is illustrative hand-waving: every number is computed
%  from a real sequence (the coding region of human beta-globin, HBB).
%
%  Topics, in order:
%    1.  Base composition & Chargaff's parity rules
%    2.  GC content and GC skew (locating replication origins)
%    3.  Combinatorics of sequence space and the genetic code
%    4.  Shannon information: bits per base, entropy, redundancy
%    5.  Geometry of the B-DNA double helix (parametric model + plot)
%    6.  Melting temperature (three classical estimators)
%    7.  The central dogma as string transforms (transcribe / translate)
%    8.  Sequence comparison: Hamming distance + Needleman-Wunsch alignment
%    9.  A first-order Markov model of the sequence
%   10.  Topology of supercoiling: Lk = Tw + Wr
%
%  Run:   octave dna_mathematics.m       (or source it inside Octave)
%  Four figures are drawn and, if run headless, saved as PNGs.
%
%  Designed for GNU Octave; MATLAB-compatible constructs preferred.
%  Functions are defined first so the file runs identically whether it is
%  executed with `octave file.m` or sourced interactively.
% =========================================================================

1;   % <-- marks this file as a *script*, not a function file

clear; close all;
try, clc; catch, end

% Use a non-interactive toolkit for PNG export when there is no display.
if isempty(getenv('DISPLAY')) && exist('graphics_toolkit', 'builtin')
  try, graphics_toolkit('gnuplot'); catch, end
end

% =========================================================================
%  LOCAL FUNCTIONS  (defined before use for command-line compatibility)
% =========================================================================

function out = complement(seq)
  % Watson-Crick complement, base for base (same 5'->3' reading frame).
  out = seq;                       % masks taken from the ORIGINAL to avoid
  out(seq == 'A') = 'T';           % chained-reassignment errors.
  out(seq == 'T') = 'A';
  out(seq == 'G') = 'C';
  out(seq == 'C') = 'G';
end

function out = revcomp(seq)
  % Reverse complement: the opposite strand read 5'->3'.
  out = fliplr(complement(seq));
end

function d = hamming(a, b)
  % Number of positions at which two equal-length sequences differ.
  if numel(a) ~= numel(b)
    error('hamming: sequences must have equal length');
  end
  d = sum(a ~= b);
end

function H = shannon_entropy(p)
  % Shannon entropy in bits; zero-probability terms are dropped.
  p = p(p > 0);
  H = -sum(p .* log2(p));
end

function [pos, gc] = gc_sliding(seq, w)
  % GC percentage in a sliding window of width w, centred on each position.
  n    = numel(seq);
  isGC = (seq == 'G') | (seq == 'C');
  k    = n - w + 1;
  gc   = zeros(1, k);
  for i = 1:k
    gc(i) = 100 * mean(isGC(i:i+w-1));
  end
  pos = (1:k) + floor(w/2);
end

function [codons, aas, code] = standard_genetic_code()
  % NCBI translation table 1, generated in canonical T,C,A,G order so that
  % the amino-acid string lines up with the classic codon layout.
  bases  = 'TCAG';
  codons = cell(1, 64);
  idx = 1;
  for i = 1:4
    for j = 1:4
      for k = 1:4
        codons{idx} = [bases(i) bases(j) bases(k)];
        idx = idx + 1;
      end
    end
  end
  aas  = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG';
  code = containers.Map(codons, num2cell(aas));
end

function protein = translate(seq, code)
  % Translate a coding strand into single-letter amino acids ('*' = stop,
  % 'X' = unknown/incomplete codon). Reads whole codons only.
  ncod    = floor(numel(seq) / 3);
  protein = repmat('X', 1, ncod);
  for i = 1:ncod
    cod = seq(3*i-2 : 3*i);
    if isKey(code, cod)
      protein(i) = code(cod);
    end
  end
end

function P = transition_matrix(seq)
  % First-order Markov transition matrix over {A,C,G,T}; rows sum to 1.
  bases = 'ACGT';
  P = zeros(4, 4);
  for i = 1:numel(seq)-1
    a = find(bases == seq(i));
    b = find(bases == seq(i+1));
    if ~isempty(a) && ~isempty(b)
      P(a, b) = P(a, b) + 1;
    end
  end
  rs = sum(P, 2);
  rs(rs == 0) = 1;          % avoid division by zero for absent states
  P = P ./ rs;
end

function [score, a1, a2] = needleman_wunsch(s, t, match, mismatch, gap)
  % Global alignment by dynamic programming. Returns the optimal score and
  % one optimal alignment (a1 aligned to a2, '-' = gap).
  n = numel(s); m = numel(t);
  F = zeros(n+1, m+1);
  F(:, 1) = (0:n)' * gap;
  F(1, :) = (0:m)  * gap;
  for i = 1:n
    for j = 1:m
      if s(i) == t(j), sc = match; else, sc = mismatch; end
      F(i+1, j+1) = max([F(i,   j)   + sc, ...
                         F(i,   j+1) + gap, ...
                         F(i+1, j)   + gap]);
    end
  end
  score = F(n+1, m+1);

  % Traceback from the bottom-right corner.
  a1 = ''; a2 = '';
  i = n; j = m;
  while i > 0 || j > 0
    if i > 0 && j > 0
      if s(i) == t(j), sc = match; else, sc = mismatch; end
      diagOK = (F(i+1, j+1) == F(i, j) + sc);
    else
      diagOK = false;
    end
    if diagOK
      a1 = [s(i) a1]; a2 = [t(j) a2]; i = i - 1; j = j - 1;
    elseif i > 0 && F(i+1, j+1) == F(i, j+1) + gap
      a1 = [s(i) a1]; a2 = ['-' a2]; i = i - 1;
    else
      a1 = ['-' a1]; a2 = [t(j) a2]; j = j - 1;
    end
  end
end

function save_fig(fname)
  % Save the current figure to PNG (used when running headless). Silent on
  % failure so interactive sessions are unaffected.
  try
    print(gcf, fname, '-dpng', '-r120');
  catch
  end
end

% =========================================================================
%  MAIN ANALYSIS
% =========================================================================

% The subject: the coding sequence of human beta-globin (HBB), 5' -> 3'.
seq = ['ATGGTGCACCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACG' ...
       'TGGATGAAGTTGGTGGTGAGGCCCTGGGCAGGCTGCTGGTGGTCTACCCTTGGACCCAGAG' ...
       'GTTCTTTGAGTCCTTTGGGGATCTGTCCACTCCTGATGCTGTTATGGGCAACCCTAAGGTG' ...
       'AAGGCTCATGGCAAGAAAGTGCTCGGTGCCTTTAGTGATGGCCTGGCTCACCTGGACAACC' ...
       'TCAAGGGCACCTTTGCCACACTGAGTGAGCTGCACTGTGACAAGCTGCACGTGGATCCTGA' ...
       'GAACTTCAGGCTCCTGGGCAACGTGCTGGTCTGTGTGCTGGCCCACCACTTTGGCAAAGAA' ...
       'TTCACCCCACCAGTGCAGGCTGCCTATCAGAAAGTGGTGGCTGGTGTGGCTAATGCCCTGG' ...
       'CCCACAAGTATCACTAA'];
seq = upper(seq);
N   = numel(seq);

printf('=========================================================\n');
printf('  THE MATHEMATICS OF DNA\n');
printf('  Sequence: human beta-globin (HBB) coding region\n');
printf('  Length N = %d nucleotides\n', N);
printf('=========================================================\n\n');

% -------------------------------------------------------------------------
%  1. BASE COMPOSITION & CHARGAFF'S PARITY RULES
% -------------------------------------------------------------------------
nA = sum(seq == 'A');  nC = sum(seq == 'C');
nG = sum(seq == 'G');  nT = sum(seq == 'T');
counts = [nA nC nG nT];
freq   = counts / N;

printf('[1] BASE COMPOSITION\n');
printf('    A = %3d (%.1f%%)   C = %3d (%.1f%%)\n', nA, 100*freq(1), nC, 100*freq(2));
printf('    G = %3d (%.1f%%)   T = %3d (%.1f%%)\n', nG, 100*freq(3), nT, 100*freq(4));

% Chargaff's FIRST rule is a statement about the *duplex*: because A pairs
% with T and G with C, the whole double helix has #A = #T and #G = #C.
comp = complement(seq);
printf('\n    Chargaff I (whole duplex, exact by base pairing):\n');
printf('       #A(top)=%d  ==  #T(bottom)=%d\n', nA, sum(comp=='T'));
printf('       #G(top)=%d  ==  #C(bottom)=%d\n', nG, sum(comp=='C'));

% Chargaff's SECOND rule: within a *single* strand, %A ~ %T and %G ~ %C for
% long genomes. Only approximate for a short gene like this one.
printf('\n    Chargaff II (single strand, approximate):\n');
printf('       %%A=%.1f  vs  %%T=%.1f    |diff| = %.1f\n', ...
       100*freq(1), 100*freq(4), 100*abs(freq(1)-freq(4)));
printf('       %%G=%.1f  vs  %%C=%.1f    |diff| = %.1f\n\n', ...
       100*freq(3), 100*freq(2), 100*abs(freq(3)-freq(2)));

figure('Name', 'Base composition');
bar(counts, 'facecolor', [0.20 0.45 0.75]);
set(gca, 'xticklabel', {'A','C','G','T'});
ylabel('count'); title('Base composition of HBB coding region');
grid on;
save_fig('dna_composition.png');

% -------------------------------------------------------------------------
%  2. GC CONTENT AND GC SKEW
% -------------------------------------------------------------------------
gc_total = 100 * (nG + nC) / N;
printf('[2] GC CONTENT\n');
printf('    Overall GC content = %.1f%%\n', gc_total);

w = 30;
[wpos, gcwin] = gc_sliding(seq, w);

g = double(seq == 'G');
c = double(seq == 'C');
skew_cum = cumsum(g - c);
printf('    Cumulative GC skew: min = %d at position %d,\n', ...
       min(skew_cum), find(skew_cum == min(skew_cum), 1));
printf('                        max = %d at position %d\n\n', ...
       max(skew_cum), find(skew_cum == max(skew_cum), 1));

figure('Name', 'GC content and skew');
subplot(2,1,1);
plot(wpos, gcwin, 'linewidth', 1.4, 'color', [0.20 0.45 0.75]);
hold on; plot([1 N], [gc_total gc_total], '--', 'color', [0.6 0.6 0.6]);
xlabel(sprintf('position (window = %d bp)', w));
ylabel('GC %'); title('Sliding-window GC content'); grid on; xlim([1 N]);
subplot(2,1,2);
plot(1:N, skew_cum, 'linewidth', 1.4, 'color', [0.75 0.30 0.25]);
xlabel('position'); ylabel('cumulative (G - C)');
title('Cumulative GC skew'); grid on; xlim([1 N]);
save_fig('dna_gc.png');

% -------------------------------------------------------------------------
%  3. COMBINATORICS OF SEQUENCE SPACE AND THE GENETIC CODE
% -------------------------------------------------------------------------
printf('[3] COMBINATORICS\n');
log10_space = N * log10(4);
printf('    Distinct sequences of length %d = 4^%d ~ 10^%.1f\n', N, N, log10_space);
printf('    (for scale, atoms in the observable universe ~ 10^80)\n');

[codons, aas, code] = standard_genetic_code();
letters = unique(aas);
printf('\n    Codon space: 4^3 = %d codons  ->  %d symbols (20 aa + stop)\n', ...
       numel(codons), numel(letters));
printf('    Degeneracy (codons per symbol):\n      ');
for k = 1:numel(letters)
  d = sum(aas == letters(k));
  printf('%c:%d ', letters(k), d);
  if mod(k, 7) == 0, printf('\n      '); end
end
printf('\n    Mean degeneracy = %.2f codons/symbol\n\n', 64 / numel(letters));

% -------------------------------------------------------------------------
%  4. SHANNON INFORMATION
% -------------------------------------------------------------------------
printf('[4] INFORMATION THEORY\n');
Hmax  = log2(4);
Hbase = shannon_entropy(freq);
printf('    Max entropy per base       = %.4f bits (uniform ACGT)\n', Hmax);
printf('    Empirical entropy per base = %.4f bits\n', Hbase);
printf('    Redundancy                 = %.4f bits/base (%.1f%%)\n', ...
       Hmax - Hbase, 100*(Hmax - Hbase)/Hmax);
printf('    Total sequence information = %.0f bits ~ %.0f bytes\n', ...
       Hbase * N, Hbase * N / 8);
printf('    (theoretical maximum        = %.0f bits)\n\n', Hmax * N);

% -------------------------------------------------------------------------
%  5. GEOMETRY OF THE B-DNA DOUBLE HELIX
% -------------------------------------------------------------------------
printf('[5] DOUBLE-HELIX GEOMETRY (B-DNA)\n');
rise    = 3.4;                   % angstrom rise per base pair
bp_turn = 10.5;                  % base pairs per helical turn
radius  = 10.0;                  % angstrom (helix diameter ~ 20 A)
twist   = 360 / bp_turn;         % degrees of twist per base pair
pitch   = rise * bp_turn;        % angstrom per full turn
height  = rise * N;              % total length of this molecule

printf('    rise per bp    = %.2f A\n', rise);
printf('    bp per turn    = %.1f\n', bp_turn);
printf('    twist per bp   = %.2f deg\n', twist);
printf('    pitch (1 turn) = %.1f A\n', pitch);
printf('    turns in HBB   = %.1f\n', N / bp_turn);
printf('    molecule length= %.0f A = %.3f um\n', height, height / 1e4);

% Frequently-noted near-coincidence: B-DNA is ~21 A wide, one turn ~34 A;
% 21 and 34 are consecutive Fibonacci numbers and 34/21 ~ phi. A memorable
% approximation, not a deep geometric law.
printf('    Fibonacci aside: pitch/width ~ 34/21 = %.3f  (phi = %.3f)\n\n', ...
       34/21, (1 + sqrt(5)) / 2);

m      = min(N, 42);                 % draw the first m base pairs
idx    = (0:m-1)';
theta  = idx * deg2rad(twist);
z      = idx * rise;
offset = deg2rad(150);               % approximate groove asymmetry
x1 = radius*cos(theta);        y1 = radius*sin(theta);
x2 = radius*cos(theta+offset); y2 = radius*sin(theta+offset);

figure('Name', 'B-DNA double helix');
plot3(x1, y1, z, '-', 'linewidth', 2.2, 'color', [0.20 0.45 0.75]); hold on;
plot3(x2, y2, z, '-', 'linewidth', 2.2, 'color', [0.75 0.30 0.25]);
for i = 1:m
  b = seq(i);
  if b == 'G' || b == 'C'
    col = [0.15 0.55 0.30];    % G:C (3 H-bonds)
  else
    col = [0.85 0.65 0.10];    % A:T (2 H-bonds)
  end
  plot3([x1(i) x2(i)], [y1(i) y2(i)], [z(i) z(i)], '-', ...
        'linewidth', 1.1, 'color', col);
end
axis equal; grid on; view(35, 18);
xlabel('x (A)'); ylabel('y (A)'); zlabel('rise (A)');
title('B-DNA double helix  (blue/red backbones,  green=G:C, gold=A:T)');
save_fig('dna_helix.png');

% -------------------------------------------------------------------------
%  6. MELTING TEMPERATURE
% -------------------------------------------------------------------------
printf('[6] MELTING TEMPERATURE (three estimators)\n');
Tm_wallace = 2*(nA + nT) + 4*(nG + nC);
Tm_basic   = 64.9 + 41*(nG + nC - 16.4) / N;
Na = 0.05;
Tm_salt    = 81.5 + 16.6*log10(Na) + 0.41*gc_total - 675/N;

printf('    Wallace 2(A+T)+4(G+C)      = %.1f C  (short oligos only)\n', Tm_wallace);
printf('    Marmur-Doty (GC, long)     = %.1f C\n', Tm_basic);
printf('    Salt-adjusted, [Na+]=%.2fM = %.1f C\n', Na, Tm_salt);
printf('    (nearest-neighbour thermodynamics is more accurate still)\n\n');

% -------------------------------------------------------------------------
%  7. THE CENTRAL DOGMA AS STRING TRANSFORMS
% -------------------------------------------------------------------------
printf('[7] CENTRAL DOGMA\n');
rc      = revcomp(seq);
mrna    = strrep(seq, 'T', 'U');
protein = translate(seq, code);

printf('    5''  %s ...\n', seq(1:30));
printf('    3''  %s ...   (complement)\n', comp(1:30));
printf('    revcomp  %s ...\n', rc(1:30));
printf('    mRNA     %s ...\n', mrna(1:30));
printf('    protein  %s ...  (%d residues incl. stop)\n\n', ...
       protein(1:min(20, numel(protein))), numel(protein));

% -------------------------------------------------------------------------
%  8. SEQUENCE COMPARISON
% -------------------------------------------------------------------------
printf('[8] SEQUENCE COMPARISON\n');
% Sickle-cell mutation: codon 7 GAG (Glu) -> GTG (Val), a single A->T change
% at position 20. In mature-chain numbering (initiator Met removed) this is
% the famous Glu6 -> Val6 substitution that produces haemoglobin S.
mut     = seq;
mut(20) = 'T';
hd      = hamming(seq, mut);
printf('    HBB vs sickle-cell allele (HbS):\n');
printf('       Hamming distance = %d substitution(s)\n', hd);
printf('       codon 7: %s(%c) -> %s(%c)   [Glu6 -> Val in the mature chain]\n', ...
       seq(19:21), translate(seq(19:21), code), ...
       mut(19:21), translate(mut(19:21), code));

s = 'GATTACA';
t = 'GCATGCU';
[score, a1, a2] = needleman_wunsch(s, t, 1, -1, -2);
printf('\n    Needleman-Wunsch global alignment (match+1, mismatch-1, gap-2):\n');
printf('       %s\n       %s\n       score = %d\n\n', a1, a2, score);

% -------------------------------------------------------------------------
%  9. A FIRST-ORDER MARKOV MODEL
% -------------------------------------------------------------------------
printf('[9] MARKOV TRANSITION MATRIX  P(next | current)\n');
P = transition_matrix(seq);
printf('          ->A     ->C     ->G     ->T\n');
b = 'ACGT';
for i = 1:4
  printf('     %c   %.3f   %.3f   %.3f   %.3f\n', b(i), P(i,:));
end
[V, D] = eig(P');
[~, kk] = min(abs(diag(D) - 1));
pi_stat = abs(V(:, kk)); pi_stat = pi_stat / sum(pi_stat);
printf('    Stationary distribution pi = [%.3f %.3f %.3f %.3f]\n\n', pi_stat);

% -------------------------------------------------------------------------
% 10. TOPOLOGY OF SUPERCOILING:  Lk = Tw + Wr
% -------------------------------------------------------------------------
printf('[10] TOPOLOGY OF SUPERCOILING\n');
% Calugareanu-White-Fuller theorem: for a closed duplex the linking number
% Lk (an integer topological invariant) splits into twist Tw and writhe Wr.
Lk0   = N / bp_turn;      % relaxed linking number
Lk    = round(Lk0) - 2;   % suppose two turns removed (negative supercoils)
Tw    = round(Lk0);       % helical twist stays near relaxed
Wr    = Lk - Tw;          % the deficit becomes writhe (supercoiling)
sigma = (Lk - Lk0) / Lk0; % superhelical density
printf('    Relaxed linking number Lk0 = N/%.1f = %.2f\n', bp_turn, Lk0);
printf('    Assume Lk = %d  =>  Lk = Tw + Wr : %d = %d + (%d)\n', Lk, Lk, Tw, Wr);
printf('    Superhelical density sigma = (Lk-Lk0)/Lk0 = %.3f\n', sigma);
printf('    (living cells hold sigma ~ -0.06, i.e. negatively supercoiled)\n\n');

printf('=========================================================\n');
printf('  Done. Figures: dna_composition, dna_gc, dna_helix.\n');
printf('=========================================================\n');
