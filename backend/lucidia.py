"""
Lucidia: The CarPool Routing Engine
by BlackRoad OS, Inc.

Intelligent multi-AI orchestration system that analyzes tasks and routes
to the optimal model from user's connected providers.

Named after the Latin "lucidus" (clear, bright) - making clear decisions
about which AI to use for each task.
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from pydantic import BaseModel
import tiktoken


class TaskComplexity(str, Enum):
    """Task complexity levels"""
    TRIVIAL = "trivial"          # Simple lookups, basic Q&A
    SIMPLE = "simple"            # Straightforward tasks
    MODERATE = "moderate"        # Multi-step reasoning
    COMPLEX = "complex"          # Deep analysis, long context
    EXPERT = "expert"            # Specialized knowledge, o1-level


class TaskType(str, Enum):
    """Types of tasks Lucidia can classify"""
    CHAT = "chat"                      # General conversation
    CODE = "code"                      # Programming tasks
    ANALYSIS = "analysis"              # Data/text analysis
    CREATIVE = "creative"              # Writing, ideation
    MULTIMODAL = "multimodal"          # Images, audio, video
    REASONING = "reasoning"            # Complex problem-solving
    REALTIME = "realtime"              # Current events, search


class ModelProvider(str, Enum):
    """Supported AI providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    XAI = "xai"
    LOCAL = "local"
    CUSTOM = "custom"


class ModelCapability(BaseModel):
    """Model capability profile"""
    provider: ModelProvider
    model_id: str
    context_window: int
    supports_vision: bool = False
    supports_function_calling: bool = False
    cost_per_1k_tokens: float
    speed_tier: str  # "fast", "medium", "slow"
    quality_tier: str  # "basic", "good", "excellent", "expert"


class TaskAnalysis(BaseModel):
    """Lucidia's analysis of a task"""
    complexity: TaskComplexity
    task_type: TaskType
    estimated_tokens: int
    requires_vision: bool = False
    requires_tools: bool = False
    requires_realtime: bool = False
    context_length: int = 0


class RoutingDecision(BaseModel):
    """Lucidia's routing decision"""
    selected_model: str
    selected_provider: ModelProvider
    reasoning: str
    alternatives: List[str]
    estimated_cost: float
    confidence_score: float


