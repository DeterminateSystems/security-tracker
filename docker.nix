{ arch-security-tracker, dockerTools }:
dockerTools.buildLayeredImage {
  name = "security-tracker";
  tag = arch-security-tracker.version;
  contents = [ arch-security-tracker ];
  config = {
    Volumes."/var/lib/security-tracker" = {};
    Cmd = ["gunicorn" "tracker:app" "-b" "[::]:8000"];
    ExposedPorts."8000" = {};
  };
}
