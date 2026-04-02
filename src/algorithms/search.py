from __future__ import annotations

from typing import Any, NewType


JsonRef = NewType("JsonRef", str)


def _get_all_json_refs(item: Any) -> set[JsonRef]:
    """Get all the definitions references from a JSON schema."""
    refs: set[JsonRef] = set()
    stack: list[Any] = [item]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            for key, value in current.items():
                if key == "$ref" and isinstance(value, str):
                    # the isinstance check ensures that '$ref' isn't the name of a property, etc.
                    refs.add(JsonRef(value))
                elif isinstance(value, dict):
                    stack.append(value)
                elif isinstance(value, list):
                    stack.extend(value)
        elif isinstance(current, list):
            stack.extend(current)
    return refs


def sort_chat_inputs_first(self, vertices_layers: list[list[str]]) -> list[list[str]]:
    """Sort vertices to prioritize chat inputs in the first layer."""
    # First check if any chat inputs have dependencies
    for layer in vertices_layers:
        for vertex_id in layer:
            if "ChatInput" in vertex_id and self.get_predecessors(
                self.get_vertex(vertex_id)
            ):
                return vertices_layers

    # If no chat inputs have dependencies, move them to first layer
    chat_inputs_first = []
    for layer in vertices_layers:
        layer_chat_inputs_first = [
            vertex_id for vertex_id in layer if "ChatInput" in vertex_id
        ]
        chat_inputs_first.extend(layer_chat_inputs_first)
        for vertex_id in layer_chat_inputs_first:
            # Remove the ChatInput from the layer
            layer.remove(vertex_id)

    if not chat_inputs_first:
        return vertices_layers

    return [chat_inputs_first, *vertices_layers]
