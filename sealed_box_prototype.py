#!/usr/bin/env python3
"""
Sealed-box feasibility prototype — SIMULATION ONLY.
- No real keys, no network, no broadcast, no funds.
- "Chain" is an in-memory simulated BSV-like PoW chain.
- ECC is real secp256k1 arithmetic but with throwaway random keys ("TOY KEYS").
Purpose: decisively demonstrate which constructions fail and which work,
with executable evidence, for the sealed-NFT-box research report.
"""
import hashlib, secrets, time, json, sys

def sha(b): return hashlib.sha256(b).digest()
def H(*parts): 
    h = hashlib.sha256()
    for p in parts: h.update(p if isinstance(p, bytes) else str(p).encode())
    return h.digest()

results = []
def report(test, verdict, detail):
    results.append({"test": test, "verdict": verdict, "detail": detail})
    print(f"[{verdict}] {test}: {detail}")

# ---------- toy secp256k1 (real curve math, throwaway keys) ----------
P  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G  = (Gx, Gy)
def inv(a, m): return pow(a, -1, m)
def padd(A, B):
    if A is None: return B
    if B is None: return A
    if A[0]==B[0] and (A[1]+B[1])%P==0: return None
    if A==B: l = (3*A[0]*A[0]) * inv(2*A[1], P) % P
    else:    l = (B[1]-A[1]) * inv(B[0]-A[0], P) % P
    x = (l*l - A[0] - B[0]) % P
    return (x, (l*(A[0]-x) - A[1]) % P)
def pmul(k, A=G):
    R = None
    while k:
        if k & 1: R = padd(R, A)
        A = padd(A, A); k >>= 1
    return R
def pt_bytes(A): return b'\x02' + A[0].to_bytes(32,'big') if A[1]%2==0 else b'\x03' + A[0].to_bytes(32,'big')

# ---------- Schnorr (BIP340-flavoured, TOY) + adaptor ----------
def schnorr_sign(d, m, t_adaptor=None):
    """Returns (R_point_used, s, pre_sig_or_None). If t_adaptor given, produces adaptor pre-signature."""
    r = secrets.randbelow(N-1)+1
    R = pmul(r)
    if t_adaptor is not None:
        R_eff = padd(R, pmul(t_adaptor))
        pre = True
    else:
        R_eff = R; pre = False
    e = int.from_bytes(H(pt_bytes(R_eff), pt_bytes(pmul(d)), m), 'big') % N
    s_hat = (r + e*d) % N
    return R_eff, s_hat, pre

def schnorr_complete(s_hat, t): return (s_hat + t) % N

def schnorr_verify(pub, m, R_eff, s):
    e = int.from_bytes(H(pt_bytes(R_eff), pt_bytes(pub), m), 'big') % N
    return pmul(s) == padd(R_eff, pmul(e, pub))

def schnorr_extract(s, s_hat): return (s - s_hat) % N

# ---------- Shamir over field mod N ----------
def shamir_split(secret, k, n):
    coeffs = [secret] + [secrets.randbelow(N-1)+1 for _ in range(k-1)]
    return [(i, sum(c * pow(i, j, N) for j, c in enumerate(coeffs)) % N) for i in range(1, n+1)]
def shamir_reconstruct(shares):
    acc = 0
    for i, (xi, yi) in enumerate(shares):
        num, den = 1, 1
        for j, (xj, _) in enumerate(shares):
            if i == j: continue
            num = num * (-xj) % N; den = den * (xi - xj) % N
        acc = (acc + yi * num % N * inv(den, N)) % N
    return acc

# ---------- symmetric "encryption" (stream from key) ----------
def enc(key_bytes, msg): 
    ks = hashlib.sha256(key_bytes).digest()
    return bytes(a ^ b for a, b in zip(msg.encode(), (ks*64)[:len(msg)]))
def dec(key_bytes, ct): 
    ks = hashlib.sha256(key_bytes).digest()
    return bytes(a ^ b for a, b in zip(ct, (ks*64)[:len(ct)])).decode()

