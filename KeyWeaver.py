import yaml
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("."))

# load central keys
with open("api_keys.yaml") as f:
    data = yaml.safe_load(f)["api_keys"]

def render(template_file, output_file):
    template = env.get_template(template_file)
    rendered = template.render(**data)

    with open(output_file, "w") as f:
        f.write(rendered)

render("theharvester.tpl.yaml", "theharvester_config.yaml")
render("bbot_secrets.tpl.yaml", "secrets.yml")