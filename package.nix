{ buildPythonPackage
, lib
, nix-gitignore
, flask
, flask_login
, flask_sqlalchemy
, flask_migrate
, flask_wtf
, flask-talisman
, email_validator
, requests
, py_scrypt
, sqlalchemy-continuum
, feedgen
, pytz
, authlib
, markupsafe
, pacman
, pkg-config
, libarchive
, git
, poetry2nix
, openssl
}:
poetry2nix.mkPoetryApplication {
  #pname = "arch-security-tracker";
  #version = "unstable";
  projectDir = ./.;
  src = nix-gitignore.gitignoreSource [
    "*.nix"
  ] ./.;

  overrides = poetry2nix.overrides.withDefaults (self: super: {
    scrypt = super.scrypt.overrideAttrs (o: {
      buildInputs = o.buildInputs ++ [openssl];
    });
  });
  #buildInputs = [
  #  flask
  #  flask_login
  #  flask_sqlalchemy
  #  flask_migrate
  #  flask_wtf
  #  flask-talisman
  #  email_validator
  #  requests
  #  py_scrypt
  #  sqlalchemy-continuum
  #  feedgen
  #  pytz
  #  authlib
  #  markupsafe
  #];
}
