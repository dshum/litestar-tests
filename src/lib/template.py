from jinja2 import Environment, PackageLoader, select_autoescape
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template import TemplateConfig

environment = Environment(
    loader=PackageLoader("app", "templates"),
    autoescape=select_autoescape(),
)

template_config = TemplateConfig(
    instance=JinjaTemplateEngine.from_environment(environment)
)