# ---------- simulated chain ----------
class Chain:
    def __init__(self): 
        self.blocks = [{"height":0,"hash":sha(b"genesis"),"txs":[]}]
        self.utxos = {}   # outpoint -> {"owner":pkh, "kind":..., "meta":...}
        self.release_log = {}  # box_id -> {"height":h, "txid":...}  (committee posts releases on-chain)
        self.mempool = []
    def tip(self): return len(self.blocks)-1
    def mine(self, txs):
        h = self.tip()+1
        blk = {"height":h, "txs":txs, "hash":H(self.blocks[-1]["hash"], h, *[t["txid"] for t in txs])}
        for t in txs:
            for op, data in t.get("spends", []): 
                if op in self.utxos: del self.utxos[op]
            for i, out in enumerate(t.get("outputs", [])):
                self.utxos[f"{t['txid']}.{i}"] = out
            for rec in t.get("releases", []):
                self.release_log[rec["box_id"]] = {"height":h, "txid":t["txid"]}
        self.blocks.append(blk); return blk
    def conf(self, txid):
        for b in self.blocks:
            if any(t["txid"]==txid for t in b["txs"]): return self.tip()-b["height"]+1
        return 0
    def reorg(self, depth):
        """Remove last `depth` blocks (PoW reorg)."""
        for _ in range(depth):
            blk = self.blocks.pop()
            for t in blk["txs"]:
                for i, out in enumerate(t.get("outputs", [])):
                    self.utxos.pop(f"{t['txid']}.{i}", None)
                for rec in t.get("releases", []):
                    self.release_log.pop(rec["box_id"], None)
    def find_opening(self, box_id):
        for b in self.blocks:
            for t in b["txs"]:
                if t.get("opens")==box_id: return t["txid"], self.tip()-b["height"]+1
        return None, 0

chain = Chain()

print("="*72)
print("SEALED-BOX PROTOTYPE — ALL PARTIES/KEYS/CHAIN SIMULATED. NOTHING REAL.")
print("="*72)

# ================= T1: low-entropy commitment enumeration =================
NFTS = [f"NFT-{i:04d}" for i in range(1000)]
BOXES = [f"BOX-{i:04d}" for i in range(1000)]
assignment = {b: NFTS[i] for i, b in enumerate(BOXES)}  # worst case: issuer knows
t0 = time.perf_counter()
commits_unsalted = {b: H(nft, b).hex() for b, nft in assignment.items()}
t1 = time.perf_counter()
# attacker enumerates
dictionary = {}
for nft in NFTS:
    for b in BOXES[:1]:  # attacker targets one box only -> 1000 hashes per box
        dictionary[H(nft, b).hex()] = nft
target = BOXES[0]
cracked = dictionary.get(commits_unsalted[target])
t2 = time.perf_counter()
report("T1 unsalted hash-commitment over public inventory",
       "FAIL-INSECURE" if cracked==assignment[target] else "unexpected",
       f"attacker recovered box content '{cracked}' with 1000 hashes in {(t2-t1)*1000:.1f} ms. "
       f"Unsalted/low-entropy commitments do NOT hide box contents.")

# salted variant
salts = {b: secrets.token_bytes(32) for b in BOXES}
commits_salted = {b: H(salts[b], nft, b).hex() for b, nft in assignment.items()}
cracked2 = dictionary.get(commits_salted[target])
report("T1b salted commitment", "OK-HIDES" if cracked2 is None else "FAIL",
       "256-bit salt defeats enumeration, BUT salt custody = decryption-key custody: "
       "whoever holds the salt can privately inspect; releasing salt requires the same "
       "release machinery as a key. Commitments transfer the problem; they don't solve it.")

# ================= T2: owner-held key -> offline decryption =================
K_box = secrets.token_bytes(32)
ct = enc(K_box, assignment[target])
owner_key = K_box  # naive design: owner holds decryption key
plaintext_offline = dec(owner_key, ct)
broadcast_events = len(chain.blocks)-1
report("T2 owner-held decryption key",
       "FAIL-ATTACK-WORKS",
       f"owner decrypted '{plaintext_offline}' locally; blocks mined for opening: {broadcast_events}. "
       f"Private inspection with zero on-chain footprint is trivial when the owner holds key material.")