class LucidiaRouter:
    """
    The brain of CarPool - intelligently routes tasks to optimal AI models.

    Like a smart dispatcher in a carpool service:
    - Analyzes each trip (task)
    - Picks the right vehicle (model)
    - Optimizes for cost and quality
    - Handles fallbacks if primary choice unavailable
    """

    def __init__(self):
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

        # Model capability database
        self.model_capabilities: Dict[str, ModelCapability] = {
            "gpt-4o": ModelCapability(
                provider=ModelProvider.OPENAI,
                model_id="gpt-4o",
                context_window=128000,
                supports_vision=True,
                supports_function_calling=True,
                cost_per_1k_tokens=0.005,
                speed_tier="fast",
                quality_tier="excellent"
            ),
            "gpt-4o-mini": ModelCapability(
                provider=ModelProvider.OPENAI,
                model_id="gpt-4o-mini",
                context_window=128000,
                supports_vision=True,
                supports_function_calling=True,
                cost_per_1k_tokens=0.00015,
                speed_tier="fast",
                quality_tier="good"
            ),
            "o1": ModelCapability(
                provider=ModelProvider.OPENAI,
                model_id="o1",
                context_window=200000,
                supports_vision=False,
                supports_function_calling=False,
                cost_per_1k_tokens=0.015,
                speed_tier="slow",
                quality_tier="expert"
            ),
            "claude-3.5-sonnet": ModelCapability(
                provider=ModelProvider.ANTHROPIC,
                model_id="claude-3-5-sonnet-20241022",
                context_window=200000,
                supports_vision=True,
                supports_function_calling=True,
                cost_per_1k_tokens=0.003,
                speed_tier="medium",
                quality_tier="excellent"
            ),
            "claude-3-haiku": ModelCapability(
                provider=ModelProvider.ANTHROPIC,
                model_id="claude-3-haiku-20240307",
                context_window=200000,
                supports_vision=True,
                supports_function_calling=True,
                cost_per_1k_tokens=0.00025,
                speed_tier="fast",
                quality_tier="good"
            ),
            "gemini-2.0-flash": ModelCapability(
                provider=ModelProvider.GOOGLE,
                model_id="gemini-2.0-flash-exp",
                context_window=1000000,
                supports_vision=True,
                supports_function_calling=True,
                cost_per_1k_tokens=0.0001,
                speed_tier="fast",
                quality_tier="excellent"
            ),
            "grok-beta": ModelCapability(
                provider=ModelProvider.XAI,
                model_id="grok-beta",
                context_window=128000,
                supports_vision=False,
                supports_function_calling=True,
                cost_per_1k_tokens=0.005,
                speed_tier="medium",
                quality_tier="good"
            )
        }

    def analyze_task(
        self,
        message: str,
        conversation_history: List[Dict[str, str]] = None
    ) -> TaskAnalysis:
        """
        Analyze a task to understand its requirements.

        Returns TaskAnalysis with complexity, type, and requirements.
        """
        # Count tokens
        tokens = len(self.tokenizer.encode(message))
        if conversation_history:
            for msg in conversation_history:
                tokens += len(self.tokenizer.encode(msg.get("content", "")))

        # Detect task type (simple keyword matching for MVP)
        task_type = self._classify_task_type(message)

        # Estimate complexity
        complexity = self._estimate_complexity(message, tokens)

        # Detect special requirements
        requires_vision = any(word in message.lower() for word in ["image", "picture", "photo", "visual", "diagram"])
        requires_tools = any(word in message.lower() for word in ["search", "web", "current", "latest", "today"])

        return TaskAnalysis(
            complexity=complexity,
            task_type=task_type,
            estimated_tokens=tokens,
            requires_vision=requires_vision,
            requires_tools=requires_tools,
            requires_realtime=requires_tools,
            context_length=tokens
        )

    def route(
        self,
        task_analysis: TaskAnalysis,
        available_providers: List[ModelProvider],
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> RoutingDecision:
        """
        Make routing decision based on task analysis and available models.

        This is the core CarPool logic - picking the right vehicle for the journey.
        """
        # Filter models by availability
        available_models = {
            model_id: cap
            for model_id, cap in self.model_capabilities.items()
            if cap.provider in available_providers
        }

        if not available_models:
            raise ValueError("No models available for routing")

        # Filter by requirements
        candidates = available_models.copy()

        if task_analysis.requires_vision:
            candidates = {k: v for k, v in candidates.items() if v.supports_vision}

        if task_analysis.requires_tools:
            candidates = {k: v for k, v in candidates.items() if v.supports_function_calling}

        if not candidates:
            # Fallback to best available
            candidates = available_models

        # Score each model
        scored_models = []
        for model_id, capability in candidates.items():
            score = self._score_model(task_analysis, capability, user_preferences)
            scored_models.append((model_id, capability, score))

        # Sort by score (descending)
        scored_models.sort(key=lambda x: x[2], reverse=True)

        # Select winner
        selected_id, selected_cap, selected_score = scored_models[0]

        # Build reasoning
        reasoning = self._build_reasoning(task_analysis, selected_cap, selected_score)

        # Alternatives
        alternatives = [model_id for model_id, _, _ in scored_models[1:4]]

        return RoutingDecision(
            selected_model=selected_id,
            selected_provider=selected_cap.provider,
            reasoning=reasoning,
            alternatives=alternatives,
            estimated_cost=task_analysis.estimated_tokens * selected_cap.cost_per_1k_tokens / 1000,
            confidence_score=selected_score
        )

    def _classify_task_type(self, message: str) -> TaskType:
        """Classify task type from message content"""
        msg_lower = message.lower()

        if any(word in msg_lower for word in ["code", "function", "debug", "implement", "program"]):
            return TaskType.CODE
        if any(word in msg_lower for word in ["analyze", "data", "compare", "evaluate"]):
            return TaskType.ANALYSIS
        if any(word in msg_lower for word in ["write", "create", "story", "poem", "article"]):
            return TaskType.CREATIVE
        if any(word in msg_lower for word in ["image", "picture", "video", "audio"]):
            return TaskType.MULTIMODAL
        if any(word in msg_lower for word in ["solve", "calculate", "prove", "logic"]):
            return TaskType.REASONING
        if any(word in msg_lower for word in ["current", "latest", "today", "news"]):
            return TaskType.REALTIME

        return TaskType.CHAT

    def _estimate_complexity(self, message: str, tokens: int) -> TaskComplexity:
        """Estimate task complexity"""
        # Simple heuristic for MVP
        if tokens < 100:
            return TaskComplexity.TRIVIAL
        if tokens < 500:
            return TaskComplexity.SIMPLE
        if tokens < 2000:
            return TaskComplexity.MODERATE
        if tokens < 10000:
            return TaskComplexity.COMPLEX
        return TaskComplexity.EXPERT

    def _score_model(
        self,
        task: TaskAnalysis,
        capability: ModelCapability,
        preferences: Optional[Dict[str, Any]]
    ) -> float:
        """
        Score a model for a given task.

        Higher score = better fit.
        """
        score = 0.0

        # Quality match
        quality_scores = {"basic": 1, "good": 2, "excellent": 3, "expert": 4}
        complexity_requirements = {
            TaskComplexity.TRIVIAL: 1,
            TaskComplexity.SIMPLE: 1,
            TaskComplexity.MODERATE: 2,
            TaskComplexity.COMPLEX: 3,
            TaskComplexity.EXPERT: 4
        }

        required_quality = complexity_requirements[task.complexity]
        model_quality = quality_scores[capability.quality_tier]

        if model_quality >= required_quality:
            score += 10
            # Bonus for exact match (don't use GPT-4 for trivial tasks)
            if model_quality == required_quality:
                score += 5
        else:
            score -= 10  # Penalty for insufficient quality

        # Cost efficiency (prefer cheaper when quality is sufficient)
        if model_quality == required_quality:
            # Normalize cost (lower is better)
            score += (0.01 - capability.cost_per_1k_tokens) * 100

        # Speed bonus
        speed_scores = {"fast": 5, "medium": 3, "slow": 0}
        score += speed_scores.get(capability.speed_tier, 0)

        # Context window check
        if task.context_length > capability.context_window:
            score -= 50  # Heavy penalty for insufficient context

        # User preferences
        if preferences:
            prefer_provider = preferences.get("preferred_provider")
            if prefer_provider == capability.provider.value:
                score += 8

        return score

    def _build_reasoning(
        self,
        task: TaskAnalysis,
        capability: ModelCapability,
        score: float
    ) -> str:
        """Build human-readable explanation of routing decision"""
        return (
            f"Selected {capability.model_id} for {task.task_type.value} task "
            f"with {task.complexity.value} complexity. "
            f"Model offers {capability.quality_tier} quality at {capability.speed_tier} speed, "
            f"matching task requirements (score: {score:.1f})."
        )


# Singleton instance
lucidia = LucidiaRouter()
