#!/usr/bin/env python3

import argparse
import json
import os
import subprocess
import sys
import platform


arch = platform.machine().lower()
system = platform.system().lower()

if system == "linux":
    if arch in ("x86_64", "amd64"):
        nix_system = "x86_64-linux"
    elif arch in ("aarch64", "arm64"):
        nix_system = "aarch64-linux"
    elif arch in ("i386", "i686"):
        nix_system = "i686-linux"
    else:
        nix_system = f"{arch}-linux"
elif system == "darwin":
    if arch in ("x86_64", "amd64"):
        nix_system = "x86_64-darwin"
    elif arch in ("arm64", "aarch64"):
        nix_system = "aarch64-darwin"
    else:
        nix_system = f"{arch}-darwin"
else:
    nix_system = f"{arch}-{system}"


def get_all_pkg_attr_paths(pkgs_dir="pkgs"):
    """Return a list of attribute paths for all packages in ./pkgs"""
    pkgs_path = os.path.join(os.getcwd(), pkgs_dir)
    if not os.path.isdir(pkgs_path):
        print(f"No '{pkgs_dir}' directory found in {os.getcwd()}")
        sys.exit(1)
    attr_paths = []
    for entry in os.listdir(pkgs_path):
        full_path = os.path.join(pkgs_path, entry)
        if os.path.isdir(full_path):
            # Assuming attribute path is pkgs.<dirname>
            attr_paths.append(entry)
    return attr_paths


def run_update(args, attr_path):
    path = os.getcwd()

    if args.nixpkgs:
        nixpkgs = args.nixpkgs
    else:
        nixpkgs = json.loads(
            subprocess.check_output(
                [
                    "nix",
                    "eval",
                    "--json",
                    "--impure",
                    "--expr",
                    f"(builtins.getFlake (toString {path})).inputs.nixpkgs",
                ]
            ).decode("utf-8")
        )

    update_nix = os.path.join(nixpkgs, "maintainers/scripts/update.nix")

    nix_args = [update_nix]
    nix_args += [
        "--arg",
        "include-overlays",
        f"(builtins.getFlake (toString {path})).outputs.legacyPackages.{nix_system}",
    ]
    nix_args += ["--argstr", "path", attr_path]
    if args.commit:
        nix_args += ["--argstr", "commit", "true"]

    nix_shell = ["nix-shell"] + nix_args

    print(f"Running: {' '.join(nix_shell)}")
    os.execvp(nix_shell[0], nix_shell)


def main(args):
    if args.attr_path:
        run_update(args, args.attr_path)
    else:
        attr_paths = get_all_pkg_attr_paths()
        if not attr_paths:
            print("No packages found in ./pkgs")
            sys.exit(1)
        for attr_path in attr_paths:
            print(f"Updating {attr_path}...")
            run_update(args, attr_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rebuild system")
    parser.add_argument("--commit", help="Commit the changes", action="store_true")
    parser.add_argument(
        "--nixpkgs",
        dest="nixpkgs",
        help="Override the nixpkgs flake input with this path, it will be used for finding update.nix",
        nargs="?",
    )
    parser.add_argument(
        "attr_path",
        metavar="attr-path",
        help="Attribute path of package to update",
        nargs="?",
    )

    args = parser.parse_args()

    main(args)
