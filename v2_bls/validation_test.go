package v2bls

import (
	"bytes"
	bls12381 "github.com/drand/kyber-bls12381"
	"testing"
)

func TestTamperingAndSerializationValidation(t *testing.T) {
	pub, secrets, e := RunDefaultDKG()
	if e != nil {
		t.Fatal(e)
	}
	if e = ValidatePublic(pub); e != nil {
		t.Fatal(e)
	}
	box := bytes.Repeat([]byte{1}, 32)
	var rs []ReleaseShare
	for _, s := range secrets {
		if e = ValidateSecret(pub, s); e != nil {
			t.Fatal(e)
		}
		r, e := Release(pub, s, box)
		if e != nil {
			t.Fatal(e)
		}
		rs = append(rs, r)
	}
	forged := rs[0]
	forged.Value = rs[1].Value
	if VerifyShare(pub, box, forged) == nil {
		t.Fatal("valid curve point at wrong index passed pairing verification")
	}
	if _, e = Recover(pub, box, []ReleaseShare{forged, rs[1], rs[2]}); e == nil {
		t.Fatal("forged valid point recovered")
	}
	key, e := Recover(pub, box, rs)
	if e != nil {
		t.Fatal(e)
	}
	c, e := Encrypt(pub, box, []byte("NFT-exact"))
	if e != nil {
		t.Fatal(e)
	}
	second, e := Encrypt(pub, box, []byte("NFT-exact"))
	if e != nil {
		t.Fatal(e)
	}
	if bytes.Equal(c.U, second.U) || bytes.Equal(c.Payload, second.Payload) {
		t.Fatal("encryption not randomized")
	}
	for _, field := range []string{"u", "v", "w", "nonce", "payload", "version"} {
		t.Run(field, func(t *testing.T) {
			damaged := *c
			flip := func(b []byte) []byte { b = append([]byte(nil), b...); b[len(b)-1] ^= 1; return b }
			switch field {
			case "u":
				damaged.U = flip(c.U)
			case "v":
				damaged.V = flip(c.V)
			case "w":
				damaged.W = flip(c.W)
			case "nonce":
				damaged.Nonce = flip(c.Nonce)
			case "payload":
				damaged.Payload = flip(c.Payload)
			case "version":
				damaged.Version = 9
			}
			if _, e := Decrypt(pub, box, key, damaged); e == nil {
				t.Fatal("tampered ciphertext decrypted")
			}
		})
	}
	for _, n := range []int{0, 1, 47, 49} {
		if VerifyShare(pub, box, ReleaseShare{Index: 0, Value: make([]byte, n)}) == nil {
			t.Fatal("bad release size accepted")
		}
	}
	bad := secrets[0]
	bad.Scalar = append([]byte(nil), bad.Scalar...)
	bad.Scalar[0] ^= 1
	if ValidateSecret(pub, bad) == nil {
		t.Fatal("altered private share accepted")
	}
	bad = secrets[0]
	bad.Index = 1
	if ValidateSecret(pub, bad) == nil {
		t.Fatal("private index substitution accepted")
	}
	bad = secrets[0]
	bad.Scalar = nil
	if ValidateSecret(pub, bad) == nil {
		t.Fatal("empty secret accepted")
	}
	badPub := pub
	badPub.Threshold = 2
	if ValidatePublic(badPub) == nil {
		t.Fatal("threshold downgrade accepted")
	}
	badPub = pub
	badPub.Commitments = append([][]byte(nil), pub.Commitments...)
	identity, e := bls12381.NewBLS12381Suite().G2().Point().Null().MarshalBinary()
	if e != nil {
		t.Fatal(e)
	}
	badPub.Commitments[2] = identity
	if ValidatePublic(badPub) == nil {
		t.Fatal("degenerate highest coefficient accepted")
	}
	other, _, e := RunDefaultDKG()
	if e != nil {
		t.Fatal(e)
	}
	if bytes.Equal(other.Commitments[0], pub.Commitments[0]) {
		t.Fatal("DKG reused master public key")
	}
	if ValidateSecret(other, secrets[0]) == nil {
		t.Fatal("cross-setup secret accepted")
	}
	if _, e = Decrypt(other, box, key, *c); e == nil {
		t.Fatal("cross-setup key accepted")
	}
}
