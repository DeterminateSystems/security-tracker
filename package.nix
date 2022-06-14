{ buildPythonPackage
, lib
, nix-gitignore
, poetry2nix
, openssl
, pkgconfig
, pkg-config
, pacman
, libarchive
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
    pyalpm = super.pyalpm.overrideAttrs (o: {
      nativeBuildInputs = (o.nativeBuildInputs or []) ++ [ pkg-config ];
      buildInputs = o.buildInputs ++ [ pkgconfig pacman libarchive ];
    });
  });
}
