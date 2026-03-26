# Model Priority Plugin for Neo-MoFox

这是一个 Neo-MoFox 插件，用于控制 LLM 模型的使用优先级。

## 功能

- 允许用户通过配置文件设置模型的使用优先级
- 优先使用高优先级模型，只有当高优先级模型不可用时才使用低优先级模型
- 与 Neo-MoFox 的负载均衡策略集成，综合考虑模型的使用情况、延迟等因素

## 安装

1. 将插件目录 `model_priority` 复制到 Neo-MoFox 的 `plugins` 目录下
2. 重启 Neo-MoFox 系统

## 配置

在 `config/plugins/model_priority/model_priority_config.toml` 文件中设置模型的优先级：

```toml
[priority]
enabled = true

# 模型优先级映射，格式为：模型标识符: 优先级值
# 优先级值越大，模型越优先被使用
model_priorities = {
    "deepseek-ai/DeepSeek-V3.2" = 100,  # 高优先级
    "Qwen/Qwen3-8B" = 0                  # 低优先级
}
```

## 工作原理

1. 插件通过 `on_plugin_loaded` 事件，在插件加载时自动设置自定义策略为默认策略
2. 自定义策略在模型选择时考虑优先级因素
3. 优先级高的模型会被优先选择，只有当高优先级模型不可用时，才会使用低优先级模型

## 示例

假设你有两个模型：
- 模型 A（包月）：`model_identifier = "deepseek-ai/DeepSeek-V3.2"`，优先级配置为 100
- 模型 B（按量付费）：`model_identifier = "Qwen/Qwen3-8B"`，优先级配置为 0

在模型选择时：
- 系统会优先使用模型 A
- 只有当模型 A 不可用（如达到 token 限制或连接失败）时，系统才会选择模型 B
