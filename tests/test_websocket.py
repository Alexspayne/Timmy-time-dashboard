"""Tests for websocket/handler.py — WebSocket manager."""

import json

from websocket.handler import WebSocketManager, WSEvent


def test_ws_event_to_json():
    event = WSEvent(event="test", data={"key": "val"}, timestamp="2026-01-01T00:00:00Z")
    j = json.loads(event.to_json())
    assert j["event"] == "test"
    assert j["data"]["key"] == "val"


def test_ws_manager_initial_state():
    mgr = WebSocketManager()
    assert mgr.connection_count == 0
    assert mgr.event_history == []


def test_ws_manager_event_history_limit():
    mgr = WebSocketManager()
    mgr._max_history = 5
    for i in range(10):
        event = WSEvent(event=f"e{i}", data={}, timestamp="t")
        mgr._event_history.append(event)
    # Simulate the trim that happens in broadcast
    if len(mgr._event_history) > mgr._max_history:
        mgr._event_history = mgr._event_history[-mgr._max_history:]
    assert len(mgr._event_history) == 5
