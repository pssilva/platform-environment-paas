// Command paas_scripts_uteis ports the PaaSScriptsUteis shell helpers.
package main

import (
	"bufio"
	"encoding/csv"
	"errors"
	"flag"
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
)

const version = "1.0"

var fields = []string{"ID", "PROJECT_NAME", "NAME_BRANCH_WORK", "ARTIFACT_ID_PARENT", "ARTIFACT_ID", "PROVEDOR", "PROJECT_DESCRIPTION", "LINK_CERTIFICATION", "TITULO_CERTIFICATION", "ARTIFACT_ID_SUB_CERTIFICATON", "LINK_GITHUB"}

func run(name string, args ...string) error {
	cmd := exec.Command(name, args...)
	cmd.Stdin, cmd.Stdout, cmd.Stderr = os.Stdin, os.Stdout, os.Stderr
	return cmd.Run()
}

func installPrerequisites() error {
	commands := [][]string{{"dnf", "-y", "check-update"}, {"dnf", "-y", "upgrade"}, {"dnf", "-y", "groupinstall", "Development Tools"}, {"dnf", "-y", "group", "install", "C Development Tools and Libraries"}, {"dnf", "-y", "groupinstall", "@development-tools", "@development-libraries"}, {"dnf", "install", "-y", "make", "automake", "gcc", "gcc-c++", "kernel-devel"}, {"dnf", "install", "-y", "git", "make", "cmake", "curl", "unzip", "g++", "libtool", "jq"}}
	for _, args := range commands {
		if err := run("sudo", args...); err != nil {
			return err
		}
	}
	return nil
}

func installSDKMAN() error {
	if err := run("bash", "-lc", "curl -s get.sdkman.io | bash"); err != nil {
		return err
	}
	return run("bash", "-lc", `source "$HOME/.sdkman/bin/sdkman-init.sh" && sdk version`)
}

func installJava(version string) error {
	if version == "" {
		version = "17.0.11-amzn"
	}
	cmd := exec.Command("bash", "-lc", `source "$HOME/.sdkman/bin/sdkman-init.sh" && sdk install java "$SDK_JAVA_VERSION" -y`)
	cmd.Env = append(os.Environ(), "SDK_JAVA_VERSION="+version)
	cmd.Stdin, cmd.Stdout, cmd.Stderr = os.Stdin, os.Stdout, os.Stderr
	return cmd.Run()
}

func installDocker() error {
	if err := run("sudo", "dnf", "install", "-y", "docker-compose"); err != nil {
		return err
	}
	if err := run("sudo", "dnf", "install", "-y", "docker-compose-plugin"); err != nil {
		return err
	}
	return run("docker", "compose", "version")
}

func makeAllTools() { fmt.Println("PaaSScriptsUteis.makeAllTools: NÃO IMPLEMENTADO AINDA!") }

func createStructure(root string) error {
	if _, err := os.Stat(root); err == nil {
		return nil
	} else if !errors.Is(err, os.ErrNotExist) {
		return err
	}
	for _, rel := range []string{"docs/imgs", "docs/indexacoes", "docs/provedores_nuvem", "scripts/src/main/automation", "scripts/src/test/automation"} {
		dir := filepath.Join(root, rel)
		if err := os.MkdirAll(dir, 0755); err != nil {
			return err
		}
		file, err := os.OpenFile(filepath.Join(dir, ".gitkeep"), os.O_CREATE|os.O_WRONLY, 0644)
		if err != nil {
			return err
		}
		file.Close()
	}
	return nil
}

func templatePath() string {
	_, file, _, _ := runtime.Caller(0)
	return filepath.Join(filepath.Dir(file), "..", "shell", "templates", "README_provedor_nuvem.md")
}

