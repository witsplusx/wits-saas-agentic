
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from logging import INFO, DEBUG

from dotenv import load_dotenv

from graphiti_core import Graphiti
from graphiti_core.driver.falkordb_driver import FalkorDriver
from graphiti_core.nodes import EpisodeType
from graphiti_core.search.search_config_recipes import NODE_HYBRID_SEARCH_RRF
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.llm_client.openai_client import OpenAIClient
from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig
from graphiti_core.cross_encoder.openai_reranker_client import OpenAIRerankerClient
from graphiti_core.search.search_filters import SearchFilters


# Custom Entity Types
class Person(BaseModel):
    """A person entity with biographical information."""
    age: Optional[int] = Field(None, description="Age of the person")
    occupation: Optional[str] = Field(None, description="Current occupation")
    location: Optional[str] = Field(None, description="Current location")
    birth_date: Optional[datetime] = Field(None, description="Date of birth")

class Company(BaseModel):
    """A business organization."""
    industry: Optional[str] = Field(None, description="Primary industry")
    founded_year: Optional[int] = Field(None, description="Year company was founded")
    headquarters: Optional[str] = Field(None, description="Location of headquarters")
    employee_count: Optional[int] = Field(None, description="Number of employees")

class Product(BaseModel):
    """A product or service."""
    category: Optional[str] = Field(None, description="Product category")
    price: Optional[float] = Field(None, description="Price in USD")
    release_date: Optional[datetime] = Field(None, description="Product release date")

# Custom Edge Types
class Employment(BaseModel):
    """Employment relationship between a person and company."""
    position: Optional[str] = Field(None, description="Job title or position")
    start_date: Optional[datetime] = Field(None, description="Employment start date")
    end_date: Optional[datetime] = Field(None, description="Employment end date")
    salary: Optional[float] = Field(None, description="Annual salary in USD")
    is_current: Optional[bool] = Field(None, description="Whether employment is current")

class Investment(BaseModel):
    """Investment relationship between entities."""
    amount: Optional[float] = Field(None, description="Investment amount in USD")
    investment_type: Optional[str] = Field(None, description="Type of investment (equity, debt, etc.)")
    stake_percentage: Optional[float] = Field(None, description="Percentage ownership")
    investment_date: Optional[datetime] = Field(None, description="Date of investment")

class Partnership(BaseModel):
    """Partnership relationship between companies."""
    partnership_type: Optional[str] = Field(None, description="Type of partnership")
    duration: Optional[str] = Field(None, description="Expected duration")
    deal_value: Optional[float] = Field(None, description="Financial value of partnership")


entity_types = {
    "Person": Person,
    "Company": Company,
    "Product": Product
}

edge_types = {
    "Employment": Employment,
    "Investment": Investment,
    "Partnership": Partnership
}

edge_type_map = {
    ("Person", "Company"): ["Employment"],
    ("Company", "Company"): ["Partnership", "Investment"],
    ("Person", "Person"): ["Partnership"],
    ("Entity", "Entity"): ["Investment"],  # Apply to any entity type
}

# Configure logging
logging.basicConfig(
    level=DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)

load_dotenv()

# Configure Ollama LLM client
llm_config = LLMConfig(
    api_key="abc",  # Ollama doesn't require a real API key
    model="qwen3:14b",
    small_model="qwen3:14b",
    base_url="http://localhost:11434/v1",  # Ollama provides this port
)
llm_client = OpenAIClient(config=llm_config)

# falkor_driver = FalkorDriver(
#   host='127.0.0.1', port=6779, username=None, password=None)
# falkor_driver._get_graph('witsmt_demo1')

async def main():
    
  graphiti = Graphiti("bolt://127.0.0.1:7687",
    "admin",
    "73@TuGraph",
    llm_client=llm_client,
    embedder=OpenAIEmbedder(
        config=OpenAIEmbedderConfig(
            api_key="abc",
            embedding_model="dengcao/Qwen3-Embedding-4B:Q8_0",
            embedding_dim=2048,
            base_url="http://localhost:11434/v1",
        )
    ),
    cross_encoder=OpenAIRerankerClient(client=llm_client, config=llm_config)
  )
  graphiti.database = "witsmt_demo1"

  await graphiti.add_episode(
      name= "Business Update",
      episode_body= "Sarah joined TechCorp as CTO in January 2023 with a $200K salary. TechCorp partnered with DataCorp in a $5M deal.",
      source_description= "Business news",
      reference_time= datetime.now(),
      entity_types= entity_types,
      edge_types= edge_types,
  )

  # Search for only specific entity types
  search_filter = SearchFilters(
      node_labels=["Person", "Company"]  # Only return Person and Company entities
  )
  results = await graphiti.search_(
      query="Who works at tech companies?",
      search_filter=search_filter
  )
  print(results)

  # Search for only specific edge types
  search_filter = SearchFilters(
      edge_types=["Employment", "Partnership"]  # Only return Employment and Partnership edges
  )
  results = await graphiti.search_(
      query="Tell me about business relationships",
      search_filter=search_filter
  )
  print(results)

if __name__ == '__main__':
    asyncio.run(main())






