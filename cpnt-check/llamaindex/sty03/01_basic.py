
from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
)

from llama_index.utils.workflow import draw_all_possible_flows


class MyWorkflow(Workflow):
    @step
    async def my_step(self, ev: StartEvent) -> StopEvent:
        # do something here
        return StopEvent(result="Hello, world!")

draw_all_possible_flows(MyWorkflow, filename="cpnt-check/llamaindex/sty03/basic_workflow.html")
async def main():
    w = MyWorkflow(timeout=10, verbose=False)
    result = await w.run()
    print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
