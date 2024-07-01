from __future__ import annotations
from LSP.plugin.core.protocol import Point, Position, Range, Request, Notification
from LSP.plugin.core.transports import encode_json, decode_json
import unittest


LSP_START_POSITION: Position = {'line': 10, 'character': 4}
LSP_END_POSITION: Position = {'line': 11, 'character': 3}
LSP_RANGE: Range = {'start': LSP_START_POSITION, 'end': LSP_END_POSITION}


class PointTests(unittest.TestCase):

    def test_lsp_conversion(self) -> None:
        point = Point.from_lsp(LSP_START_POSITION)
        self.assertEqual(point.row, 10)
        self.assertEqual(point.col, 4)
        lsp_point = point.to_lsp()
        self.assertEqual(lsp_point['line'], 10)
        self.assertEqual(lsp_point['character'], 4)


class EncodingTests(unittest.TestCase):
    def test_encode(self) -> None:
        encoded = encode_json({"text": "😃"})
        self.assertEqual(encoded, b'{"text":"\xF0\x9F\x98\x83"}')
        decoded = decode_json(encoded)
        self.assertEqual(decoded, {"text": "😃"})


class RequestTests(unittest.TestCase):

    def test_initialize(self) -> None:
        req = Request.initialize({"param": 1})
        payload = req.to_payload(1)
        self.assertEqual(payload["jsonrpc"], "2.0")
        self.assertEqual(payload["id"], 1)
        self.assertEqual(payload["method"], "initialize")
        self.assertEqual(payload["params"], {"param": 1})

    def test_shutdown(self) -> None:
        req = Request.shutdown()
        payload = req.to_payload(1)
        self.assertEqual(payload["jsonrpc"], "2.0")
        self.assertEqual(payload["id"], 1)
        self.assertEqual(payload["method"], "shutdown")
        self.assertNotIn('params', payload)


class NotificationTests(unittest.TestCase):

    def test_initialized(self) -> None:
        notification = Notification.initialized()
        payload = notification.to_payload()
        self.assertEqual(payload["jsonrpc"], "2.0")
        self.assertNotIn("id", payload)
        self.assertEqual(payload["method"], "initialized")
        self.assertEqual(payload["params"], dict())

    def test_exit(self) -> None:
        notification = Notification.exit()
        payload = notification.to_payload()
        self.assertEqual(payload["jsonrpc"], "2.0")
        self.assertNotIn("id", payload)
        self.assertEqual(payload["method"], "exit")
        self.assertNotIn('params', payload)
