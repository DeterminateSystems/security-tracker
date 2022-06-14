{ security-tracker, dockerTools }:
dockerTools.buildLayeredImage {
  name = "security-tracker";
  tag = security-tracker.version;
  contents = [ security-tracker ];
  config = {
    Volumes."/var/lib/security-tracker" = {};
    Cmd = ["gunicorn" "tracker:app" "-b" "[::]:8000"];
    ExposedPorts."8000" = {};
  };
}
