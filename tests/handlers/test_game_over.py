from unittest.mock import AsyncMock, patch

import pytest

from app.handlers.game_over import game_over_command
from tests.util import get_chat


@pytest.mark.asyncio
async def test_no_open_game():
    tester = await get_chat({"users": {"@aaa": {"data": 1}}, "active_users": ["@aaa"]})
    assert await game_over_command(tester.update, tester.context)
    tester.assert_reply_text(text="No hay ningún juego abierto.")


@pytest.mark.asyncio
async def test_has_a_winner():
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}, "@bbb": {}},
            "active_users": ["@aaa", "@bbb"],
            "cycles": [
                {
                    "users": ["@aaa", "@bbb"],
                    "points": {
                        "@aaa": {"message_id": 1111, "value": 1},
                        "@bbb": {"message_id": 1111, "value": 2},
                    },
                }
            ],
        }
    )
    bot = AsyncMock()
    tester.update.get_bot = lambda: bot
    await game_over_command(tester.update, tester.context)
    bot.send_message.assert_called_once_with(chat_id=1, text="Tenemos un ganador @aaa")


@pytest.mark.asyncio
async def test_a_new_cycle():
    tester = await get_chat(
        {
            "users": {"@aaa": {"data": 1}, "@bbb": {}, "@ccc": {}},
            "active_users": ["@aaa", "@bbb", "@ccc"],
            "cycles": [
                {
                    "users": ["@aaa", "@bbb", "@ccc"],
                    "points": {
                        "@aaa": {"message_id": 1111, "value": 1},
                        "@bbb": {"message_id": 1111, "value": 1},
                        "@ccc": {"message_id": 1111, "value": 2},
                    },
                }
            ],
        }
    )
    bot = AsyncMock()
    tester.update.get_bot = lambda: bot
    await game_over_command(tester.update, tester.context)
    bot.send_message.assert_called_once_with(chat_id=1, text="Desempate @aaa @bbb")