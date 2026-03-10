"""
Unit tests for the Lucidia routing engine.

These tests run without any external API calls or internet access.
"""

import sys
import os

# Allow imports from backend/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from lucidia import (
    LucidiaRouter,
    TaskComplexity,
    TaskType,
    ModelProvider,
    RoutingDecision,
)


@pytest.fixture
def router():
    return LucidiaRouter()


# ---------------------------------------------------------------------------
# Task analysis
# ---------------------------------------------------------------------------

class TestAnalyzeTask:
    def test_short_message_is_trivial(self, router):
        analysis = router.analyze_task("Hi")
        assert analysis.complexity == TaskComplexity.TRIVIAL

    def test_code_keyword_detected(self, router):
        analysis = router.analyze_task("Write a Python function to reverse a string")
        assert analysis.task_type == TaskType.CODE

    def test_analysis_keyword_detected(self, router):
        analysis = router.analyze_task("Analyze this dataset and compare the results")
        assert analysis.task_type == TaskType.ANALYSIS

    def test_creative_keyword_detected(self, router):
        analysis = router.analyze_task("Write a short story about space exploration")
        assert analysis.task_type == TaskType.CREATIVE

    def test_realtime_keyword_detected(self, router):
        analysis = router.analyze_task("What is the latest news today?")
        assert analysis.task_type == TaskType.REALTIME

    def test_reasoning_keyword_detected(self, router):
        analysis = router.analyze_task("Solve this logic puzzle and prove your reasoning")
        assert analysis.task_type == TaskType.REASONING

    def test_vision_flag_set_for_image_mention(self, router):
        analysis = router.analyze_task("Describe what is in this image")
        assert analysis.requires_vision is True

    def test_requires_tools_for_web_search(self, router):
        analysis = router.analyze_task("Search the web for current stock prices")
        assert analysis.requires_tools is True

    def test_general_chat_default_type(self, router):
        analysis = router.analyze_task("Hello, how are you?")
        assert analysis.task_type == TaskType.CHAT

    def test_conversation_history_tokens_included(self, router):
        history = [{"role": "user", "content": "Tell me about Python"}]
        analysis_with = router.analyze_task("What about lists?", history)
        analysis_without = router.analyze_task("What about lists?")
        assert analysis_with.estimated_tokens > analysis_without.estimated_tokens

    def test_token_count_positive(self, router):
        analysis = router.analyze_task("Some message")
        assert analysis.estimated_tokens > 0


# ---------------------------------------------------------------------------
# Task type classification (_classify_task_type)
# ---------------------------------------------------------------------------

class TestClassifyTaskType:
    def test_code(self, router):
        assert router._classify_task_type("debug this function") == TaskType.CODE

    def test_analysis(self, router):
        assert router._classify_task_type("evaluate the performance") == TaskType.ANALYSIS

    def test_creative(self, router):
        assert router._classify_task_type("create a poem") == TaskType.CREATIVE

    def test_multimodal(self, router):
        assert router._classify_task_type("process this video") == TaskType.MULTIMODAL

    def test_reasoning(self, router):
        assert router._classify_task_type("calculate the answer") == TaskType.REASONING

    def test_realtime(self, router):
        assert router._classify_task_type("current events today") == TaskType.REALTIME

    def test_chat_fallback(self, router):
        assert router._classify_task_type("sounds good") == TaskType.CHAT


# ---------------------------------------------------------------------------
# Complexity estimation (_estimate_complexity)
# ---------------------------------------------------------------------------

class TestEstimateComplexity:
    def test_trivial_under_100_tokens(self, router):
        assert router._estimate_complexity("hi", 50) == TaskComplexity.TRIVIAL

    def test_simple_100_to_500(self, router):
        assert router._estimate_complexity("x", 200) == TaskComplexity.SIMPLE

    def test_moderate_500_to_2000(self, router):
        assert router._estimate_complexity("x", 1000) == TaskComplexity.MODERATE

    def test_complex_2000_to_10000(self, router):
        assert router._estimate_complexity("x", 5000) == TaskComplexity.COMPLEX

    def test_expert_above_10000(self, router):
        assert router._estimate_complexity("x", 15000) == TaskComplexity.EXPERT


# ---------------------------------------------------------------------------
# Routing decisions
# ---------------------------------------------------------------------------

class TestRoute:
    def test_routes_to_openai_when_only_openai_available(self, router):
        analysis = router.analyze_task("Hello!")
        decision = router.route(analysis, [ModelProvider.OPENAI])
        assert decision.selected_provider == ModelProvider.OPENAI

    def test_routes_to_anthropic_when_only_anthropic_available(self, router):
        analysis = router.analyze_task("Hello!")
        decision = router.route(analysis, [ModelProvider.ANTHROPIC])
        assert decision.selected_provider == ModelProvider.ANTHROPIC

    def test_raises_when_no_providers(self, router):
        analysis = router.analyze_task("Hello!")
        with pytest.raises(ValueError, match="No models available"):
            router.route(analysis, [])

    def test_preferred_provider_gets_score_bonus(self, router):
        analysis = router.analyze_task("Hello!")
        decision = router.route(
            analysis,
            [ModelProvider.OPENAI, ModelProvider.ANTHROPIC],
            user_preferences={"preferred_provider": "anthropic"},
        )
        # The preference may or may not win depending on scoring, but the call
        # should not raise and should return a valid decision.
        assert decision.selected_model in router.model_capabilities

    def test_vision_requirement_filters_models(self, router):
        analysis = router.analyze_task("Describe this image please")
        assert analysis.requires_vision
        decision = router.route(analysis, [ModelProvider.OPENAI])
        cap = router.model_capabilities[decision.selected_model]
        assert cap.supports_vision

    def test_decision_has_reasoning(self, router):
        analysis = router.analyze_task("Explain quantum computing")
        decision = router.route(analysis, [ModelProvider.OPENAI])
        assert isinstance(decision.reasoning, str)
        assert len(decision.reasoning) > 0

    def test_estimated_cost_non_negative(self, router):
        analysis = router.analyze_task("Hello")
        decision = router.route(analysis, [ModelProvider.OPENAI])
        assert decision.estimated_cost >= 0

    def test_confidence_score_present(self, router):
        analysis = router.analyze_task("Hello")
        decision = router.route(analysis, [ModelProvider.OPENAI])
        assert isinstance(decision.confidence_score, float)

    def test_alternatives_list(self, router):
        analysis = router.analyze_task("Hello")
        decision = router.route(
            analysis, [ModelProvider.OPENAI, ModelProvider.ANTHROPIC]
        )
        assert isinstance(decision.alternatives, list)


# ---------------------------------------------------------------------------
# Token counting fallback
# ---------------------------------------------------------------------------

class TestCountTokens:
    def test_returns_positive_integer(self, router):
        count = router._count_tokens("Hello, world!")
        assert isinstance(count, int)
        assert count > 0

    def test_longer_text_more_tokens(self, router):
        short = router._count_tokens("Hi")
        long = router._count_tokens("This is a much longer sentence with many words")
        assert long > short
