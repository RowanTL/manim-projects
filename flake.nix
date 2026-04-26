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
          
          # Audio / Multimedia
          libpulseaudio
          pipewire
          alsa-lib
          
          # Video / Hardware Acceleration
          libglvnd
          wayland
          libva
          libvdpau
          libdrm         # <-- NEW
          mesa           # <-- NEW
          
          # Network / Security
          krb5
          nss            # <-- NEW (Often needed for QtWebEngine/Media)
          nspr           # <-- NEW
          expat          # <-- NEW
          
          # Core Graphics
          glib
          libGL

          # Desktop / Windowing basics
          libxkbcommon
          fontconfig
          freetype
          dbus

          # Extensive X11 / XCB support
          xorg.libX11
          xorg.libxcb
          xorg.libXext
          xorg.libXrender
          xorg.libXi
          xorg.libXrandr
          xorg.libXcomposite # <-- NEW
          xorg.libXdamage    # <-- NEW
          xorg.libXfixes     # <-- NEW
          xorg.libXcursor    # <-- NEW
          xorg.xcbutil
          xorg.xcbutilwm
          xorg.xcbutilimage
          xorg.xcbutilkeysyms
          xorg.xcbutilrenderutil
          xorg.xcbutilcursor
        ]);
        QT_QPA_PLATFORM = "xcb";
        shellHook = ''
          unset PYTHONPATH
        '';
      };
    };
}
