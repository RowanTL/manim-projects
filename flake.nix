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
          # Core C++ and Math
          stdenv.cc.cc.lib
          zlib
          zstd
          
          # Core Graphics
          glib
          libGL

          # Network / Security
          krb5

          # Audio
          libpulseaudio
          pipewire
          alsa-lib

          # Desktop / Windowing basics
          libxkbcommon
          fontconfig
          freetype
          dbus

          # Extensive X11 / XCB support (Usually required by PyQt6/PySide6 wheels)
          xorg.libX11
          xorg.libxcb
          xorg.libXext
          xorg.libXrender
          xorg.libXi
          xorg.xcbutil
          xorg.xcbutilwm
          xorg.xcbutilimage
          xorg.xcbutilkeysyms
          xorg.xcbutilrenderutil
          xorg.xcbutilcursor # Usually the exact missing file for PyQt6
        ]);
        QT_QPA_PLATFORM = "xcb";
        shellHook = ''
          unset PYTHONPATH
        '';
      };
    };
}
