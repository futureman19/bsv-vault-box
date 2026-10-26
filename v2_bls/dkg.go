package v2bls

import (
	"errors"
	"github.com/drand/kyber"
	bls12381 "github.com/drand/kyber-bls12381"
	"github.com/drand/kyber/share/dkg"
	"github.com/drand/kyber/sign/schnorr"
)

// RunDefaultDKG deliberately uses 3-of-3. Losing one operator prevents release.
func RunDefaultDKG() (Public, []SecretShare, error) { return RunDKG(3, 3) }

// RunDKG orchestrates drand's Pedersen-style DKG in one process: every node
// independently generates a polynomial, exchanges ECIES-encrypted deals and
// authenticated responses, and verifies its resulting share. No trusted dealer
// or reconstructed master scalar is used. This is NOT process-isolated DKG.
// It fails closed on complaints/evictions instead of implementing retries.
func RunDKG(n, k int) (Public, []SecretShare, error) {
	if n < 2 || n > 256 || k < 2 || k > n {
		return Public{}, nil, errors.New("require 2 <= threshold <= n <= 256")
	}
	suite := bls12381.NewBLS12381Suite()
	group := suite.G2().(dkg.Suite)
	nodes := make([]dkg.Node, n)
	long := make([]kyber.Scalar, n)
	for i := range nodes {
		long[i] = group.Scalar().Pick(group.RandomStream())
		nodes[i] = dkg.Node{Index: uint32(i), Public: group.Point().Mul(long[i], nil)}
	}
	cfg := dkg.Config{Suite: group, NewNodes: nodes, Threshold: k, Nonce: dkg.GetNonce(), Auth: schnorr.NewScheme(group), FastSync: true}
	handlers := make([]*dkg.DistKeyGenerator, n)
	deals := make([]*dkg.DealBundle, 0, n)
	for i := range handlers {
		local := cfg
		local.Longterm = long[i]
		h, e := dkg.NewDistKeyHandler(&local)
		if e != nil {
			return Public{}, nil, e
		}
		handlers[i] = h
		deal, e := h.Deals()
		if e != nil {
			return Public{}, nil, e
		}
		if deal == nil {
			return Public{}, nil, errors.New("missing DKG deal")
		}
		if e = dkg.VerifyPacketSignature(&cfg, deal); e != nil {
			return Public{}, nil, errors.New("DKG deal authentication failed")
		}
		deals = append(deals, deal)
	}
	responses := make([]*dkg.ResponseBundle, 0, n)
	for _, h := range handlers {
		r, e := h.ProcessDeals(deals)
		if e != nil {
			return Public{}, nil, errors.New("DKG deal processing failed")
		}
		if r != nil {
			if e = dkg.VerifyPacketSignature(&cfg, r); e != nil {
				return Public{}, nil, errors.New("DKG response authentication failed")
			}
			responses = append(responses, r)
		}
	}
	pub := Public{Version: 1, N: n, Threshold: k}
	secrets := make([]SecretShare, n)
	var first *dkg.Result
	for i, h := range handlers {
		result, just, e := h.ProcessResponses(responses)
		if e != nil || just != nil || result == nil || len(result.QUAL) != n {
			return Public{}, nil, errors.New("DKG did not finish with all participants")
		}
		if first == nil {
			first = result
			for _, p := range result.Key.Commitments() {
				b, e := p.MarshalBinary()
				if e != nil {
					return Public{}, nil, e
				}
				pub.Commitments = append(pub.Commitments, b)
			}
		} else if !first.PublicEqual(result) {
			return Public{}, nil, errors.New("inconsistent DKG public results")
		}
		s := result.Key.PriShare()
		if s.I != i {
			return Public{}, nil, errors.New("unexpected DKG index")
		}
		b, e := s.V.MarshalBinary()
		if e != nil {
			return Public{}, nil, e
		}
		secrets[i] = SecretShare{Index: i, Scalar: b}
	}
	for _, s := range secrets {
		if e := ValidateSecret(pub, s); e != nil {
			return Public{}, nil, e
		}
	}
	return pub, secrets, nil
}
