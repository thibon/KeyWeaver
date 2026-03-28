import yaml
import argparse
import os
from jinja2 import Environment, FileSystemLoader

def expand(path):
    return os.path.expanduser(path)

def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="Generate configs from central API keys")
    
    parser.add_argument("--input", default="api_keys.yaml", help="Path to api_keys.yaml")
    parser.add_argument("--targets", default="targets.yaml", help="Targets config file")
    parser.add_argument("--output-dir", default="./generated", help="Local output directory")
    parser.add_argument("--tools", default="all", help="Comma-separated tools")
    parser.add_argument("--deploy", action="store_true", help="Write directly to tool destinations")

    args = parser.parse_args()

    # load data
    apikeys = load_yaml(args.input)["apikeys"]
    targets = load_yaml(args.targets)["tools"]

    # select tools
    if args.tools == "all":
        selected_tools = targets.keys()
    else:
        selected_tools = [t.strip() for t in args.tools.split(",")]

    env = Environment(loader=FileSystemLoader("."))

    os.makedirs(args.output_dir, exist_ok=True)

    for tool in selected_tools:
        if tool not in targets:
            print(f"[!] Unknown tool: {tool}")
            continue

        config = targets[tool]

        template_file = config["template"]
        output_name = config["output"]
        destination = expand(config.get("destination", ""))

        template = env.get_template(template_file)
        template.render(**apikeys)

        # 1. toujours générer en local
        local_path = os.path.join(args.output_dir, output_name)
        with open(local_path, "w") as f:
            f.write(rendered)

        print(f"[+] Generated {local_path}")

        # 2. deploy option
        if args.deploy:
            if not destination:
                print(f"[!] No destination defined for {tool}")
                continue

            dest_dir = os.path.dirname(destination)
            os.makedirs(dest_dir, exist_ok=True)

            with open(destination, "w") as f:
                f.write(rendered)

            print(f"[+] Deployed to {destination}")

if __name__ == "__main__":
    main()