func processCSV(input string) (int, error) {
	f, err := os.Open(input)
	if err != nil {
		return 0, err
	}
	defer f.Close()
	r := csv.NewReader(f)
	r.FieldsPerRecord = -1
	header, err := r.Read()
	if err != nil {
		return 0, err
	}
	indices := map[string]int{}
	for i, name := range header {
		indices[strings.TrimSpace(strings.TrimPrefix(name, "\ufeff"))] = i
	}
	for _, field := range fields {
		if _, ok := indices[field]; !ok {
			return 0, fmt.Errorf("CSV: coluna obrigatória ausente: %s", field)
		}
	}
	home, err := os.UserHomeDir()
	if err != nil {
		return 0, err
	}
	template, templateErr := os.ReadFile(templatePath())
	count := 0
	for {
		row, readErr := r.Read()
		if readErr == io.EOF {
			break
		}
		if readErr != nil {
			return count, readErr
		}
		value := map[string]string{}
		for _, key := range fields {
			i := indices[key]
			if i < len(row) {
				value[key] = strings.Trim(row[i], `"`)
			}
		}
		root := filepath.Join(home, "projetos", value["ARTIFACT_ID_PARENT"], value["ARTIFACT_ID"], value["ARTIFACT_ID_SUB_CERTIFICATON"])
		if err := createStructure(root); err != nil {
			return count, err
		}
		readme := filepath.Join(root, "README.md")
		if _, err := os.Stat(readme); errors.Is(err, os.ErrNotExist) && templateErr == nil {
			content := string(template)
			replacements := map[string]string{"PROJECT_NAME": value["PROJECT_NAME"], "ARTIFACT_ID": value["ARTIFACT_ID"], "ARTIFACT_ID_PARENT": value["ARTIFACT_ID_PARENT"], "ARTIFACT_ID_SUB_CERTIFICATON": value["ARTIFACT_ID_SUB_CERTIFICATON"], "TITULO_CERTIFICATION": value["TITULO_CERTIFICATION"], "LINK_GITHUB": value["LINK_GITHUB"], "LINK_CERTIFICATION": value["LINK_CERTIFICATION"]}
			for key, val := range replacements {
				content = strings.ReplaceAll(content, "{{"+key+"}}", val)
			}
			if err := os.WriteFile(readme, []byte(content), 0644); err != nil {
				return count, err
			}
		}
		count++
	}
	return count, nil
}

func menu() {
	choices := []string{"Voltar", "Criar Projeto", "tarefa3", "tarefa4", "tarefa5", "fim"}
	s := bufio.NewScanner(os.Stdin)
	for {
		for i, c := range choices {
			fmt.Printf("%d. %s\n", i+1, c)
		}
		fmt.Print("PaaSScriptsUteis »»» Selecione uma opção: ")
		if !s.Scan() {
			return
		}
		choice := strings.TrimSpace(s.Text())
		if choice == "6" || strings.EqualFold(choice, "fim") {
			fmt.Println("PaaSScriptsUteis.menu »»» Finalizado!!")
			return
		}
		fmt.Println("Opção selecionada:", choice)
	}
}

func usage() {
	fmt.Printf("PaaSScriptsUteis %s\nUso: paas_scripts_uteis <comando> [argumentos]\nComandos: menu, install-pre-requisites, install-sdkman, install-java [versão], install-docker, install-all-tools, make-all-tools, provider-<aws|azure|gcp|hpc|rhopenshift|oci|sp>, create-structure <caminho>, process-csv <arquivo>, summary\n", version)
}

func main() {
	flag.Usage = usage
	flag.Parse()
	args := flag.Args()
	if len(args) == 0 || args[0] == "--help" || args[0] == "-h" {
		usage()
		return
	}
	var err error
	switch args[0] {
	case "--version", "version":
		fmt.Println(version)
	case "menu":
		menu()
	case "install-pre-requisites":
		err = installPrerequisites()
	case "install-sdkman":
		err = installSDKMAN()
	case "install-java":
		versionArg := ""
		if len(args) > 1 {
			versionArg = args[1]
		}
		err = installJava(versionArg)
	case "install-docker":
		err = installDocker()
	case "install-all-tools":
		if err = installPrerequisites(); err == nil {
			if err = installSDKMAN(); err == nil {
				if err = installJava("17.0.11-amzn"); err == nil {
					err = installDocker()
				}
			}
		}
		if err == nil {
			makeAllTools()
		}
	case "make-all-tools":
		makeAllTools()
	case "create-structure":
		if len(args) < 2 {
			err = errors.New("informe o caminho de trabalho")
		} else {
			err = createStructure(args[1])
		}
	case "process-csv":
		if len(args) < 2 {
			err = errors.New("informe o arquivo CSV")
		} else {
			var n int
			n, err = processCSV(args[1])
			if err == nil {
				fmt.Printf("Linhas processadas: %d\n", n)
			}
		}
	case "summary":
		fmt.Println("Rotinas de criação de pastas, CSV e instalação de ferramentas. Use --help para comandos.")
	default:
		if strings.HasPrefix(args[0], "provider-") {
			fmt.Printf("PaaSScriptsUteis.installSDKProvedor%s: NÃO IMPLEMENTADO AINDA!\n", strings.TrimPrefix(args[0], "provider-"))
			fmt.Println("A automação de instalação deste provedor não está implementada no shell original.")
		} else {
			usage()
			err = fmt.Errorf("comando desconhecido: %s", args[0])
		}
	}
	if err != nil {
		fmt.Fprintln(os.Stderr, "Erro:", err)
		os.Exit(1)
	}
}
