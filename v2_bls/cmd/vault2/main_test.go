package main

import (
	"bytes"
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestJSONCiphertextBudget(t *testing.T) {
	// A permitted 16 MiB plaintext expands under base64 JSON encoding.
	c := struct {
		Payload []byte `json:"payload"`
	}{Payload: make([]byte, 13<<20)}
	raw, err := json.Marshal(c)
	if err != nil {
		t.Fatal(err)
	}
	var restored struct {
		Payload []byte `json:"payload"`
	}
	if err = decode(bytes.NewReader(raw), &restored); err != nil {
		t.Fatal("permitted ciphertext exceeds JSON reader budget", err)
	}
	if !bytes.Equal(restored.Payload, c.Payload) {
		t.Fatal("payload roundtrip mismatch")
	}
}

func TestCLILifecycle(t *testing.T) {
	dir := filepath.Join(t.TempDir(), "committee")
	invoke := func(input string, args ...string) ([]byte, error) {
		var out bytes.Buffer
		e := run(args, strings.NewReader(input), &out)
		return out.Bytes(), e
	}
	if _, e := invoke("", "setup", "-dir", dir); e != nil {
		t.Fatal(e)
	}
	pub := filepath.Join(dir, "public.json")
	box := strings.Repeat("ab", 32)
	nft := "NFT-#000-preassigned\x00exact\n"
	ciphertext, e := invoke(nft, "encrypt", "-public", pub, "-box", box)
	if e != nil {
		t.Fatal(e)
	}
	cfile := filepath.Join(dir, "cipher.json")
	if e = os.WriteFile(cfile, ciphertext, 0600); e != nil {
		t.Fatal(e)
	}
	var records []json.RawMessage
	for _, name := range []string{"operator-0.json", "operator-1.json", "operator-2.json"} {
		r, e := invoke("", "release", "-operator", filepath.Join(dir, name), "-box", box)
		if e != nil {
			t.Fatal(e)
		}
		if _, e = invoke(string(r), "verify", "-public", pub); e != nil {
			t.Fatal(e)
		}
		records = append(records, json.RawMessage(r))
	}
	file := filepath.Join(dir, "releases.json")
	raw, _ := json.Marshal(records)
	if e = os.WriteFile(file, raw, 0600); e != nil {
		t.Fatal(e)
	}
	result, e := invoke("", "decrypt", "-public", pub, "-box", box, "-cipher", cfile, "-releases", file)
	if e != nil || string(result) != nft {
		t.Fatal("CLI exact decrypt failed", e)
	}
	raw, _ = json.Marshal(records[:2])
	if e = os.WriteFile(file, raw, 0600); e != nil {
		t.Fatal(e)
	}
	if _, e = invoke("", "decrypt", "-public", pub, "-box", box, "-cipher", cfile, "-releases", file); e == nil {
		t.Fatal("two operators decrypted")
	}
	var altered map[string]any
	if e = json.Unmarshal(records[0], &altered); e != nil {
		t.Fatal(e)
	}
	altered["operator_sig"] = strings.Repeat("00", 64)
	raw, _ = json.Marshal(altered)
	if _, e = invoke(string(raw), "verify", "-public", pub); e == nil {
		t.Fatal("forged attribution accepted")
	}
	if _, e = invoke("", "setup", "-dir", dir); e == nil {
		t.Fatal("overwrote existing private keys")
	}
}
