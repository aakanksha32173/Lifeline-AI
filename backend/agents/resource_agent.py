from uagents import Agent, Context, Model
from typing import List, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from browser.browserbase_search import search_resources_with_browserbase


class ResourceSearchRequest(Model):
    query: str
    location: str
    urgency: str = "today"


class ResourceItem(Model):
    name: str
    category: str
    address: Optional[str] = None
    phone: Optional[str] = None
    hours: Optional[str] = None
    eligibility: Optional[str] = None
    source_url: str
    confidence: float


class ResourceSearchResponse(Model):
    results: List[ResourceItem]


resource_agent = Agent(
    name="lifeline_resource_agent",
    seed="lifeline-resource-agent-secret-seed",
    port=8001,
    endpoint=["http://localhost:8001/submit"],
)


@resource_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Resource agent started.")
    ctx.logger.info(f"Agent address: {resource_agent.address}")


@resource_agent.on_message(model=ResourceSearchRequest)
async def handle_search(ctx: Context, sender: str, msg: ResourceSearchRequest):
    ctx.logger.info(f"Received task: {msg.query} near {msg.location}")

    resources = await search_resources_with_browserbase(
        query=msg.query,
        location=msg.location,
    )

    response = ResourceSearchResponse(
        results=[
            ResourceItem(
                name=r.name,
                category=r.category,
                address=r.address,
                phone=r.phone,
                hours=r.hours,
                eligibility=r.eligibility,
                source_url=r.source_url,
                confidence=r.confidence,
            )
            for r in resources
        ]
    )

    await ctx.send(sender, response)
def find_resources_for_cluster(cluster):
    location = cluster.incidents[0].location or "unknown"

    return [
        {
            "name": "Lincoln High School Shelter",
            "type": "shelter",
            "location": "Houston",
            "capacity": 500,
            "available": True
        },
        {
            "name": "Mobile Medical Unit A",
            "type": "medical",
            "location": location,
            "available": True
        }
    ]

if __name__ == "__main__":
    resource_agent.run()