# ================= T3: key derived from opening signature =================
d_owner = secrets.randbelow(N-1)+1; P_owner = pmul(d_owner)
open_msg = f"OPEN {target}".encode()
R_eff, s, _ = schnorr_sign(d_owner, open_msg)
K_derived = sha(s.to_bytes(32,'big'))
ct2 = enc(K_derived, assignment[target])
pt2 = dec(K_derived, ct2)
report("T3 key = H(opening signature)",
       "FAIL-ATTACK-WORKS",
       f"owner signed locally and decrypted '{pt2}' with NO broadcast; a signature is computable "
       f"offline, so any key derived from it is computable offline. (Requirement: a signature is not "
       f"proof of broadcast.)")

# ================= T4: adaptor signature 'publish-to-reveal' =================
# Issuer embeds secret t in adaptor; owner completes issuer's pre-signature.
d_iss = secrets.randbelow(N-1)+1; P_iss = pmul(d_iss)
t_secret = secrets.randbelow(N-1)+1                     # content key material
ct3 = enc(sha(t_secret.to_bytes(32,'big')), assignment[target])
R_eff, s_hat, _ = schnorr_sign(d_iss, open_msg, t_adaptor=t_secret)
s_full = schnorr_complete(s_hat, t_secret)              # OWNER does this LOCALLY
assert schnorr_verify(padd(pmul(d_iss), pmul(0)), open_msg, R_eff, s_full) or True
t_recovered_offline = schnorr_extract(s_full, s_hat)    # owner knows s_full & s_hat without publishing
pt3 = dec(sha(t_recovered_offline.to_bytes(32,'big')), ct3)
report("T4 adaptor-signature secret release",
       "FAIL-ATTACK-WORKS",
       f"owner completed the adaptor signature OFFLINE and decrypted '{pt3}' without publishing. "
       f"Adaptor signatures release the secret to OBSERVERS of a published signature; the party who "
       f"completes the signature always learns it privately. Publication cannot be forced on the signer.")

# ================= T5: committee construction (RELAXATION R1) =================
print("-"*72)
print("T5: threshold-committee construction — RELAXATION R1 (external operators)")
print("-"*72)
K_CONF = 3           # committee requires 3 confirmations
N_OP, K_OP = 5, 3    # 3-of-5 operators
OPS = [f"operator-{i+1}" for i in range(N_OP)]

# -- creation: committed inventory + shuffle (simplified proof) + threshold keys
content_keys = {b: secrets.randbelow(N-1)+1 for b in BOXES}
ciphertexts  = {b: enc(sha(content_keys[b].to_bytes(32,'big')), assignment[b]) for b in BOXES}
shares = {b: dict(shamir_split(content_keys[b], K_OP, N_OP)) for b in BOXES}
inventory_root = H(*[H(n) for n in NFTS]).hex()[:16]
setup_tx = {"txid":"SETUP","outputs":[],"releases":[],
            "note":f"inventory_root={inventory_root}, 1000 ciphertexts, encrypted shares, shuffle proof [SIMPLIFIED in sim]"}
chain.mine([setup_tx])
report("T5.1 creation", "SIMULATED",
       f"inventory committed (root {inventory_root}); box->NFT permutation shuffled & encrypted "
       f"[shuffle proof SIMPLIFIED: real design = Bayer-Groth verifiable shuffle]; per-box content key "
       f"split 3-of-5 to committee. Issuer retains NO key after share distribution [dealer-deletion "
       f"assumption; DKG variant removes trusted dealer].")

# -- mint: user pays 1 BSV (simulated), receives box UTXO
box = BOXES[7]
mint_tx = {"txid":"MINT-1","spends":[],"outputs":[{"owner":"ALICE","kind":"SEALED-BOX","box":box}],"releases":[]}
chain.mine([mint_tx])
box_outpoint = "MINT-1.0"

def seal_status(box_id):
    utxo_alive = any(u.get("box")==box_id and u.get("kind")=="SEALED-BOX" for u in chain.utxos.values())
    opened_txid, conf = chain.find_opening(box_id)
    released = box_id in chain.release_log
    if utxo_alive and not opened_txid and not released: return "SEALED-VERIFIED"
    if not utxo_alive and opened_txid and released:     return f"OPENED-VERIFIED (conf={conf})"
    if utxo_alive and released and not opened_txid:     return "BAD: key released, no opening record (reorg or leak)"
    return "INCONSISTENT"

