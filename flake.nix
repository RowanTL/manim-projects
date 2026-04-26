{
  description = "Develop Shell with CUDA and python available";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs =
    { nixpkgs, ... }:
    let
      inherit (nixpkgs) lib;
      # forAllSystems = lib.genAttrs lib.systems.flakeExposed;
      system = "x86_64-linux";
    in
    {
      devShells."${system}".default = let
        pkgs = import nixpkgs {
          inherit system;

          config = {
            allowUnfree = true;
          };
        };
      in pkgs.mkShell {
        packages = [
          (pkgs.python3.withPackages (pypkgs: with pypkgs; [
            # torch
            # torchvision
            # torchaudio
            # plyfile
            # tqdm
            # joblib
            # opencv-python
            # numpy
          ]))
          pkgs.uv
          pkgs.ffmpeg
          pkgs.cairo
          pkgs.pango
          pkgs.pkg-config
          pkgs.texlive.combined.scheme-full
          pkgs.ninja
        ];
        shellHook = ''
          unset PYTHONPATH
        '';
      };
    };
}
