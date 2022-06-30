{
  description = "NixOS security tracker";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }: {
    nixosModule = { system, lib, ... }: {
      imports = [ ./module.nix ];
      # TODO: decide if this makes sense
      #security-tracker.package = lib.mkDefault self.defaultPackage.${system};
    };
  } // flake-utils.lib.eachDefaultSystem (system: {
    packages.security-tracker = nixpkgs.legacyPackages.${system}.callPackage ./package.nix {};
    defaultPackage = self.packages.${system}.security-tracker;

    nixosTest = nixpkgs.legacyPackages.${system}.nixosTest {
      nodes.machine = {
        imports = [ self.nixosModule ];
        services.security-tracker.enable = true;
      };

      testScript = ''
        machine.wait_for_unit("multi-user.target")
        machine.succeed("trackerctl db initdb")
        machine.wait_until_succeeds("curl --silent --show-error --fail localhost:8000")
      '';
    };
  });
}
