{
  description = "Manim and manim-slides ";

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
          ]))
          pkgs.uv
          pkgs.ffmpeg
          pkgs.cairo
          pkgs.pango
          pkgs.pkg-config
          pkgs.texlive.combined.scheme-full
          pkgs.ninja
          pkgs.ruff
          pkgs.ty
        ];
        # Fix for "cannot open shared object file" errors from PyPI wheels.
        # This tells the dynamic linker where to find these core libraries.
        LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath (with pkgs; [
          stdenv.cc.cc.lib # Provides libstdc++.so.6
          zlib             # Often needed by numpy/pandas
          glib             # Often needed by OpenCV
          libGL            # Needed by OpenCV
        ]);
        shellHook = ''
          unset PYTHONPATH
        '';
      };
    };
}
