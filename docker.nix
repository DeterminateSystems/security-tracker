{ arch-security-tracker, dockerTools }:
dockerTools.buildLayeredImage {
  name = "security-tracker";
  contents = [ arch-security-tracker ];
  config = {
    Volumes."/var/lib/security-tracker" = {};
    Cmd = ["gunicorn" "tracker:app"];
  };
}
