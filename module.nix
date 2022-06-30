{ config, pkgs, lib, ... }:
let
  cfg = config.services.security-tracker;
  settingsFormat = pkgs.formats.ini {};
in {
  options.services.security-tracker = {
    enable = lib.mkEnableOption "NixOS security tracker";
    package = lib.mkOption {
      type = lib.types.package;
      default = pkgs.callPackage ./package.nix {};
    };
    port = lib.mkOption {
      type = lib.types.port;
      default = 8000;
    };
    settings = lib.mkOption {
      description = ''
        Settings for the security tracker, which override the defaults from the package.

        See https://github.com/DeterminateSystems/security-tracker/blob/master/config/00-default.conf for the defaults.
      '';
      type = settingsFormat.type;
      default = {};
    };
  };
  config = lib.mkIf cfg.enable {
    systemd.services.security-tracker = {
      wantedBy = ["multi-user.target"];
      serviceConfig = {
        ExecStart = "${cfg.package.dependencyEnv}/bin/gunicorn tracker:app [::]:${toString cfg.port}";
        DynamicUser = true;
        StateDirectory = "security-tracker";
      };
    };
    environment.etc."security-tracker/nixos.conf".source = settingsFormat.generate "security-tracker-nixos.conf" cfg.settings;
    # Is this a sensible approach to getting scripts to run in the DynamicUser context?
    environment.systemPackages = [ (pkgs.writeScriptBin "trackerctl" ''
      #!${pkgs.runtimeShell}
      stdio_flag=--pipe
      [[ -t 0 ]] && stdio_flag=--pty
      exec systemd-run \
        -p User=security-tracker \
        -p DynamicUser=true \
        -p StateDirectory=security-tracker \
        "$stdio_flag" \
        -- ${cfg.package}/bin/trackerctl "$@"
    '') ];
  };
}
