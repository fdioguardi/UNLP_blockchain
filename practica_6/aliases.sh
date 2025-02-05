alias tarpaulin="cargo tarpaulin --target-dir src/coverage --skip-clean --exclude-files=target/debug/* --out html"

alias full="cargo contract build && cargo test && tarpaulin"
