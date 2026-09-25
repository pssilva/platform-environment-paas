#!/usr/bin/env python3
"""Python port of PaaSScriptsUteis_main.sh.

Installation commands run only when their corresponding subcommand is invoked.
"""
from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path
import subprocess
import sys

VERSION = "1.0"
FIELDS = ["ID", "PROJECT_NAME", "NAME_BRANCH_WORK", "ARTIFACT_ID_PARENT",
          "ARTIFACT_ID", "PROVEDOR", "PROJECT_DESCRIPTION", "LINK_CERTIFICATION",
          "TITULO_CERTIFICATION", "ARTIFACT_ID_SUB_CERTIFICATON", "LINK_GITHUB"]
PROVIDERS = ("AWS", "Azure", "GCP", "Hpc", "RhOpenShift", "OCI", "Sp")


def set_venvs() -> dict[str, str]:
    script = Path(__file__).resolve()
    automation = script.parents[2]
    return {"ABS_SCRIPT_PATH": str(script), "ABS_DIRECTORY": str(script.parent),
            "PARENT_MODULO": "PaaSScriptsUteis", "AUTOMATION_PATH": str(automation),
            "TEMPLATES_PATH": str(automation / "PaaSScriptsUteis" / "shell" / "templates")}


def run(*args: str) -> None:
    subprocess.run(args, check=True)


def install_prerequisites() -> None:
    for command in (("sudo", "dnf", "-y", "check-update"), ("sudo", "dnf", "-y", "upgrade"),
                    ("sudo", "dnf", "-y", "groupinstall", "Development Tools"),
                    ("sudo", "dnf", "-y", "group", "install", "C Development Tools and Libraries"),
                    ("sudo", "dnf", "-y", "groupinstall", "@development-tools", "@development-libraries"),
                    ("sudo", "dnf", "install", "-y", "make", "automake", "gcc", "gcc-c++", "kernel-devel"),
                    ("sudo", "dnf", "install", "-y", "git", "make", "cmake", "curl", "unzip", "g++", "libtool", "jq")):
        run(*command)


def install_sdkman() -> None:
    subprocess.run("curl -s get.sdkman.io | bash", shell=True, check=True)
    init = Path.home() / ".sdkman/bin/sdkman-init.sh"
    if not init.exists():
        raise FileNotFoundError(f"SDKMAN init not found: {init}")
    subprocess.run(["bash", "-lc", f'source "{init}" && sdk version'], check=True)


def install_java(version: str = "17.0.11-amzn") -> None:
    environment = os.environ.copy()
    environment["SDK_JAVA_VERSION"] = version
    subprocess.run(["bash", "-lc", 'source "$HOME/.sdkman/bin/sdkman-init.sh" && sdk install java "$SDK_JAVA_VERSION" -y'], env=environment, check=True)


def install_docker() -> None:
    run("sudo", "dnf", "install", "-y", "docker-compose")
    run("sudo", "dnf", "install", "-y", "docker-compose-plugin")
    run("docker", "compose", "version")


def make_all_tools() -> None:
    print("\nPaaSScriptsUteis.makeAllTools: NÃO IMPLEMENTADO AINDA!\n")


def install_all_tools() -> None:
    install_prerequisites()
    install_sdkman()
    install_java()
    install_docker()
    make_all_tools()


def project_inputs(args: list[str]) -> dict[str, str]:
    if not args:
        raise ValueError("Informe um arquivo env ou NAME_PROJECT ARTIFACT_ID [ARCH].")
    candidate = Path(args[0]).expanduser()
    values: dict[str, str] = {}
    if candidate.is_file():
        # Supports simple KEY=value env files; arbitrary shell code is intentionally not executed.
        for raw in candidate.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip().strip("\"'")
    else:
        for key, value in zip(("NAME_PROJECT", "ARTIFACT_ID", "ARCH"), args):
            values[key] = value
    values.setdefault("ARCH", "arch/clean")
    values.setdefault("ARTIFACT_ID_PATH", "")
    return values


def install_provider(provider: str, args: list[str]) -> None:
    values = project_inputs(args)
    print(f"PaaSScriptsUteis.installSDKProvedor{provider}: NÃO IMPLEMENTADO AINDA!")
    for key in ("NAME_PROJECT", "ARTIFACT_ID", "ARTIFACT_ID_PATH", "ARCH"):
        print(f" {key} = {values.get(key, '')}")
    print("A automação de instalação deste provedor não está implementada no shell original.")


