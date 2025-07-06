{
  lib,
	stdenv,
  python3,
	makeWrapper
}:
stdenv.mkDerivation {
  pname = "update-pkgs";
  version = "0.1.0";

  src = ./src;

	nativeBuildInputs = [
		makeWrapper
	];

  installPhase = ''
    mkdir -p $out/bin
    cp ./script.py $out/bin/nur-package-update
    chmod +x $out/bin/nur-package-update
		wrapProgram $out/bin/nur-package-update \
			--prefix PATH : ${lib.makeBinPath [ python3 ]}
  '';

  meta = {
    description = "CLI for updating Nur packages using update.nix";
    license = lib.licenses.mit;
    maintainers = with lib.maintainers; [ eveeifyeve ];
  };
}
