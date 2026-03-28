import yaml
import argparse
import os
from jinja2 import Environment, FileSystemLoader

# mapping tool -> template / output
TEMPLATES = {
    "theharvester": ("theharvester.tpl.yaml", "theharvester_config.yaml"),
    "bbot": ("bbot_secrets.tpl.yaml", "secrets.yml"),
}

def main():
    parser = argparse.ArgumentParser(description="Generate configs from central API keys")
    parser.add_argument("--input", default="api_keys.yaml", help="Path to api_keys.yaml")
    parser.add_argument("--output-dir", default=".", help="Output directory")
    parser.add_argument("--tools", default="all", help="Comma-separated list of tools (bbot,theharvester)")

    args = parser.parse_args()

    # load keys
    with open(args.input) as f:
        data = yaml.safe_load(f)["api_keys"]

    # select tools
    if args.tools == "all":
        selected_tools = TEMPLATES.keys()
    else:
        selected_tools = [t.strip() for t in args.tools.split(",")]

    env = Environment(loader=FileSystemLoader("."))

    os.makedirs(args.output_dir, exist_ok=True)

    for tool in selected_tools:
        if tool not in TEMPLATES:
            print(f"[!] Unknown tool: {tool}")
            continue

        template_file, output_file = TEMPLATES[tool]
        template = env.get_template(template_file)
        rendered = template.render(**data)

        output_path = os.path.join(args.output_dir, output_file)

        with open(output_path, "w") as f:
            f.write(rendered)

        print(f"[+] Generated {output_path}")

if __name__ == "__main__":
    main()