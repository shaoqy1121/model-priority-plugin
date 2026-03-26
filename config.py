from src.app.plugin_system.base import BaseConfig, Field, SectionBase, config_section


class ModelPriorityConfig(BaseConfig):
    """模型优先级配置。"""

    config_name = "model_priority_config"
    config_description = "控制模型使用的优先顺序"

    @config_section("priority")
    class PrioritySection(SectionBase):
        """模型优先级配置。"""

        enabled: bool = Field(default=True, description="是否启用优先级控制")
        
        # 模型优先级映射，格式为：模型名称: 优先级值
        # 优先级值越大，模型越优先被使用
        model_priorities: dict[str, int] = Field(
            default_factory=dict,
            description="模型优先级映射，格式为：模型名称: 优先级值"
        )

    priority: PrioritySection = Field(default_factory=PrioritySection)
