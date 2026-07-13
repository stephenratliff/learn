NASH & HILBERT Octave Lab Bundle
--------------------------------
GNU Octave 7+ , no toolboxes required.

NASH:
 nash_2x2.m              - 2x2 bimatrix pure + mixed Nash
 best_response_plot.m    - best response vs q
 nash_bargaining.m       - max (u1-d1)*(u2-d2) over polygon
 cournot_nash.m          - Cournot duopoly intersection
 nash_embedding_demo.m   - Nash-Kuiper corrugation length preservation
 nash_moser_newton.m     - smoothed Newton vs plain Newton

HILBERT:
 hilbert_hotel.m         - bijections n->n+1, n->2n, Cantor pairing
 hilbert_space_fourier.m - Fourier series in L2, Parseval, L2 error
 gram_schmidt_hilbert.m  - Modified Gram-Schmidt, orthonormal basis
 spectral_hilbert_demo.m - 2x2 spectral ellipse + hilb(n) cond explosion
 hilbert_curve.m         - space-filling curve order 1-7
 variational_demo.m      - catenary minimizes energy, Euler-Lagrange

Usage:
 octave> nash_2x2([3 0;5 1],[3 5;0 1])
 octave> cournot_nash(20,1,2,3)
 octave> hilbert_space_fourier(15,"square")
 octave> hilbert_curve(5)
 octave> spectral_hilbert_demo(2,1,1)
