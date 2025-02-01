import discord
import openai
import anthropic
import os
import dotenv

# Load bot token and API keys
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

# Initialize Discord bot
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

# Initialize OpenAI and Anthropic clients
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
anthropic_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Avoid responding to itself

    if message.content.startswith("!draw"):
        prompt = message.content[len("!draw "):].strip()  # Extract user prompt

        if not prompt:
            await message.channel.send("❗ Please provide a prompt. Example: `!draw a futuristic city skyline`")
            return

        try:
            response = openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                n=1
            )
            image_url = response.data[0].url  # Get the image URL
            await message.channel.send(f"🖼️ Here is your image:\n{image_url}")

        except openai.OpenAIError as e:
            await message.channel.send(f"❌ Error generating image: {e}")

    elif message.content.startswith("!gpt"):
        prompt = message.content[len("!gpt "):].strip()  # Extract prompt

        if not prompt:
            await message.channel.send("❗ Please provide a prompt. Example: `!gpt Tell me a joke`")
            return

        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200
            )
            reply = response.choices[0].message.content  # Extract response
        except openai.OpenAIError as e:
            reply = f"❌ Error: {e}"

        await message.channel.send(reply)

    elif message.content.startswith("!claude"):  # Use "!claude" to trigger the bot
        prompt = message.content[len("!claude "):]  # Remove command prefix
        
        try:
            response = anthropic_client.messages.create(
                 model="claude-3-5-sonnet-20241022",  # Use the latest Claude model
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            reply = response.content[0].text  # Extract response
        except Exception as e:
            reply = f"Error: {e}"
        
        await message.channel.send(reply)
        
    elif message.content.startswith("!claude-opus"):
        prompt = message.content[len("!claude-opus "):].strip()  # Extract prompt

        if not prompt:
            await message.channel.send("❗ Please provide a prompt. Example: `!claude-opus Summarize this article`")
            return

        try:
            response = anthropic_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            reply = response.content  # Extract response
        except anthropic.AnthropicError as e:
            reply = f"❌ Error: {e}"

        await message.channel.send(reply)

    elif message.content.startswith("!claude-haiku"):
        prompt = message.content[len("!claude-haiku "):].strip()  # Extract prompt

        if not prompt:
            await message.channel.send("❗ Please provide a prompt. Example: `!claude-haiku Explain gravity`")
            return

        try:
            response = anthropic_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            reply = response.content  # Extract response
        except anthropic.AnthropicError as e:
            reply = f"❌ Error: {e}"

        await message.channel.send(reply)

# Run the bot
client.run(DISCORD_TOKEN)
