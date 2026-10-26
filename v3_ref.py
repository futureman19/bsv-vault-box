#!/usr/bin/env python3
"""
VAULT-0003 reference PoC — draw-at-open mystery packs.

SIMULATION ONLY. No real funds, no broadcast, no production keys.
The chain is simulated: block hashes are deterministic stand-ins
(sha256 of height). Everything protocol-visible is replay-verified.
"""
import hashlib, json, math, os, sys

D = 1  # draw block = open block + D (spec default)

# ---------------- manifest ----------------
def canonical_manifest():
    designs = ([{"id": i, "ref": f"bafy...design{i}", "weight": 100} for i in range(900)] +   # commons
               [{"id": i, "ref": f"bafy...design{i}", "weight": 10} for i in range(900, 990)] + # rares
               [{"id": i, "ref": f"bafy...design{i}", "weight": 1} for i in range(990, 1000)])  # legendaries
    return {
        "name": "Genesis Series", "pack_size": 10, "allow_pack_duplicates": False,
        "designs": designs,
        "total_weight": sum(d["weight"] for d in designs),   # 90,910
        "slots": {"9": {"table": [{"id": i, "weight": 1} for i in range(990, 1000)],
                        "total_weight": 10}},                 # guaranteed legendary slot
        "manifest_version": 1,
    }

