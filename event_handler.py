from src.app.plugin_system.base import BaseEventHandler, EventDecision
from src.kernel.llm.policy import LoadBalancedPolicy, Policy, set_default_policy_factory
from src.core.config import get_model_config
from typing import Any, dict


class ModelPriorityHandler(BaseEventHandler):
    """模型优先级事件处理器。"""

    handler_name = "model_priority_handler"
    handler_description = "控制模型使用的优先顺序"

    def __init__(self, plugin):
        super().__init__(plugin)
        # 注册事件订阅
        self.init_subscribe([
            "on_plugin_loaded",
        ])
        
    async def execute(self, event_name: str, params: dict[str, Any]) -> tuple[EventDecision, dict[str, Any]]:
        """执行事件处理。"""
        if event_name == "on_plugin_loaded":
            # 当插件加载时，设置自定义的策略工厂
            set_default_policy_factory(self._create_priority_policy_factory)
            return EventDecision.SUCCESS, params
        
        return EventDecision.PASS, params
    
    def _create_priority_policy_factory(self) -> Policy:
        """创建带优先级的策略工厂。"""
        return PriorityLoadBalancedPolicy()


class PriorityLoadBalancedPolicy(LoadBalancedPolicy):
    """带优先级的负载均衡策略。"""
    
    def _select_best_model(self) -> dict[str, Any] | None:
        """
        选择负载均衡评分最低的可用模型，同时考虑模型优先级。
        
        评分公式：
        total_tokens + penalty * PENALTY_WEIGHT + usage_penalty * USAGE_PENALTY_WEIGHT + avg_latency * LATENCY_WEIGHT - priority * PRIORITY_WEIGHT
        """
        from src.core.config import get_model_config
        
        # 获取模型优先级配置
        priority_config = {}
        try:
            config = get_model_config()
            # 尝试从插件配置中获取优先级设置
            # 这里我们假设插件配置已经加载
            # 实际实现中，我们可能需要从插件的配置中获取
        except Exception:
            # 如果获取配置失败，使用空配置
            pass
        
        with self._lock:
            candidate_models = [
                m for m in self._models
                if m.get("model_identifier") not in self._failed_models
            ]
            
            if not candidate_models:
                return None
            
            # 计算每个候选模型的评分
            best_model = None
            best_score = float("inf")
            
            # 优先级权重
            PRIORITY_WEIGHT = 10000.0
            
            for model in candidate_models:
                model_name = model.get("model_identifier", "unknown")
                stats = self._model_usage.get(model_name)
                if stats is None:
                    # 如果没有统计数据，给予最高优先级（评分为0）
                    return model
                
                # 获取模型优先级，默认为0
                # 首先从模型配置中获取
                priority = model.get("priority", 0)
                
                # 然后从插件配置中获取（如果有）
                if model_name in priority_config:
                    priority = priority_config[model_name]
                
                score = (
                    stats.total_tokens
                    + stats.penalty * self._penalty_weight
                    + stats.usage_penalty * self._usage_penalty_weight
                    + stats.avg_latency * self._latency_weight
                    - priority * PRIORITY_WEIGHT  # 优先级越高，评分越低
                )
                
                if score < best_score:
                    best_score = score
                    best_model = model
            
            return best_model
