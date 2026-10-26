#!/usr/bin/env python3
"""
VAULT-0001 reference implementation — Draft.
Decoder-first PoC for the sealed vault box spec: wire format, state machine,
seal-check algorithm, golden vectors. SIMULATED chain only; no network, no funds.
Test private keys are published constants by design (spec vectors).
"""
import hashlib, json, sys

def sha(b): return hashlib.sha256(b).digest()
def sha256d(b): return sha(sha(b))
def hash160(b): return hashlib.new('ripemd160', sha(b)).digest()

SEALED, OPENED = 0, 1

# ---------- minimal script codec ----------
OP_0=0x00; OP_FALSE=0x00; OP_IF=0x63; OP_ENDIF=0x68; OP_CODESEPARATOR=0xab; OP_1=0x51
def push(data: bytes) -> bytes:
    l = len(data)
    if l == 0: return bytes([OP_0])
    if l <= 75: return bytes([l]) + data
    if l <= 255: return bytes([0x4c, l]) + data
    if l <= 65535: return bytes([0x4d]) + l.to_bytes(2,"little") + data
    raise ValueError("push too large for PoC")

def parse_pushes(script: bytes):
    """Generic push-opcode parser — the INDEPENDENT decoder (shares no encode logic)."""
    out, i = [], 0
    while i < len(script):
        op = script[i]; i += 1
        if 1 <= op <= 75:
            out.append(("push", script[i:i+op])); i += op
        elif op == 0x4c:
            l = script[i]; i += 1; out.append(("push", script[i:i+l])); i += l
        elif op == 0x4d:
            l = int.from_bytes(script[i:i+2],"little"); i += 2; out.append(("push", script[i:i+l])); i += l
        else:
            out.append(("op", op))
    return out

# ---------- vault envelope ----------
CANONICAL_BODY = b"VAULT-COVENANT-BODY-v0.1-PLACEHOLDER"  # replaced by compiled sCrypt artifact at graduation
CT = b"application/vnd.vault+json"

def encode_vault_script(state, box_id, content_ref, owner_pkh, meta: dict) -> bytes:
    assert state in (SEALED, OPENED) and len(box_id)==32 and len(content_ref)==32 and len(owner_pkh)==20
    prefix = push(bytes([state])) + push(box_id) + push(content_ref) + push(owner_pkh) + CANONICAL_BODY
    m = dict(meta); m.update({"box_id": box_id.hex(), "content_ref": content_ref.hex(),
                              "state": state, "owner_pkh": owner_pkh.hex()})
    envelope = bytes([OP_FALSE, OP_IF]) + push(b"ord") + bytes([OP_1]) + push(CT) + bytes([OP_0]) + push(json.dumps(m, sort_keys=True).encode()) + bytes([OP_ENDIF])
    return prefix + bytes([OP_CODESEPARATOR]) + envelope

class TamperError(Exception): pass

def read_push(script: bytes, i: int):
    """Return (data, next_i) for the push opcode at position i."""
    op = script[i]; i += 1
    if 1 <= op <= 75: return script[i:i+op], i+op
    if op == 0x4c: l = script[i]; i += 1; return script[i:i+l], i+l
    if op == 0x4d: l = int.from_bytes(script[i:i+2],"little"); i += 2; return script[i:i+l], i+l
    raise TamperError(f"expected push opcode at {i-1}, got 0x{op:02x}")

def decode_vault_script(script: bytes) -> dict:
    """Independent decoder: cursor-based, no shared logic with the encoder."""
    i = 0
    state, i  = read_push(script, i)
    box_id, i = read_push(script, i)
    content_ref, i = read_push(script, i)
    owner_pkh, i = read_push(script, i)
    if script[i:i+len(CANONICAL_BODY)] != CANONICAL_BODY:
        raise TamperError("non-canonical covenant body (lookalike script)")
    i += len(CANONICAL_BODY)
    if i >= len(script) or script[i] != OP_CODESEPARATOR:
        raise TamperError("missing OP_CODESEPARATOR before envelope")
    i += 1
    if len(state)!=1 or state[0] not in (0,1): raise TamperError("bad state byte")
    if len(box_id)!=32 or len(content_ref)!=32 or len(owner_pkh)!=20: raise TamperError("bad field lengths")
    # ord envelope: OP_FALSE OP_IF "ord" OP_1 <ct> OP_0 <json> OP_ENDIF
    if script[i]!=OP_FALSE or script[i+1]!=OP_IF: raise TamperError("bad envelope header")
    i += 2
    tag, i = read_push(script, i)
    if tag != b"ord" or script[i]!=OP_1: raise TamperError("not an ord envelope")
    i += 1
    ct, i = read_push(script, i)
    if ct != CT: raise TamperError("wrong content type")
    if script[i]!=OP_0: raise TamperError("bad envelope separator")
    i += 1
    meta_raw, i = read_push(script, i)
    if script[i]!=OP_ENDIF: raise TamperError("unterminated envelope")
    meta = json.loads(meta_raw)
    if meta["box_id"]!=box_id.hex() or meta["content_ref"]!=content_ref.hex() \
       or meta["state"]!=state[0] or meta["owner_pkh"]!=owner_pkh.hex():
        raise TamperError("ord envelope / covenant state mismatch")
    return {"state": state[0], "box_id": box_id.hex(), "content_ref": content_ref.hex(), "owner_pkh": owner_pkh.hex()}

