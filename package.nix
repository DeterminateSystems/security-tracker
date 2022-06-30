{ lib
, nix-gitignore
, poetry2nix
, openssl
}:
poetry2nix.mkPoetryApplication {
  projectDir = ./.;
  src = nix-gitignore.gitignoreSource [
    "*.nix"
    "result"
  ] ./.;

  overrides = poetry2nix.overrides.withDefaults (self: super: {
    scrypt = super.scrypt.overrideAttrs (o: {
      buildInputs = o.buildInputs ++ [openssl];
    });
  });
}
