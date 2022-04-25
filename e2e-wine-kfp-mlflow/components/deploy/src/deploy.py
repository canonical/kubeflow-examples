import argparse
import subprocess

from jinja2 import Environment, FileSystemLoader


def deploy(model_uri: str):
    with open("/tmp/manifest.yaml", "w") as f:
        env = Environment(loader=FileSystemLoader('./templates'),
                          trim_blocks=True, lstrip_blocks=True)
        template = env.get_template('deploy-manifest.j2')
        rendered = template.render(model_uri=model_uri)
        print("Rendered Manifest:")
        print(rendered)
        f.write(rendered)

    result = subprocess.call(
        ['kubectl', 'apply', '-f', '/tmp/manifest.yaml', '-n', 'admin'])
    assert result == 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data processor')
    parser.add_argument('--model_uri', help='Model URI')

    args = parser.parse_args()

    deploy(args.model_uri)
