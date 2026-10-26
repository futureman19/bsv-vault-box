#!/usr/bin/env python3
"""
VAULT-0002 reference PoC — committee key-release for sealed boxes.

SIMULATION ONLY. No real funds, no broadcast, no production keys.

Cryptographic stand-in: threshold BLS-IBE is replaced by per-box
Feldman-verifiable Shamir shares over secp256k1 (real curve math, stdlib only):
  - dealer posts per-box polynomial commitments C_j = g^{a_j} on-chain
  - operator i's share for box b is s = P_b(i), publicly verifiable:
        g^s == prod_j C_j^{i^j}
  - k valid shares reconstruct ONLY that box's key (Lagrange at 0)
This models the protocol semantics (release gating, public share verification,
aggregation, attribution, discrepancy detection). Production swaps the wrapper
for tlock-style threshold BLS per spec §10.2 — semantics unchanged.
"""
import hashlib, json, os, sys

# ---------------- secp256k1 (minimal, real) ----------------
P  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
Q  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G  = (Gx, Gy)

def inv(a, m): return pow(a % m, m - 2, m)
def padd(A, B):
    if A is None: return B
    if B is None: return A
    if A[0] == B[0] and (A[1] + B[1]) % P == 0: return None
    l = ((3 * A[0] * A[0]) * inv(2 * A[1], P)) % P if A == B \
        else ((B[1] - A[1]) * inv(B[0] - A[0], P)) % P
    x = (l * l - A[0] - B[0]) % P
    return (x, (l * (A[0] - x) - A[1]) % P)
def pmul(k, A=G):
    R = None
    while k:
        if k & 1: R = padd(R, A)
        A = padd(A, A); k >>= 1
    return R

def H(*parts) -> int:
    h = hashlib.sha256()
    for p in parts: h.update(p if isinstance(p, bytes) else str(p).encode())
    return int.from_bytes(h.digest(), 'big') % Q

# ---------------- committee / chain sim ----------------
K_CONF = 3  # test K; spec recommends 6

class Chain:
    """Simulated BSV: opening records + on-chain release registry."""
    def __init__(self):
        self.openings = {}   # box_id -> {conf, covenant_valid}
        self.releases = []   # on-chain release records
        self.commitments = {}  # box_id -> [C_0..C_{k-1}]
    def record_opening(self, box_id, covenant_valid=True):
        self.openings[box_id] = {'conf': 0, 'covenant_valid': covenant_valid}
    def mine(self, n=1):
        for o in self.openings.values(): o['conf'] += n
    def reorg(self, box_id, depth):
        o = self.openings.get(box_id)
        if o: o['conf'] -= depth
    def opening_confirmed(self, box_id):
        o = self.openings.get(box_id)
        return bool(o and o['conf'] >= K_CONF and o['covenant_valid'])

class Operator:
    """Honest key-keeper: enforces the §6 release policy."""
    def __init__(self, idx, shares, alive=True):
        self.idx = idx; self.shares = shares; self.alive = alive; self._released = set()
    def release(self, chain, box_id):
        if not self.alive: return None
        if box_id in self._released: return None                      # idempotence
        if not chain.opening_confirmed(box_id): return None           # POLICY GATE
        self._released.add(box_id)
        rec = {'box_id': box_id, 'operator': self.idx,
               'share': self.shares[box_id], 'sig': f"op{self.idx}:{box_id}"}
        chain.releases.append(rec)                                    # on-chain record
        return rec

def mask(key):
    # hash first: raw big-endian key bytes would leave the high 19 bytes
    # identical for nearby keys, so the XOR must avalanche on ANY key change
    return hashlib.sha256(key.to_bytes(32, 'big')).digest()

class Box:
    def __init__(self, box_id, key, nft, k):
        self.box_id, self.nft, self.k = box_id, nft, k
        # per-box polynomial P(x) = key + a1 x + a2 x^2 ... (degree k-1)
        self.coefs = [key] + [(H(box_id, 'coef', j) % 1000) + 1 for j in range(1, k)]
        self.commitments = [pmul(c) for c in self.coefs]              # Feldman commitments
        self.ciphertext = bytes(a ^ b for a, b in zip(nft.encode(), mask(key)))
        self.sealed, self.unspent = True, True
    def share_for(self, i):
        return sum(c * pow(i, j, Q) for j, c in enumerate(self.coefs)) % Q

# ---------------- verification / aggregation ----------------
def verify_share(commitments, i, share):
    """Feldman: g^share == prod_j C_j^{i^j}  (public, needs no committee trust)"""
    lhs = pmul(share)
    rhs = None
    for j, C in enumerate(commitments): rhs = padd(rhs, pmul(pow(i, j, Q), C))
    return lhs == rhs

def aggregate(shares_by_idx):
    """Lagrange-interpolate at x=0 mod Q -> box key."""
    xs, ys = list(shares_by_idx), [shares_by_idx[x] for x in shares_by_idx]
    key = 0
    for m in range(len(xs)):
        num = den = 1
        for n in range(len(xs)):
            if m == n: continue
            num = num * (-xs[n]) % Q
            den = den * (xs[m] - xs[n]) % Q
        key = (key + ys[m] * num * inv(den, Q)) % Q
    return key

def decrypt(box, key):
    pt = bytes(a ^ b for a, b in zip(box.ciphertext, mask(key)))
    return pt.decode(errors='replace')

def seal_check(chain, box):
    """Extended §7 check: UTXO sealed AND no k aggregatable valid shares."""
    valid = {r['operator']: r['share'] for r in chain.releases
             if r['box_id'] == box.box_id
             and verify_share(chain.commitments[box.box_id], r['operator'], r['share'])}
    if not (box.unspent and box.sealed): return 'OPENED'
    if len(valid) >= box.k:
        return 'SEALED' if chain.opening_confirmed(box.box_id) else 'UNSEALED-DISCREPANCY'
    return 'SEALED'

