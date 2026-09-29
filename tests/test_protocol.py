"""
Tests for the wire protocol. Target: green at the end of stage 1.
These define the contract between the client and the server.
"""
import pytest

import config
from langame.common.protocol import Message, MessageBuffer, MessageType, ProtocolError, answer, join


def test_round_trip():
    original = answer(17, 2)
    line = original.to_wire().decode(config.ENCODING).rstrip(config.MESSAGE_DELIMITER)
    parsed = Message.from_wire(line)
    assert parsed.type is MessageType.ANSWER
    assert parsed.payload == {"question_id": 17, "choice": 2}


def test_wire_ends_with_delimiter():
    assert join("liraz").to_wire().endswith(config.MESSAGE_DELIMITER.encode())


def test_hebrew_survives():
    msg = Message(MessageType.QUESTION, {"text": "מה בירת ישראל?"})
    line = msg.to_wire().decode(config.ENCODING).strip()
    assert Message.from_wire(line).payload["text"] == "מה בירת ישראל?"


@pytest.mark.parametrize("bad", [
    "not json at all",
    '{"payload": {}}',                       # missing type
    '{"type": "DANCE", "payload": {}}',      # unknown type
    '{"type": "JOIN"}',                      # missing payload
    '{"type": "JOIN", "payload": "x"}',      # payload not a dict
])
def test_malformed_raises_protocol_error(bad):
    with pytest.raises(ProtocolError):
        Message.from_wire(bad)


def test_buffer_splits_glued_messages():
    buf = MessageBuffer()
    data = join("a").to_wire() + join("b").to_wire()
    messages = buf.feed(data)
    assert [m.payload["name"] for m in messages] == ["a", "b"]


def test_buffer_reassembles_split_message():
    buf = MessageBuffer()
    data = join("liraz").to_wire()
    first, second = data[:5], data[5:]
    assert buf.feed(first) == []
    messages = buf.feed(second)
    assert len(messages) == 1 and messages[0].payload["name"] == "liraz"


def test_buffer_rejects_oversized_message():
    buf = MessageBuffer()
    with pytest.raises(ProtocolError):
        buf.feed(b"x" * (config.MAX_MESSAGE_BYTES + 1))