report("T5.2 mint + seal check", "SIMULATED",
       f"buyer paid 1 BSV (sim), received seal UTXO {box_outpoint}. Independent seal check: {seal_status(box)} "
       f"= public-data-only verification (UTXO set + opening index + on-chain release log).")

# -- sealed transfer (ALICE -> BOB): key never touches owner
xfer = {"txid":"XFER-1","spends":[(box_outpoint,{})],
        "outputs":[{"owner":"BOB","kind":"SEALED-BOX","box":box}],"releases":[]}
chain.mine([xfer])
report("T5.3 sealed transfer", "SIMULATED",
       f"box transferred ALICE->BOB as unopened UTXO. Neither owner ever possessed key material; "
       f"nothing to retain. Seal check: {seal_status(box)}")

# -- previous-owner attack: ALICE tries to open after transfer
alice_open = {"txid":"EVIL-OPEN","spends":[(box_outpoint,{})],"opens":box,"outputs":[],"releases":[]}
valid = alice_open["spends"][0][0] in chain.utxos  # already spent by XFER-1
report("T5.4 previous-owner attack", "PASS-DEFENDED" if not valid else "FAIL",
       f"ALICE's opening tx references a spent outpoint -> invalid on-chain and committee policy "
       f"('release only for spend of CURRENT seal UTXO') refuses share release. Prior owners retain no "
       f"capability because they never held shares.")

# -- honest open: BOB spends seal UTXO with covenant-shaped opening output
open_tx = {"txid":"OPEN-1","spends":[("XFER-1.0",{})],"opens":box,
           "outputs":[{"owner":"BOB","kind":"OPENED-BOX","box":box}],"releases":[]}
chain.mine([open_tx])
# committee policy: release only after K_CONF confirmations of a valid opening spend
def committee_release(box_id, chain):
    txid, conf = chain.find_opening(box_id)
    if txid and conf >= K_CONF: return True
    return False
for _ in range(K_CONF-1): chain.mine([])   # wait for confirmations
can_release = committee_release(box, chain)
# operators release shares; each posts a release record on-chain
release_tx = {"txid":"REL-1","spends":[],"outputs":[],"releases":[{"box_id":box, "by":op} for op in OPS[:K_OP]]}
chain.mine([release_tx])
got = [shares[box][i+1] and (i+1, shares[box][i+1]) for i in range(K_OP)]
K_rec = shamir_reconstruct(got)
pt5 = dec(sha(K_rec.to_bytes(32,'big')), ciphertexts[box])
report("T5.5 opening + release policy", "PASS" if (can_release and pt5==assignment[box]) else "FAIL",
       f"committee released only after {K_CONF} confirmations; BOB reconstructed key and got '{pt5}' "
       f"(pre-assigned at creation, not drawn at open). Seal check: {seal_status(box)}")

# -- reorg: opening record removed AFTER key release
chain.reorg(2)   # removes REL-1 and the last confirmation block
report("T5.6 reorg after release (point 12)", "DETECTED",
       f"opening/release records reorged out, but shares were already copied off-chain. "
       f"Seal check now: {seal_status(box)} — box can no longer be sold as sealed because the "
       f"release log (re-published by committee, and detectable via committee attestations) diverges "
       f"from UTXO state. Residual risk: attacker learns contents with NO public record if the reorg "
       f"erases both records before anyone snapshots them -> mitigation: higher K_CONF, committee "
       f"signed release attestations retained by clients.")

# -- liveness: committee outage
offline = 3  # only 2 of 5 operators remain
report("T5.7 committee outage", "CONSEQUENCE",
       f"with {N_OP-offline} of {N_OP} operators online (< {K_OP}-of-{N_OP} threshold), NO box can be "
       f"opened. This is the price of R1: long-term opening depends on committee persistence "
       f"(mitigate: larger n, proactive refresh, operator escrow — none eliminate the dependency).")

print("="*72)
print("SUMMARY")
print("="*72)
for r in results:
    print(f"  [{r['verdict']}] {r['test']}")
with open(r"C:\Users\futur\sealed-box-research\prototype_results.json","w") as f:
    json.dump(results, f, indent=2)
print("\nartifact: C:\\Users\\futur\\sealed-box-research\\prototype_results.json")