def manifest_root(m):
    blob = json.dumps(m, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(blob).hexdigest()

# ---------------- simulated chain ----------------
class Chain:
    def __init__(self):
        self.blocks = {}        # height -> hash
        self.height = 0
        self.txs = {}           # txid -> height
        self._mine()
    def _mine(self):
        self.height += 1
        self.blocks[self.height] = hashlib.sha256(f"block{self.height}".encode()).hexdigest()
    def mine(self, n=1):
        for _ in range(n): self._mine()
    def include(self, txid):
        self.mine(); self.txs[txid] = self.height; return self.height
    def blockhash(self, h): return self.blocks.get(h)
    def reorg(self, txid):
        """open tx falls out of the chain"""
        del self.txs[txid]

# ---------------- the draw (spec section 6, verbatim semantics) ----------------
def draw_index(box_id, seed, slot, retry, total_weight):
    h = hashlib.sha256(f"VAULT3-DRAW|{box_id}|{seed}|{slot}|{retry}".encode()).digest()
    return int.from_bytes(h, 'big') % total_weight

def pick(table, idx):
    cum = 0
    for d in table:
        cum += d["weight"]
        if idx < cum: return d["id"]
    raise AssertionError("weight walk overflow")

def draw_pack(manifest, box_id, seed):
    """Deterministic pack computation from public data. Anyone replays this.
    Dedup scope is PER-TABLE (spec section 6): non-termination is impossible
    if the manifest validity rule holds (table size >= slots bound to it)."""
    pack, retries, seen = [], 0, {}
    for slot in range(manifest["pack_size"]):
        scfg = manifest.get("slots", {}).get(str(slot))
        table, tw = (scfg["table"], scfg["total_weight"]) if scfg \
                    else (manifest["designs"], manifest["total_weight"])
        tkey = f"slot{slot}" if scfg else "main"
        seen.setdefault(tkey, set())
        retry = 0
        while True:
            d = pick(table, draw_index(box_id, seed, slot, retry, tw))
            if manifest["allow_pack_duplicates"] or d not in seen[tkey]: break
            retry += 1; retries += 1
        seen[tkey].add(d)
        pack.append(d)
    return pack, retries

def draw_pack_for_open(manifest, chain, box_id, open_txid):
    """Full pipeline: opening tx -> draw block -> pack. None before collapse."""
    h = chain.txs.get(open_txid)
    if h is None: return None                       # not opened / reorged out
    seed = chain.blockhash(h + D)
    if seed is None: return None                    # draw block doesn't exist yet
    pack, _ = draw_pack(manifest, box_id, seed)
    return pack

def verify_mint(manifest, chain, box_id, open_txid, claimed_designs):
    """Client-side mint validity: claimed pack must equal recomputed pack."""
    pack = draw_pack_for_open(manifest, chain, box_id, open_txid)
    return pack is not None and pack == claimed_designs

# ---------------- tests ----------------
def main():
    results = []
    def check(name, cond): results.append((name, bool(cond))); print(('PASS ' if cond else 'FAIL ') + name)

    man, root = canonical_manifest(), manifest_root(canonical_manifest())
    chain = Chain()

    # 1-2. manifest commitment: deterministic root, tamper-evident
    check('1 manifest root deterministic', root == manifest_root(canonical_manifest()))
    tampered = canonical_manifest(); tampered["designs"][5]["weight"] = 16
    check('2 manifest tamper changes root (odds un-riggable post-launch)',
          manifest_root(tampered) != root)

    # 3-4. no pack before collapse; pack exists after
    check('3 no pack computable before opening (no draw block exists)',
          draw_pack_for_open(man, chain, 'box-alpha', 'tx-open-alpha') is None)
    oh = chain.include('tx-open-alpha')
    check('4 pack still None before draw block (D=1), computable after it',
          draw_pack_for_open(man, chain, 'box-alpha', 'tx-open-alpha') is None and
          (chain.mine(1), draw_pack_for_open(man, chain, 'box-alpha', 'tx-open-alpha'))[1] is not None)

    # 5-6. determinism + independent replay
    p1 = draw_pack_for_open(man, chain, 'box-alpha', 'tx-open-alpha')
    p2 = draw_pack_for_open(man, chain, 'box-alpha', 'tx-open-alpha')
    check('5 pack deterministic', p1 == p2)
    seed = chain.blockhash(oh + D)
    p3, _ = draw_pack(man, 'box-alpha', seed)       # independent replay path
    check('6 independent verifier replays identical pack', p3 == p1)

    # 7. pack shape: 10 cards, main-table slots (0-8) dedup among themselves
    check('7 pack = 10 cards, main-table slots mutually unique',
          len(p1) == 10 and len(set(p1[:9])) == 9)

    # 8. guaranteed slot: slot 9 always legendary across many boxes
    rare_slots = []
    for i in range(60):
        ch = Chain(); ch.include(f'tx{i}'); ch.mine(1)
        pk = draw_pack_for_open(man, ch, f'box{i}', f'tx{i}')
        rare_slots.append(pk[9] >= 990)
    check('8 guaranteed-legendary slot (slot 9) across 60 packs', all(rare_slots))

    # 9. rarity distribution sanity on the main table (slots 0-8 of many packs)
    commons = legendaries = 0
    N = 400
    for i in range(N):
        ch = Chain(); ch.include(f'm{i}'); ch.mine(1)
        pk = draw_pack_for_open(man, ch, f'dist{i}', f'm{i}')
        for d in pk[:9]:
            if d < 900: commons += 1
            elif d >= 990: legendaries += 1
    total = N * 9
    fc, fl = commons/total, legendaries/total
    check(f'9 rarity weights hold (commons~99% got {fc:.1%}, legendaries~0.01% got {fl:.2%})',
          fc > 0.95 and fl < 0.01)

    # 10. Version A honesty: 1000 cards from 1000 designs -> ~63% unique
    seen = set(); tot = 0
    for i in range(100):
        ch = Chain(); ch.include(f'c{i}'); ch.mine(1)
        pk = draw_pack_for_open(man, ch, f'cc{i}', f'c{i}')
        seen.update(pk); tot += len(pk)
    check(f'10 across 1000 cards: {len(seen)} unique designs (coupon-collector ~632, duplicates real)',
          550 <= len(seen) <= 720)

    # 11-12. mint validity + invalid-mint rejection
    good = p1
    bad = p1.copy(); bad[0] = (bad[0] + 1) % 1000
    check('11 valid mint accepted (claimed == recomputed)',
          verify_mint(man, chain, 'box-alpha', 'tx-open-alpha', good))
    check('12 INVALID-MINT rejected (claimed != recomputed)',
          not verify_mint(man, chain, 'box-alpha', 'tx-open-alpha', bad))

    # 13. reorg: opening dies -> pack gone; re-open later -> fresh (different) draw
    chain.reorg('tx-open-alpha')
    check('13 reorg erases the pack (box back to sealed, mint orphaned)',
          draw_pack_for_open(man, chain, 'box-alpha', 'tx-open-alpha') is None)
    chain.mine(3); chain.include('tx-open-alpha2'); chain.mine(1)
    p_new = draw_pack_for_open(man, chain, 'box-alpha', 'tx-open-alpha2')
    check('14 re-open draws a fresh pack (overwhelmingly likely different)', p_new != p1)

    # 15. box_id in seed: two boxes in the same block still get different packs
    ch2 = Chain(); ch2.include('txA'); ch2.mine(1)
    check('15 same block, different boxes -> different packs (issuer cannot predict)',
          draw_pack_for_open(man, ch2, 'box-1', 'txA') != draw_pack_for_open(man, ch2, 'box-2', 'txA'))

    # golden vectors (deterministic)
    vec = {'note': 'SIMULATION vectors - block hashes are stand-ins, NOT a live chain',
           'D': D, 'manifest_root': root,
           'example_box': 'box-alpha', 'first_open_height': oh,
           'first_pack': p1, 'reopened_pack': p_new}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'v3_vectors.json'), 'w') as f:
        json.dump(vec, f, indent=2)

    failed = [n for n, ok in results if not ok]
    print(f'\n{len(results)-len(failed)}/{len(results)} tests passed' +
          ('' if not failed else f'  FAILED: {failed}'))
    sys.exit(1 if failed else 0)

if __name__ == '__main__':
    main()
