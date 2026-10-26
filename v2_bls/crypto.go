// Package v2bls implements the local VAULT-0002 cryptographic prototype.
package v2bls

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/binary"
	"errors"
	"github.com/drand/kyber"
	bls12381 "github.com/drand/kyber-bls12381"
	"github.com/drand/kyber/encrypt/ibe"
	"github.com/drand/kyber/share"
	"github.com/drand/kyber/sign/tbls"
)

// Public contains G2 polynomial commitments, constant term first. All byte
// slices in this API use standard base64 under encoding/json. Pin the public
// setup; accepting attacker-selected setup material defeats share verification.
type Public struct {
	Version     int      `json:"version"`
	N           int      `json:"n"`
	Threshold   int      `json:"threshold"`
	Commitments [][]byte `json:"commitments"`
}

// SecretShare contains sensitive plaintext key material. Never log or commit it.
// Index is zero-based. JSON serialization is portable but NOT encrypted at rest;
// store one file per operator with host-appropriate access controls.
type SecretShare struct {
	Index  int    `json:"index"`
	Scalar []byte `json:"scalar"`
}

// ReleaseShare holds a zero-based index and a 48-byte compressed G1 point.
// Value excludes kyber's internal two-byte TBLS index prefix.
type ReleaseShare struct {
	Index int    `json:"index"`
	Value []byte `json:"value"`
}
type Ciphertext struct {
	Version int    `json:"version"`
	U       []byte `json:"u"`
	V       []byte `json:"v"`
	W       []byte `json:"w"`
	Nonce   []byte `json:"nonce"`
	Payload []byte `json:"payload"`
}

// Identity uses raw box bytes, NOT ASCII hex or a drand round digest.
func Identity(box []byte) ([]byte, error) {
	if len(box) != 32 {
		return nil, errors.New("box_id must be exactly 32 raw bytes")
	}
	return append([]byte("VAULT2:"), box...), nil
}
func publicPoly(pub Public) (*share.PubPoly, error) {
	if pub.Version != 1 || pub.N < 2 || pub.N > 256 || pub.Threshold < 2 || pub.Threshold > pub.N || len(pub.Commitments) != pub.Threshold {
		return nil, errors.New("invalid public setup")
	}
	suite := bls12381.NewBLS12381Suite()
	points := make([]kyber.Point, len(pub.Commitments))
	for i, b := range pub.Commitments {
		p, e := decodePoint(suite.G2(), b)
		if e != nil {
			return nil, errors.New("invalid G2 commitment")
		}
		points[i] = p
	}
	if points[0].Equal(suite.G2().Point().Null()) || points[len(points)-1].Equal(suite.G2().Point().Null()) {
		return nil, errors.New("degenerate public polynomial")
	}
	return share.NewPubPoly(suite.G2(), nil, points), nil
}
func decodePoint(group kyber.Group, b []byte) (kyber.Point, error) {
	if len(b) != group.PointLen() {
		return nil, errors.New("invalid point length")
	}
	p := group.Point()
	if e := p.UnmarshalBinary(b); e != nil {
		return nil, errors.New("invalid point encoding")
	}
	if check, ok := p.(interface{ IsInCorrectGroup() bool }); ok && !check.IsInCorrectGroup() {
		return nil, errors.New("point outside subgroup")
	}
	encoded, e := p.MarshalBinary()
	if e != nil || !bytes.Equal(encoded, b) {
		return nil, errors.New("noncanonical point")
	}
	return p, nil
}

// ValidatePublic validates serialized setup material before it is pinned/used.
func ValidatePublic(pub Public) error { _, e := publicPoly(pub); return e }
func privateShare(pub Public, s SecretShare) (*share.PriShare, error) {
	poly, e := publicPoly(pub)
	if e != nil {
		return nil, e
	}
	if s.Index < 0 || s.Index >= pub.N {
		return nil, errors.New("secret index out of range")
	}
	group := bls12381.NewBLS12381Suite().G2()
	scalar := group.Scalar()
	if len(s.Scalar) != scalar.MarshalSize() {
		return nil, errors.New("invalid scalar length")
	}
	if e = scalar.UnmarshalBinary(s.Scalar); e != nil {
		return nil, errors.New("invalid scalar")
	}
	encoded, e := scalar.MarshalBinary()
	if e != nil || !bytes.Equal(encoded, s.Scalar) {
		return nil, errors.New("noncanonical scalar")
	}
	p := &share.PriShare{I: s.Index, V: scalar}
	if !poly.Check(p) {
		return nil, errors.New("secret does not match public setup")
	}
	return p, nil
}
func ValidateSecret(pub Public, s SecretShare) error { _, e := privateShare(pub, s); return e }

