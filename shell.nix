{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.python312Packages.pip
    pkgs.python312Packages.setuptools
    pkgs.python312Packages.requests
    pkgs.python312Packages.reportlab
    pkgs.python312Packages.matplotlib
    pkgs.python312Packages.pytest
  ];

shellHook = ''
    export PYTHONPATH=$PWD/src:$PYTHONPATH
    echo "PYTHONPATH set to $PYTHONPATH"
  '';

}