def create_structure(work_path: Path) -> None:
    if work_path.exists():
        return
    for relative in ("docs/imgs", "docs/indexacoes", "docs/provedores_nuvem",
                     "scripts/src/main/automation", "scripts/src/test/automation"):
        directory = work_path / relative
        directory.mkdir(parents=True, exist_ok=True)
        (directory / ".gitkeep").touch(exist_ok=True)


def process_csv(input_csv: Path, template: Path | None = None) -> int:
    root = Path.home() / "projetos"
    template = template or Path(set_venvs()["TEMPLATES_PATH"]) / "README_provedor_nuvem.md"
    count = 0
    with input_csv.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames:
            raise ValueError("CSV vazio ou sem cabeçalho")
        for row in reader:
            values = {key: (row.get(key) or "").strip().strip('"') for key in FIELDS}
            parent = root / values["ARTIFACT_ID_PARENT"]
            target = parent / values["ARTIFACT_ID"] / values["ARTIFACT_ID_SUB_CERTIFICATON"]
            create_structure(target)
            readme = target / "README.md"
            if not readme.exists() and template.is_file():
                content = template.read_text(encoding="utf-8")
                replacements = {"PROJECT_NAME": values["PROJECT_NAME"], "ARTIFACT_ID": values["ARTIFACT_ID"],
                                "ARTIFACT_ID_PARENT": values["ARTIFACT_ID_PARENT"],
                                "ARTIFACT_ID_SUB_CERTIFICATON": values["ARTIFACT_ID_SUB_CERTIFICATON"],
                                "TITULO_CERTIFICATION": values["TITULO_CERTIFICATION"],
                                "LINK_GITHUB": values["LINK_GITHUB"], "LINK_CERTIFICATION": values["LINK_CERTIFICATION"]}
                for key, value in replacements.items():
                    content = content.replace("{{" + key + "}}", value)
                readme.write_text(content, encoding="utf-8")
            count += 1
    return count


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Utilitários de automação PaaS", add_help=True)
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("menu", help="Exibe o menu interativo")
    for name in ("install-pre-requisites", "install-sdkman", "install-java", "install-docker", "install-all-tools", "make-all-tools"):
        item = sub.add_parser(name)
        if name == "install-java": item.add_argument("version", nargs="?", default="17.0.11-amzn")
    for provider in PROVIDERS:
        item = sub.add_parser("provider-" + provider.lower())
        item.add_argument("args", nargs="*")
    item = sub.add_parser("create-structure"); item.add_argument("work_path", type=Path)
    item = sub.add_parser("process-csv"); item.add_argument("input_csv", type=Path)
    sub.add_parser("summary")
    return parser


def menu() -> None:
    choices = ("Voltar", "Criar Projeto", "tarefa3", "tarefa4", "tarefa5", "fim")
    while True:
        print("\n".join(f"{i}. {value}" for i, value in enumerate(choices, 1)))
        try: choice = input("PaaSScriptsUteis »»» Selecione uma opção: ").strip()
        except EOFError: return
        try: selected = choices[int(choice)-1]
        except (ValueError, IndexError): print("Opção não encontrada!"); continue
        if selected == "fim": print("PaaSScriptsUteis.menu »»» Finalizado!!"); return
        print(f"{selected} selecionado")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "menu": menu()
        elif args.command == "install-pre-requisites": install_prerequisites()
        elif args.command == "install-sdkman": install_sdkman()
        elif args.command == "install-java": install_java(args.version)
        elif args.command == "install-docker": install_docker()
        elif args.command == "install-all-tools": install_all_tools()
        elif args.command == "make-all-tools": make_all_tools()
        elif args.command and args.command.startswith("provider-"): install_provider(args.command[9:], args.args)
        elif args.command == "create-structure": create_structure(args.work_path)
        elif args.command == "process-csv": print(f"Linhas processadas: {process_csv(args.input_csv)}")
        elif args.command == "summary": print("Rotinas de criação de pastas, CSV e instalação de ferramentas. Use --help para comandos.")
        else: build_parser().print_help()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Erro: {error}", file=sys.stderr); return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
