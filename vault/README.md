# Vault

`artifacts/vault.json` is committed for reproducibility with exact pins for scrypt-ts 1.4.5 and scrypt-cli 0.2.3 (scryptlib 2.2.6 in the lockfile; native sCrypt compiler 1.20.0+commit.693498a); rebuilds must match the public checker's prefix and code-tail fingerprint.

## Build

```sh
npm run build
```

## Testing Locally

```sh
npm run test
```

## Run Tests on the Bitcoin Testnet

```sh
npm run test:testnet
```