# ---------------- scenario tests ----------------
def main():
    results = []
    def check(name, cond):
        results.append((name, bool(cond))); print(('PASS ' if cond else 'FAIL ') + name)

    N, K = 5, 3
    chain = Chain()
    boxes = {f'box{i:02d}': Box(f'box{i:02d}', H('key', f'box{i:02d}'),
                                f'NFT-#{i:03d}-preassigned', K) for i in range(3)}
    for b in boxes.values(): chain.commitments[b.box_id] = b.commitments
    ops = [Operator(i, {bid: b.share_for(i) for bid, b in boxes.items()})
           for i in range(1, N + 1)]

    # 1. contents fixed at creation, hidden from everyone (no shares exist yet)
    b0 = boxes['box00']
    check('1 ciphertext commits to pre-assigned NFT',
          decrypt(b0, b0.coefs[0]) == 'NFT-#000-preassigned')
    check('2 no shares on-chain before any opening -> nothing to aggregate',
          len(chain.releases) == 0 and seal_check(chain, b0) == 'SEALED')

    # 3. policy gate: release refused while opening absent/unconfirmed
    chain.record_opening('box00')               # opening tx seen, 0 conf
    refused = all(op.release(chain, 'box00') is None for op in ops)
    check('3 unconfirmed opening -> all operators refuse release', refused)
    chain.mine(K_CONF - 1)                      # still below K
    check('4 opening below K confirmations -> still refused',
          all(op.release(chain, 'box00') is None for op in ops))

    # 5. confirmed opening -> exactly K shares suffice, Feldman-verified
    chain.mine(1)
    recs = [op.release(chain, 'box00') for op in ops[:K]]
    shares = {r['operator']: r['share'] for r in recs}
    check('5 confirmed opening -> k shares released', len(recs) == K)
    check('6 every release share publicly verifiable (Feldman)',
          all(verify_share(chain.commitments['box00'], i, s) for i, s in shares.items()))
    key = aggregate(shares)
    check('7 aggregation recovers key; contents == pre-assigned NFT',
          decrypt(b0, key) == 'NFT-#000-preassigned')

    # 8. k-1 shares cannot reconstruct
    partial = dict(list(shares.items())[:K - 1])
    check('8 k-1 shares insufficient', decrypt(b0, aggregate(partial)) != 'NFT-#000-preassigned')

    # 9. forged share rejected publicly
    forged_ok = verify_share(chain.commitments['box00'], 4, (shares[1] + 1) % Q)
    check('9 forged/altered share fails Feldman verification', not forged_ok)

    # 10. sealed box never opened -> seal holds even after other boxes open
    check('10 untouched box still SEALED', seal_check(chain, boxes['box01']) == 'SEALED')

    # 11. reorg: opening evaporates after release -> UNSEALED-DISCREPANCY
    chain.reorg('box00', K_CONF)                # back to 0 conf
    check('11 reorg past release -> UNSEALED-DISCREPANCY (not marketable as sealed)',
          seal_check(chain, b0) == 'UNSEALED-DISCREPANCY')

    # 12. idempotence + attribution
    again = ops[0].release(chain, 'box00')
    check('12 operator cannot release twice (idempotent)', again is None)
    check('13 every release record attributable to an operator index',
          all('operator' in r and 'sig' in r for r in chain.releases))

    # 14. rogue operator posts share with NO opening at all -> detectable
    chain.releases.append({'box_id': 'box01', 'operator': 9,
                           'share': boxes['box01'].share_for(9), 'sig': 'rogue'})
    rogue = [r for r in chain.releases if r['box_id'] == 'box01'
             and not chain.opening_confirmed('box01')]
    check('14 release with no confirmed opening is self-proving misbehavior',
          len(rogue) == 1 and rogue[0]['operator'] == 9)

    # 15. quorum loss -> permanent seal (liveness assumption demonstrated)
    for op in ops: op.alive = False
    ops[0].alive = ops[1].alive = True          # only 2 of 5 survive, k=3
    ops[0]._released.clear(); ops[1]._released.clear()
    chain.record_opening('box02'); chain.mine(K_CONF)
    recs2 = [r for r in (op.release(chain, 'box02') for op in ops) if r]
    check('15 quorum loss (2<k alive) -> box02 key unrecoverable, permanently sealed',
          len(recs2) == 2 and
          decrypt(boxes['box02'], aggregate({r['operator']: r['share'] for r in recs2}))
          != 'NFT-#002-preassigned')

    # golden vectors (deterministic: coefficients derived from fixed strings)
    vec = {'note': 'SIMULATION vectors - Feldman-Shamir stand-in, NOT production BLS',
           'curve': 'secp256k1', 'k': K, 'n': N, 'K_conf': K_CONF,
           'boxes': {bid: {'nft': b.nft,
                           'coefficients': [str(c) for c in b.coefs],
                           'share_op1': str(b.share_for(1)),
                           'share_op2': str(b.share_for(2)),
                           'share_op3': str(b.share_for(3)),
                           'key': str(b.coefs[0])}
                     for bid, b in boxes.items()}}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'v2_vectors.json'), 'w') as f:
        json.dump(vec, f, indent=2)

    failed = [n for n, ok in results if not ok]
    print(f'\n{len(results) - len(failed)}/{len(results)} tests passed' +
          ('' if not failed else f'  FAILED: {failed}'))
    sys.exit(1 if failed else 0)

if __name__ == '__main__':
    main()
