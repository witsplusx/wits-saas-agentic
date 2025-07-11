
from graphiti_core import Graphiti
from graphiti_core.llm_client.openai_generic_client import OpenAIGenericClient
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig
from graphiti_core.cross_encoder.openai_reranker_client import OpenAIRerankerClient

# Configure OpenAI-compatible service
llm_config = LLMConfig(
    api_key="<your-api-key>",
    model="<your-main-model>",        # e.g., "mistral-large-latest"
    small_model="<your-small-model>", # e.g., "mistral-small-latest"
    base_url="<your-base-url>",       # e.g., "https://api.mistral.ai/v1"
)

# Initialize Graphiti with OpenAI-compatible service
graphiti = Graphiti(
    "bolt://localhost:7687",
    "neo4j",
    "password",
    llm_client=OpenAIGenericClient(config=llm_config),
    embedder=OpenAIEmbedder(
        config=OpenAIEmbedderConfig(
            api_key="<your-api-key>",
            embedding_model="<your-embedding-model>", # e.g., "mistral-embed"
            base_url="<your-base-url>",
        )
    ),
    cross_encoder=OpenAIRerankerClient(
        config=LLMConfig(
            api_key="<your-api-key>",
            model="<your-small-model>",  # Use smaller model for reranking
            base_url="<your-base-url>",
        )
    )
)