// Release is a cryptographic operation only; callers MUST enforce chain policy.
func Release(pub Public, secret SecretShare, box []byte) (ReleaseShare, error) {
	id, e := Identity(box)
	if e != nil {
		return ReleaseShare{}, e
	}
	p, e := privateShare(pub, secret)
	if e != nil {
		return ReleaseShare{}, e
	}
	sig, e := tbls.NewThresholdSchemeOnG1(bls12381.NewBLS12381Suite()).Sign(p, id)
	if e != nil {
		return ReleaseShare{}, e
	}
	return ReleaseShare{Index: p.I, Value: append([]byte(nil), sig[2:]...)}, nil
}
func indexedShare(pub Public, r ReleaseShare) ([]byte, error) {
	if r.Index < 0 || r.Index >= pub.N {
		return nil, errors.New("release index out of range")
	}
	p, e := decodePoint(bls12381.NewBLS12381Suite().G1(), r.Value)
	if e != nil {
		return nil, e
	}
	if p.Equal(bls12381.NewBLS12381Suite().G1().Point().Null()) {
		return nil, errors.New("identity release point")
	}
	sig := make([]byte, 2+len(r.Value))
	binary.BigEndian.PutUint16(sig, uint16(r.Index))
	copy(sig[2:], r.Value)
	return sig, nil
}
func VerifyShare(pub Public, box []byte, r ReleaseShare) error {
	id, e := Identity(box)
	if e != nil {
		return e
	}
	poly, e := publicPoly(pub)
	if e != nil {
		return e
	}
	sig, e := indexedShare(pub, r)
	if e != nil {
		return e
	}
	if e = tbls.NewThresholdSchemeOnG1(bls12381.NewBLS12381Suite()).VerifyPartial(poly, id, sig); e != nil {
		return errors.New("release share verification failed")
	}
	return nil
}
func Recover(pub Public, box []byte, rs []ReleaseShare) ([]byte, error) {
	id, e := Identity(box)
	if e != nil {
		return nil, e
	}
	poly, e := publicPoly(pub)
	if e != nil {
		return nil, e
	}
	if len(rs) < pub.Threshold || len(rs) > pub.N {
		return nil, errors.New("insufficient or excess release shares")
	}
	seen := make(map[int]bool, len(rs))
	sigs := make([][]byte, 0, len(rs))
	for _, r := range rs {
		if seen[r.Index] {
			return nil, errors.New("duplicate release index")
		}
		seen[r.Index] = true
		if e = VerifyShare(pub, box, r); e != nil {
			return nil, e
		}
		s, e := indexedShare(pub, r)
		if e != nil {
			return nil, e
		}
		sigs = append(sigs, s)
	}
	scheme := tbls.NewThresholdSchemeOnG1(bls12381.NewBLS12381Suite())
	key, e := scheme.Recover(poly, id, sigs, pub.Threshold, pub.N)
	if e != nil {
		return nil, errors.New("key recovery failed")
	}
	if e = scheme.VerifyRecovered(poly.Commit(), id, key); e != nil {
		return nil, errors.New("recovered key verification failed")
	}
	return key, nil
}

// Encrypt uses CCA IBE to wrap a random AES-256-GCM key, supporting NFT payloads
// longer than the IBE library's 32-byte plaintext limit.
func Encrypt(pub Public, box, nft []byte) (*Ciphertext, error) {
	id, e := Identity(box)
	if e != nil {
		return nil, e
	}
	poly, e := publicPoly(pub)
	if e != nil {
		return nil, e
	}
	key := make([]byte, 32)
	if _, e = rand.Read(key); e != nil {
		return nil, e
	}
	defer clear(key)
	wrapped, e := ibe.EncryptCCAonG2(bls12381.NewBLS12381Suite(), poly.Commit(), id, key)
	if e != nil {
		return nil, errors.New("IBE encryption failed")
	}
	u, e := wrapped.U.MarshalBinary()
	if e != nil {
		return nil, e
	}
	aead, e := newAEAD(key)
	if e != nil {
		return nil, e
	}
	nonce := make([]byte, aead.NonceSize())
	if _, e = rand.Read(nonce); e != nil {
		return nil, e
	}
	return &Ciphertext{Version: 1, U: u, V: wrapped.V, W: wrapped.W, Nonce: nonce, Payload: aead.Seal(nil, nonce, nft, nil)}, nil
}
func newAEAD(key []byte) (cipher.AEAD, error) {
	b, e := aes.NewCipher(key)
	if e != nil {
		return nil, e
	}
	return cipher.NewGCM(b)
}
func Decrypt(pub Public, box, key []byte, c Ciphertext) ([]byte, error) {
	id, e := Identity(box)
	if e != nil {
		return nil, e
	}
	poly, e := publicPoly(pub)
	if e != nil {
		return nil, e
	}
	p, e := decodePoint(bls12381.NewBLS12381Suite().G1(), key)
	if e != nil {
		return nil, e
	}
	if p.Equal(bls12381.NewBLS12381Suite().G1().Point().Null()) {
		return nil, errors.New("identity key point")
	}
	if e = tbls.NewThresholdSchemeOnG1(bls12381.NewBLS12381Suite()).VerifyRecovered(poly.Commit(), id, key); e != nil {
		return nil, errors.New("key does not match box identity and setup")
	}
	return decryptUnchecked(key, c)
}
func decryptUnchecked(key []byte, c Ciphertext) ([]byte, error) {
	if c.Version != 1 || len(c.V) != 32 || len(c.W) != 32 {
		return nil, errors.New("invalid ciphertext envelope")
	}
	suite := bls12381.NewBLS12381Suite()
	private, e := decodePoint(suite.G1(), key)
	if e != nil {
		return nil, e
	}
	u, e := decodePoint(suite.G2(), c.U)
	if e != nil {
		return nil, e
	}
	wrapped, e := ibe.DecryptCCAonG2(suite, private, &ibe.Ciphertext{U: u, V: c.V, W: c.W})
	// Library's CCA failure string contains internal values: never propagate it.
	if e != nil {
		return nil, errors.New("IBE authentication failed")
	}
	defer clear(wrapped)
	if len(wrapped) != 32 {
		return nil, errors.New("invalid wrapped key length")
	}
	aead, e := newAEAD(wrapped)
	if e != nil {
		return nil, e
	}
	if len(c.Nonce) != aead.NonceSize() {
		return nil, errors.New("invalid nonce length")
	}
	plaintext, e := aead.Open(nil, c.Nonce, c.Payload, nil)
	if e != nil {
		return nil, errors.New("payload authentication failed")
	}
	return plaintext, nil
}
