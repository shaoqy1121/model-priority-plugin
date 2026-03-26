from src.app.plugin_system.base import BasePlugin, register_plugin

from .config import ModelPriorityConfig
from .event_handler import ModelPriorityHandler


@register_plugin
class ModelPriorityPlugin(BasePlugin):
    """模型优先级插件。"""

    plugin_name = "model_priority"
    plugin_description = "控制模型使用的优先顺序"
    plugin_version = "1.0.0"

    configs: list[type] = [ModelPriorityConfig]
    dependent_components: list[str] = []

    def get_components(self) -> list[type]:
        """返回插件组件类。"""

        return [ModelPriorityHandler]
