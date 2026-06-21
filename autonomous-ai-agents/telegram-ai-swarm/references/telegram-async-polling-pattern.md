# Telegram Bot Adapter — Polling with asyncio

## The problem

`Application.run_polling()` from python-telegram-bot creates its OWN event loop internally. If you call it from inside an `asyncio.run(main())` context, you get:

```
RuntimeError: This event loop is already running
RuntimeError: Cannot close a running event loop
```

## The fix: async polling

Never use `run_polling()`. Do this instead:

```python
async def start(self):
    # Build the application
    self._app = Application.builder().token(self.token).build()
    self._app.add_handler(...)
    
    # Initialize (no new event loop!)
    await self._app.initialize()
    
    # Get bot info
    me = await self._app.bot.get_me()
    
    # Start polling (async version!)
    await self._app.updater.start_polling(allowed_updates=["message"])
    
    # Keep alive
    while True:
        await asyncio.sleep(3600)

async def stop(self):
    if self._app:
        try:
            await self._app.updater.stop()
        except Exception:
            pass
        await self._app.shutdown()
```

## Message handler pattern

```python
async def _message_handler(self, update: Update, context):
    msg = update.message
    if not msg or not msg.text:
        return
    
    # Convert to normalized event
    event = MessageEvent(
        chat_id=msg.chat.id,
        user_id=msg.from_user.id,
        user_name=msg.from_user.full_name,
        text=msg.text,
        message_id=msg.message_id,
        is_group=msg.chat.type in ("group", "supergroup"),
        is_mention=f"@{bot_username}" in msg.text,
    )
    
    # Pass to your handler
    await self.callback(event)
```

## Sending messages

```python
async def send_reply(self, chat_id, agent_label, text, reply_to_message_id=None):
    full_text = f"{agent_label}\n\n{text}"
    
    # Handle 4096 char limit
    max_len = 4000  # Leave room for label
    if len(full_text) > max_len:
        parts = split_at_sentence_boundary(full_text, max_len)
    else:
        parts = [full_text]
    
    for part in parts:
        await self._bot.send_message(
            chat_id=chat_id,
            text=part,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=reply_to_message_id,
        )
        await asyncio.sleep(0.5)
```

## Filtering messages

In groups:
```python
# Check if bot is mentioned
mention = f"@{bot_username}"
is_mention = mention in msg.text

# Check if replying to bot
is_reply_to_bot = (msg.reply_to_message and 
                   msg.reply_to_message.from_user and 
                   msg.reply_to_message.from_user.is_bot)

# DM: always process
# Group: only process if mentioned or replying to bot
```