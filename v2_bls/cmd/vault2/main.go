// vault2 is an offline cryptographic CLI. Release does NOT check chain policy.
package main

import (
	"bytes"
	"crypto/ed25519"
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"io"
	"os"
	"path/filepath"
	v2 "vault.local/v2_bls"
)

type setupPublic struct {
	Public    v2.Public `json:"public"`
	Operators []string  `json:"operators"` // zero-indexed Ed25519 public keys, hex
}
type operatorFile struct {
	Setup              setupPublic    `json:"setup"`
	Share              v2.SecretShare `json:"share"`
	AttributionPrivate []byte         `json:"attribution_private"` // base64, SECRET
}
type releaseRecord struct {
	BoxID         string `json:"box_id"`
	OperatorIndex int    `json:"operator_idx"`
	Share         string `json:"ibe_key_share"`
	Signature     string `json:"operator_sig"`
}

const maxInput = 16 << 20

func decode(r io.Reader, v any) error {
	raw, err := io.ReadAll(io.LimitReader(r, 2*maxInput+1))
	if err != nil || len(raw) > 2*maxInput {
		return errors.New("JSON input exceeds 32 MiB limit or cannot be read")
	}
	d := json.NewDecoder(bytes.NewReader(raw))
	d.DisallowUnknownFields()
	if e := d.Decode(v); e != nil {
		return errors.New("invalid JSON input")
	}
	var extra any
	if e := d.Decode(&extra); e != io.EOF {
		return errors.New("trailing JSON input")
	}
	return nil
}
func readJSON(path string, v any) error {
	f, e := os.Open(path)
	if e != nil {
		return errors.New("cannot open input file")
	}
	defer f.Close()
	return decode(f, v)
}
func parseHex(s string, n int) ([]byte, error) {
	if len(s) != 2*n {
		return nil, errors.New("invalid hex length")
	}
	b, e := hex.DecodeString(s)
	if e != nil {
		return nil, errors.New("invalid hex")
	}
	return b, nil
}
func validateSetup(p setupPublic) error {
	if e := v2.ValidatePublic(p.Public); e != nil {
		return e
	}
	if len(p.Operators) != p.Public.N {
		return errors.New("operator key count mismatch")
	}
	seen := map[string]bool{}
	for _, s := range p.Operators {
		b, e := parseHex(s, ed25519.PublicKeySize)
		if e != nil {
			return e
		}
		canonical := hex.EncodeToString(b)
		if seen[canonical] {
			return errors.New("duplicate attribution key")
		}
		seen[canonical] = true
	}
	return nil
}
func attributionMessage(box []byte, index int, value []byte) []byte {
	m := append([]byte("VAULT2-REL"), box...)
	m = append(m, byte(index))
	return append(m, value...)
}
func verifyRecord(p setupPublic, r releaseRecord) (v2.ReleaseShare, error) {
	if e := validateSetup(p); e != nil {
		return v2.ReleaseShare{}, e
	}
	if r.OperatorIndex < 0 || r.OperatorIndex >= p.Public.N {
		return v2.ReleaseShare{}, errors.New("operator index out of range")
	}
	box, e := parseHex(r.BoxID, 32)
	if e != nil {
		return v2.ReleaseShare{}, e
	}
	value, e := parseHex(r.Share, 48)
	if e != nil {
		return v2.ReleaseShare{}, e
	}
	sig, e := parseHex(r.Signature, 64)
	if e != nil {
		return v2.ReleaseShare{}, e
	}
	pk, e := parseHex(p.Operators[r.OperatorIndex], 32)
	if e != nil {
		return v2.ReleaseShare{}, e
	}
	if !ed25519.Verify(pk, attributionMessage(box, r.OperatorIndex, value), sig) {
		return v2.ReleaseShare{}, errors.New("invalid operator attribution signature")
	}
	share := v2.ReleaseShare{Index: r.OperatorIndex, Value: value}
	if e = v2.VerifyShare(p.Public, box, share); e != nil {
		return v2.ReleaseShare{}, e
	}
	return share, nil
}
func writeNew(path string, v any, mode os.FileMode) error {
	f, e := os.OpenFile(path, os.O_WRONLY|os.O_CREATE|os.O_EXCL, mode)
	if e != nil {
		return errors.New("refusing to overwrite or unable to create setup file")
	}
	e = json.NewEncoder(f).Encode(v)
	closeErr := f.Close()
	if e != nil {
		return e
	}
	return closeErr
}
func run(args []string, in io.Reader, out io.Writer) error {
	if len(args) == 0 {
		return errors.New("usage: vault2 setup|encrypt|release|verify|decrypt")
	}
	flags := flag.NewFlagSet(args[0], flag.ContinueOnError)
	flags.SetOutput(io.Discard)
	dir := flags.String("dir", "", "new setup directory")
	pubPath := flags.String("public", "", "public.json")
	operator := flags.String("operator", "", "operator-N.json")
	boxHex := flags.String("box", "", "32-byte hex box id")
	cipherPath := flags.String("cipher", "", "ciphertext JSON file")
	releasesPath := flags.String("releases", "", "release record JSON array file")
	if e := flags.Parse(args[1:]); e != nil {
		return errors.New("invalid command flags")
	}
	if flags.NArg() != 0 {
		return errors.New("unexpected positional arguments")
	}
	if args[0] == "setup" {
		if *dir == "" {
			return errors.New("setup requires -dir")
		}
		// Require a new directory: never mix a failed/new setup with old key files.
		if e := os.Mkdir(*dir, 0700); e != nil {
			return errors.New("setup directory must not already exist; parent must exist")
		}
		pub, secrets, e := v2.RunDefaultDKG()
		if e != nil {
			return e
		}
		p := setupPublic{Public: pub}
		private := make([]ed25519.PrivateKey, pub.N)
		for i := range private {
			pk, sk, e := ed25519.GenerateKey(rand.Reader)
			if e != nil {
				return e
			}
			private[i] = sk
			p.Operators = append(p.Operators, hex.EncodeToString(pk))
		}
		for i, s := range secrets {
			if e = writeNew(filepath.Join(*dir, fmt.Sprintf("operator-%d.json", i)), operatorFile{Setup: p, Share: s, AttributionPrivate: private[i]}, 0600); e != nil {
				return e
			}
		}
		if e = writeNew(filepath.Join(*dir, "public.json"), p, 0644); e != nil {
			return e
		}
		return json.NewEncoder(out).Encode(map[string]any{"ok": true, "n": 3, "threshold": 3, "dkg_process_isolated": false})
	}
	if args[0] == "release" {
		var o operatorFile
		if e := readJSON(*operator, &o); e != nil {
			return e
		}
		if e := validateSetup(o.Setup); e != nil {
			return e
		}
		box, e := parseHex(*boxHex, 32)
		if e != nil {
			return e
		}
		r, e := v2.Release(o.Setup.Public, o.Share, box)
		if e != nil {
			return e
		}
		if len(o.AttributionPrivate) != ed25519.PrivateKeySize {
			return errors.New("invalid attribution private key length")
		}
		sk := ed25519.PrivateKey(o.AttributionPrivate)
		pk, e := parseHex(o.Setup.Operators[r.Index], 32)
		if e != nil {
			return e
		}
		derived := ed25519.NewKeyFromSeed(sk.Seed())
		if !bytes.Equal(derived, sk) || !bytes.Equal(sk.Public().(ed25519.PublicKey), pk) {
			return errors.New("attribution key mismatch")
		}
		sig := ed25519.Sign(sk, attributionMessage(box, r.Index, r.Value))
		return json.NewEncoder(out).Encode(releaseRecord{BoxID: hex.EncodeToString(box), OperatorIndex: r.Index, Share: hex.EncodeToString(r.Value), Signature: hex.EncodeToString(sig)})
	}
	var p setupPublic
	if e := readJSON(*pubPath, &p); e != nil {
		return e
	}
	if e := validateSetup(p); e != nil {
		return e
	}
	if args[0] == "verify" {
		var r releaseRecord
		if e := decode(in, &r); e != nil {
			return e
		}
		if _, e := verifyRecord(p, r); e != nil {
			return e
		}
		return json.NewEncoder(out).Encode(map[string]bool{"valid": true})
	}
	box, e := parseHex(*boxHex, 32)
	if e != nil {
		return e
	}
	switch args[0] {
	case "encrypt":
		plaintext, e := io.ReadAll(io.LimitReader(in, maxInput+1))
		if e != nil {
			return e
		}
		if len(plaintext) > maxInput {
			return errors.New("plaintext exceeds 16 MiB limit")
		}
		c, e := v2.Encrypt(p.Public, box, plaintext)
		if e != nil {
			return e
		}
		return json.NewEncoder(out).Encode(c)
	case "decrypt":
		var c v2.Ciphertext
		if e := readJSON(*cipherPath, &c); e != nil {
			return e
		}
		var records []releaseRecord
		if e := readJSON(*releasesPath, &records); e != nil {
			return e
		}
		shares := make([]v2.ReleaseShare, 0, len(records))
		for _, r := range records {
			b, e := parseHex(r.BoxID, 32)
			if e != nil || !bytes.Equal(b, box) {
				return errors.New("release belongs to another box")
			}
			s, e := verifyRecord(p, r)
			if e != nil {
				return e
			}
			shares = append(shares, s)
		}
		key, e := v2.Recover(p.Public, box, shares)
		if e != nil {
			return e
		}
		plain, e := v2.Decrypt(p.Public, box, key, c)
		if e != nil {
			return e
		}
		_, e = out.Write(plain)
		return e
	default:
		return errors.New("unknown command")
	}
}
func main() {
	if e := run(os.Args[1:], os.Stdin, os.Stdout); e != nil {
		fmt.Fprintln(os.Stderr, "vault2:", e)
		os.Exit(1)
	}
}
