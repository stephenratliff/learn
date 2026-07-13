% =========================================================================
% FERMAT'S LAST THEOREM — Proof Outline
% =========================================================================
%
% Theorem (Fermat, ~1637):
%   There are no positive integers x, y, z and integer n > 2 such that:
%
%         x^n + y^n = z^n
%
%   Fermat claimed a "marvellous proof" in a margin note, but none was ever
%   found. The theorem remained unproven for 358 years until Andrew Wiles
%   completed a proof in 1995 (announced 1993, gap patched 1994–1995).
%
% Reference:
%   Wiles, A. (1995). "Modular elliptic curves and Fermat's Last Theorem."
%   Annals of Mathematics, 141(3), 443–551.
%   Taylor, R. & Wiles, A. (1995). "Ring-theoretic properties of certain
%   Hecke algebras." Annals of Mathematics, 141(3), 553–572.
%
% =========================================================================
% HIGH-LEVEL PROOF STRATEGY
% =========================================================================
%
% The proof proceeds by contradiction via three major pillars:
%
%  1. Frey Curve Construction
%  2. Ribet's Level-Lowering Theorem  (epsilon conjecture)
%  3. Wiles's Modularity Theorem      (formerly Taniyama–Shimura–Weil)
%
% =========================================================================
% PART 1 — FREY CURVE
% =========================================================================
%
% Suppose, for contradiction, that a non-trivial solution exists:
%
%   a^p + b^p = c^p,   p prime, p >= 5,  a,b,c positive integers.
%
% Gerhard Frey (1986) associated to any such solution an elliptic curve E,
% now called the "Frey curve":
%
%   E : y^2 = x(x - a^p)(x + b^p)
%
% Key properties of E:
%   - It is semistable (specific bad-reduction type at all primes dividing abc).
%   - Its discriminant is  Δ = (abc)^{2p} / 2^8  (up to powers).
%   - Its conductor N_E satisfies  N_E | 2 * rad(abc),  where rad is the
%     radical (product of distinct prime factors).
%   - The mod-p Galois representation  ρ_{E,p}  attached to E[p] has
%     very restricted ramification.
%
% Frey observed that E looked "too special" to be modular — setting the
% stage for a contradiction.
%
% =========================================================================
% PART 2 — RIBET'S THEOREM (1990)
% =========================================================================
%
% Background — Modular Forms:
%   A modular form of weight k and level N is a holomorphic function
%   f : H → C on the upper half-plane satisfying a transformation law
%   under the action of Γ_0(N) ⊂ SL(2,Z) and growth conditions.
%   Each newform f has an attached p-adic Galois representation ρ_{f,p}.
%
% The Epsilon Conjecture (Serre, 1987) — proved by Ribet (1990):
%   If E is a semistable elliptic curve over Q, and ρ_{E,p} arises from
%   a newform f of level N, then ρ_{E,p} also arises from a newform g
%   of level N' where N' is obtained from N by removing all prime factors
%   that divide N but come from the "extra" Frey ramification.
%
% Applied to the Frey Curve:
%   Ribet showed that if E (the Frey curve) is modular, then the associated
%   mod-p representation ρ_{E,p} would have to arise from a newform of
%   level 2.
%
%   But there are NO newforms of weight 2 and level 2.
%   (The space S_2(Γ_0(2)) is empty — a classical fact.)
%
%   ⟹  The Frey curve E cannot be modular.
%
% =========================================================================
% PART 3 — WILES'S MODULARITY THEOREM
% =========================================================================
%
% Taniyama–Shimura–Weil Conjecture (semistable case):
%   Every semistable elliptic curve E over Q is modular, i.e. there
%   exists a newform f of weight 2 such that:
%
%     L(E, s) = L(f, s)
%
%   (their L-functions are equal), or equivalently, ρ_{E,p} ≅ ρ_{f,p}.
%
% Wiles's Strategy — R = T Theorem:
%   Wiles proved the modularity theorem by establishing an isomorphism
%   between two rings:
%
%     R ≅ T
%
%   where:
%     R = Universal deformation ring of ρ_{E,p} (encodes all lifts of
%         the mod-p representation to p-adic representations).
%     T = Hecke algebra acting on a space of modular forms of the
%         appropriate level and weight.
%
%   Proving R ≅ T shows every Galois representation of the right type
%   comes from a modular form — hence E is modular.
%
% Key Technical Ingredients:
%
%   (a) Mazur's Deformation Theory of Galois Representations
%       — Parameterizes p-adic lifts of a residual representation ρ_0.
%
%   (b) Horizontal Iwasawa Theory / Euler Systems (Kolyvagin, Flach)
%       — Bounds the Selmer group; Wiles used a modified Flach system.
%       — Taylor–Wiles method: a patching argument over auxiliary primes
%         Q_n to prove the numerical criterion  #(T/η) | #H^1_f(Q, M).
%
%   (c) Commutative Algebra Criterion (Wiles–Lenstra):
%       If R → T is surjective and  #(T/η)  divides  #(R/η_R),
%       then R ≅ T  (both are complete intersections).
%       Here η is the congruence ideal of the newform f in T.
%
%   (d) Base Change and Solvable Lifting (Langlands, Tunnell):
%       Handles the initial residual representation  ρ_{E,3}  or  ρ_{E,5}
%       to get the proof off the ground (a "3-5 switch" trick).
%
% =========================================================================
% PART 4 — COMPLETING THE CONTRADICTION
% =========================================================================
%
% Summary of logical chain:
%
%   Step 1:  Assume  a^p + b^p = c^p  has a solution for prime p ≥ 5.
%
%   Step 2:  Construct the Frey curve  E : y^2 = x(x-a^p)(x+b^p).
%            E is a semistable elliptic curve over Q.
%
%   Step 3:  By Wiles's Theorem, E is modular  ⟹  ρ_{E,p} comes from
%            some newform f of level N_E.
%
%   Step 4:  By Ribet's Theorem, ρ_{E,p} also comes from a newform of
%            level 2.
%
%   Step 5:  No such newform of level 2 exists.
%
%   Step 6:  CONTRADICTION.  Therefore no solution exists.  □
%
% For n = 4: Proved by Fermat himself via infinite descent.
% For n = p*m (composite): Reducing to the prime case covers all n > 2.
%
% =========================================================================
% SMALL NUMERICAL CHECKS (Octave runnable)
% =========================================================================
% The following code verifies there are no small solutions, as a sanity
% check consistent with FLT for small values.

fprintf('Checking x^n + y^n = z^n for x,y,z in [1,50], n in [3,7]...\n');

solutions_found = 0;
max_val = 50;

for n = 3:7
  for x = 1:max_val
    for y = x:max_val
      % Compute candidate z
      lhs = x^n + y^n;
      z   = round(lhs^(1/n));
      % Check nearby integers to guard against floating-point error
      for zc = max(1, z-1) : z+1
        if zc^n == lhs
          fprintf('  FOUND: %d^%d + %d^%d = %d^%d\n', x, n, y, n, zc, n);
          solutions_found++;
        end
      end
    end
  end
end

if solutions_found == 0
  fprintf('No solutions found — consistent with Fermat''s Last Theorem.\n');
end

% =========================================================================
% END OF FILE
% =========================================================================
