package v2bls

import (
	"bytes"
	"encoding/json"
	bls12381 "github.com/drand/kyber-bls12381"
	"github.com/drand/kyber/share"
	"github.com/drand/kyber/sign/tbls"
	"testing"
)

func TestThreeOfThreeRealDKGIBE(t *testing.T) {
	pub, secrets, err := RunDefaultDKG()
	if err != nil {
		t.Fatal(err)
	}
	if pub.N != 3 || pub.Threshold != 3 || len(pub.Commitments) != 3 {
		t.Fatal("not 3-of-3")
	}
	box := bytes.Repeat([]byte{0xa3}, 32)
	id, err := Identity(box)
	if err != nil || !bytes.Equal(id, append([]byte("VAULT2:"), box...)) {
		t.Fatal("identity must be prefix plus raw bytes")
	}
	nft := []byte(`{"nft":"NFT-#000-preassigned","metadata":"exact bytes, not a stand-in, longer than 32 bytes"}`)
	c, err := Encrypt(pub, box, nft)
	if err != nil {
		t.Fatal(err)
	}
	var releases []ReleaseShare
	for _, secret := range secrets {
		// JSON is the process boundary; never write or print these private bytes.
		raw, e := json.Marshal(secret)
		if e != nil {
			t.Fatal(e)
		}
		var restored SecretShare
		if e = json.Unmarshal(raw, &restored); e != nil {
			t.Fatal(e)
		}
		r, e := Release(pub, restored, box)
		if e != nil {
			t.Fatal(e)
		}
		if len(r.Value) != 48 {
			t.Fatal("release must be a compressed G1 point")
		}
		if e = VerifyShare(pub, box, r); e != nil {
			t.Fatal(e)
		}
		releases = append(releases, r)
	}
	pbytes, _ := json.Marshal(pub)
	var p2 Public
	if err = json.Unmarshal(pbytes, &p2); err != nil {
		t.Fatal(err)
	}
	cbytes, _ := json.Marshal(c)
	var c2 Ciphertext
	if err = json.Unmarshal(cbytes, &c2); err != nil {
		t.Fatal(err)
	}
	key, err := Recover(p2, box, releases)
	if err != nil {
		t.Fatal(err)
	}
	plain, err := Decrypt(p2, box, key, c2)
	if err != nil || !bytes.Equal(plain, nft) {
		t.Fatal("exact NFT not recovered", err)
	}
	for omitted := 0; omitted < 3; omitted++ {
		t.Run(string(rune('A'+omitted))+"_missing", func(t *testing.T) {
			pair := append([]ReleaseShare(nil), releases[:omitted]...)
			pair = append(pair, releases[omitted+1:]...)
			if _, e := Recover(pub, box, pair); e == nil {
				t.Fatal("two shares accepted")
			}
			// Bypass our threshold guard AND the library's t=3 guard: interpolate
			// the two actual G1 points with t=2. This must not yield the IBE key.
			suite := bls12381.NewBLS12381Suite()
			points := make([]*share.PubShare, 0, 2)
			for _, r := range pair {
				p := suite.G1().Point()
				if e := p.UnmarshalBinary(r.Value); e != nil {
					t.Fatal(e)
				}
				points = append(points, &share.PubShare{I: r.Index, V: p})
			}
			raw, e := share.RecoverCommit(suite.G1(), points, 2, 3)
			if e != nil {
				t.Fatal(e)
			}
			rawKey, e := raw.MarshalBinary()
			if e != nil {
				t.Fatal(e)
			}
			if bytes.Equal(rawKey, key) {
				t.Fatal("raw two-point interpolation recovered key")
			}
			if _, e = Decrypt(pub, box, rawKey, *c); e == nil {
				t.Fatal("raw two-point interpolation decrypted")
			}
			// Direct IBE attempt, bypassing our recovered-key verification as well.
			if _, e = decryptUnchecked(rawKey, *c); e == nil {
				t.Fatal("IBE accepted raw two-point key")
			}
			// Two scalar shares interpolated with a false threshold also fail PK check.
			priv := make([]*share.PriShare, 0, 2)
			for _, r := range pair {
				s := suite.G2().Scalar()
				if e = s.UnmarshalBinary(secrets[r.Index].Scalar); e != nil {
					t.Fatal(e)
				}
				priv = append(priv, &share.PriShare{I: r.Index, V: s})
			}
			scalar, e := share.RecoverSecret(suite.G2(), priv, 2, 3)
			if e != nil {
				t.Fatal(e)
			}
			expected := suite.G2().Point()
			if e = expected.UnmarshalBinary(pub.Commitments[0]); e != nil {
				t.Fatal(e)
			}
			if suite.G2().Point().Mul(scalar, nil).Equal(expected) {
				t.Fatal("two scalar shares recovered master")
			}
		})
	}
	wrong := bytes.Repeat([]byte{0xb4}, 32)
	if _, err = Decrypt(pub, wrong, key, *c); err == nil {
		t.Fatal("wrong identity accepted")
	}
	wrongReleases := make([]ReleaseShare, 0, 3)
	for _, s := range secrets {
		r, e := Release(pub, s, wrong)
		if e != nil {
			t.Fatal(e)
		}
		wrongReleases = append(wrongReleases, r)
	}
	wrongKey, e := Recover(pub, wrong, wrongReleases)
	if e != nil {
		t.Fatal(e)
	}
	if _, e = decryptUnchecked(wrongKey, *c); e == nil {
		t.Fatal("IBE decrypted with other identity key")
	}
	altered := releases[0]
	altered.Value = append([]byte(nil), altered.Value...)
	altered.Value[10] ^= 1
	if VerifyShare(pub, box, altered) == nil {
		t.Fatal("altered share verified")
	}
	if VerifyShare(pub, wrong, releases[0]) == nil {
		t.Fatal("wrong identity share verified")
	}
	for _, i := range []int{-1, 3, 65536} {
		bad := releases[0]
		bad.Index = i
		if VerifyShare(pub, box, bad) == nil {
			t.Fatal("out of range share verified")
		}
		if _, e = Recover(pub, box, []ReleaseShare{bad, releases[1], releases[2]}); e == nil {
			t.Fatal("out of range accepted")
		}
	}
	if _, e = Recover(pub, box, []ReleaseShare{releases[0], releases[0], releases[1]}); e == nil {
		t.Fatal("duplicate accepted")
	}
	suite := bls12381.NewBLS12381Suite()
	pk := suite.G2().Point()
	if e = pk.UnmarshalBinary(pub.Commitments[0]); e != nil {
		t.Fatal(e)
	}
	if e = tbls.NewThresholdSchemeOnG1(suite).VerifyRecovered(pk, id, key); e != nil {
		t.Fatal(e)
	}
}

func TestRejectMalformedInputs(t *testing.T) {
	for _, n := range []int{0, 1, 31, 33, 64} {
		if _, e := Identity(make([]byte, n)); e == nil {
			t.Fatal("invalid box ID length")
		}
	}
	for _, params := range [][2]int{{0, 0}, {3, 0}, {3, 4}, {257, 3}} {
		if _, _, e := RunDKG(params[0], params[1]); e == nil {
			t.Fatal("bad committee accepted")
		}
	}
}
