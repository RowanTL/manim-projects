{
  description = "Python development environment for Manim";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };

        # Define the Python environment and include Manim
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          manim
          numpy
          ruff
          ty
        ]);

      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            pythonEnv
            
            # System dependencies required by Manim
            ffmpeg
            cairo
            pango
            pkg-config

            # LaTeX environment for rendering math equations.
            # Note: scheme-full is large but guarantees you won't miss obscure packages.
            texlive.combined.scheme-full 

            vlc # Play the videos back
          ];

          shellHook = ''
            echo "Python: $(python --version)"
            echo "Manim:  $(manim --version)"
          '';
        };
      }
    );
}