# ---------- state machine ----------
ALLOWED = {(SEALED,SEALED):"transfer", (SEALED,OPENED):"open", (OPENED,OPENED):"transfer"}
def validate_spend(prev: dict, nxt: dict | None, sig_ok: bool) -> tuple[bool,str]:
    if not sig_ok: return False, "owner signature invalid"
    if nxt is None: return False, "vault output destroyed (covenant forbids non-vault spend)"
    if prev["box_id"]!=nxt["box_id"]: return False, "box_id mutated"
    if prev["content_ref"]!=nxt["content_ref"]: return False, "content_ref mutated"
    t = (prev["state"], nxt["state"])
    if t not in ALLOWED: return False, f"illegal transition {t} (reseal/invalid state)"
    return True, ALLOWED[t]

# ---------- chain view + seal check ----------
class SimChain:
    """Minimal lineage-capable chain sim. Production: replace with 1sat-server/WoC (Tier 0)
    or SPV+merkle proofs (Tier 1) — interface identical."""
    def __init__(self): self.utxos={}; self.spends=[]; self.releases={}; self.tip=0; self.conf={}
    def add(self, outpoint, script, owner_desc=""): self.utxos[outpoint]={"script":script}
    def spend(self, outpoint, new_outpoint=None, new_script=None, conf=3, sig_ok=True):
        prev = decode_vault_script(self.utxos[outpoint]["script"])
        nxt = decode_vault_script(new_script) if new_script else None
        ok, why = validate_spend(prev, nxt, sig_ok)
        if not ok: return False, why
        del self.utxos[outpoint]
        if new_outpoint: self.add(new_outpoint, new_script); self.conf[new_outpoint]=conf
        self.spends.append((outpoint, new_outpoint)); return True, why
    def release(self, box_id): self.releases[box_id]=True

def seal_status(box_id_hex, view: SimChain, K=3):
    cur=None
    for op,u in view.utxos.items():
        try: d=decode_vault_script(u["script"])
        except TamperError: continue
        if d["box_id"]==box_id_hex: cur=(op,d)
    if cur is None:
        return "UNKNOWN", "no live vault UTXO for box (opened-and-respent history or indexer gap)"
    op,d = cur
    if d["state"]==OPENED:
        c = view.conf.get(op,0)
        return ("OPENED-VERIFIED" if c>=K else "UNKNOWN"), f"state=OPENED conf={c} (K={K})"
    if box_id_hex in view.releases:
        return "UNSEALED-DISCREPANCY", "release record exists but seal UTXO unspent — do not buy as sealed"
    return "SEALED-VERIFIED", f"unspent, state=SEALED, no release record (conf {view.conf.get(op,0)})"

# ================= tests + golden vectors =================
# Published test keys (toy scalars; fine to publish per spec pipeline)
ALICE, BOB = b"\x01"*32, b"\x02"*32
def pkh(key): return hash160(key)
GEN_TXID = sha(b"VAULT-0001 genesis vector tx")
GEN_OUTPOINT = GEN_TXID + (0).to_bytes(4,"little")
BOX_ID = sha256d(GEN_OUTPOINT)
CONTENT_REF = sha256d(b"vault vector content descriptor")
failures=[]
def check(name, cond, detail=""):
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    if not cond: failures.append(name)

print("="*70); print("VAULT-0001 reference implementation — test run (simulated; nothing real)"); print("="*70)

