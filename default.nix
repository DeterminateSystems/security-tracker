{ sources ? import ./nix/sources.nix
, pkgs ? import sources.nixpkgs {}
}:
let
  callPackage = pkgs.newScope (pkgs // pkgs.python3Packages // self);
  self = {
    security-tracker = callPackage ./package.nix {};
    dockerImage = callPackage ./docker.nix {};
  };
in self
