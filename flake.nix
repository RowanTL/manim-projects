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
        LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath (with pkgs; [
          stdenv.cc.cc.lib
          zlib
          
          # Core Graphics
          glib
          libGL

          # Desktop / Windowing libraries required by PyPI Qt wheels
          libxkbcommon
          fontconfig
          dbus
          xorg.libX11
          xorg.libxcb
          xorg.libXext
          xorg.libXrender
          xorg.libXi
        ]);
        # To prevent Qt from throwing warnings about missing Wayland plugins, 
        # it's usually safest to force it to use X11/xcb when running through Nix + PyPI wheels
        QT_QPA_PLATFORM = "xcb";
        shellHook = ''
          unset PYTHONPATH
        '';
      };
    };
}