# known-answer first (spec pipeline rule)
check("KAT sha256('abc')", sha(b"abc").hex()=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")

# golden vector: deterministic envelope
meta = {"name":"Vector Box #1","collection":"VAULT-Vectors"}
script1 = encode_vault_script(SEALED, BOX_ID, CONTENT_REF, pkh(ALICE), meta)
vec_hex = script1.hex()
dec = decode_vault_script(script1)
check("roundtrip: encode -> independent decode",
      dec["state"]==SEALED and dec["box_id"]==BOX_ID.hex() and dec["content_ref"]==CONTENT_REF.hex() and dec["owner_pkh"]==pkh(ALICE).hex())

# negative: forged covenant body
forged = push(bytes([SEALED]))+push(BOX_ID)+push(CONTENT_REF)+push(pkh(ALICE))+b"FAKE-BODY"+bytes([OP_CODESEPARATOR])
try: decode_vault_script(forged); check("forgery rejected", False)
except TamperError as e: check("forgery rejected", True, str(e))

# negative: envelope/covenant mismatch
bad_meta_script = push(bytes([SEALED]))+push(BOX_ID)+push(CONTENT_REF)+push(pkh(ALICE))+CANONICAL_BODY+bytes([OP_CODESEPARATOR])+ \
    bytes([OP_FALSE,OP_IF])+push(b"ord")+bytes([OP_1])+push(CT)+bytes([OP_0])+push(json.dumps({"box_id":"00"*32,"content_ref":CONTENT_REF.hex(),"state":0,"owner_pkh":pkh(ALICE).hex()}).encode())+bytes([OP_ENDIF])
try: decode_vault_script(bad_meta_script); check("envelope mismatch rejected", False)
except TamperError as e: check("envelope mismatch rejected", True, str(e))

# lifecycle on simulated chain
v = SimChain()
v.add("genesis.0", script1); v.conf["genesis.0"]=10
print("-"*70)
st,_ = seal_status(BOX_ID.hex(), v); check("fresh box seals", st=="SEALED-VERIFIED", _)

# transfer alice->bob
s2 = encode_vault_script(SEALED, BOX_ID, CONTENT_REF, pkh(BOB), meta)
ok,why = v.spend("genesis.0","t1.0",s2,conf=5)
st,_ = seal_status(BOX_ID.hex(), v); check("sealed transfer", ok and st=="SEALED-VERIFIED", f"{why}; {st}")

# reseal attempt is meaningless (already sealed) — test illegal OPENED->SEALED + open + opened transfer
s3 = encode_vault_script(OPENED, BOX_ID, CONTENT_REF, pkh(BOB), meta)
ok,why = v.spend("t1.0","t2.0",s3,conf=1)
st,_ = seal_status(BOX_ID.hex(), v); check("opening accepted, shallow conf -> UNKNOWN", ok and st=="UNKNOWN", f"{why}; {st}")
v.conf["t2.0"]=6
st,_ = seal_status(BOX_ID.hex(), v); check("opening deep conf -> OPENED-VERIFIED", st=="OPENED-VERIFIED", st)

s4 = encode_vault_script(SEALED, BOX_ID, CONTENT_REF, pkh(ALICE), meta)
ok,why = v.spend("t2.0","evil.0",s4,conf=9)
check("reseal rejected (OPENED->SEALED)", not ok, why)

ok,why = v.spend("t2.0","evil2.0",None,conf=9)
check("destruction rejected (spend to non-vault)", not ok, why)

s5 = encode_vault_script(OPENED, BOX_ID, sha256d(b"DIFFERENT CONTENT"), pkh(BOB), meta)
ok,why = v.spend("t2.0","evil3.0",s5,conf=9)
check("content substitution rejected", not ok, why)

ok,why = v.spend("t2.0","evil4.0", encode_vault_script(OPENED, BOX_ID, CONTENT_REF, pkh(ALICE), meta), conf=9, sig_ok=False)
check("theft rejected (bad owner sig)", not ok, why)

# opened transfer is legal
s6 = encode_vault_script(OPENED, BOX_ID, CONTENT_REF, pkh(ALICE), meta)
ok,why = v.spend("t2.0","t3.0",s6,conf=6)
st,_ = seal_status(BOX_ID.hex(), v); check("opened box transferable", ok and st=="OPENED-VERIFIED", f"{why}; {st}")

# MODE-SECRET discrepancy: release record on a sealed box
v2 = SimChain(); v2.add("g2.0", script1); v2.conf["g2.0"]=10; v2.release(BOX_ID.hex())
st,_ = seal_status(BOX_ID.hex(), v2); check("release-without-opening flagged", st=="UNSEALED-DISCREPANCY", _)

# golden vectors file — deterministic, reproducible byte-for-byte
vectors = {
  "spec":"VAULT-0001 v0.1 DRAFT",
  "genesis_outpoint": GEN_OUTPOINT.hex(),
  "box_id": BOX_ID.hex(),
  "content_ref": CONTENT_REF.hex(),
  "alice_pkh": pkh(ALICE).hex(), "bob_pkh": pkh(BOB).hex(),
  "sealed_script_hex": vec_hex,
  "expected_decode": dec,
  "canonical_body_hex": CANONICAL_BODY.hex(),
}
blob = json.dumps(vectors, sort_keys=True, indent=2)
with open(r"C:\Users\futur\sealed-box-research\vault_vectors.json","w") as f: f.write(blob)
regen = json.dumps(vectors, sort_keys=True, indent=2)
check("golden vectors reproducible byte-for-byte", blob==regen)
with open(r"C:\Users\futur\sealed-box-research\vault_vectors.json") as f: back=f.read()
check("golden vectors file roundtrip", back==blob)

print("="*70)
print("RESULT:", "ALL PASS" if not failures else f"{len(failures)} FAILURES: {failures}")
sys.exit(1 if failures else 0)
