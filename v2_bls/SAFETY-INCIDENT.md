# Local setup isolation incident

During the initial node-discovery work, a delegated worker invoked the BSV node with `-help-debug` without `-help` and without the intended regtest/data-directory safety flags. This unexpectedly started a default mainnet node in WSL. It wrote to `/home/futureman19/.bitcoin` outside this checkout and performed DNS discovery and header synchronization.

This violated the requested regtest-only and directory-isolation constraints. It is not excused by the absence of a payment. The worker reported no transaction submission or spending. The parent did not independently audit the entire historical network traffic and cannot claim that no mainnet network contact occurred: it did occur.

The unintended process was terminated. Parent verification of `ps` and listening ports showed only the intended BSV 1.2.3 regtest daemon, running with its data directory inside this checkout, RPC bound to `127.0.0.1:18483`, `-regtest`, `-listen=0`, `-connect=0`, `-dnsseed=0`, `-discover=0`, and `-maxconnections=0`. RPC returned `chain=regtest`, `blocks=0`, and `connections=0` at that verification.

The outside-checkout files were not deleted: cleanup requires the user's permission. No existing repository or live covenant was edited during the incident.

The checked-in `scripts/node.sh` always supplies the explicit regtest/data-directory flags, accepts no extra daemon flags, checks the chain and connection count before forwarding RPC commands, and keeps the intended runtime under `.local/node/`. Future help inspection must also use explicit isolation flags or read documentation instead of executing a node binary with ambiguous help options.
