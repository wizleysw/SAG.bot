from datetime import date
import config
import discord


def main():
    client = discord.Client()

    @client.event
    async def on_ready():        
        channel_id = 0
        for guild in client.guilds:
            if guild.name == config.DISCORD_GUILD_NAME:
                for channel in guild.channels:
                    if channel.name == config.DISCORD_CHANNEL_NAME:
                        channel_id = channel.id
                        break
            else: continue
        channel = client.get_channel(channel_id)

        import bot_discord
        msg = f'```js\n[{date.today()}]\n{bot_discord.run()}\n```'
        print(msg)

        for index in range(0, len(msg), 2000):
            await channel.send(msg[ index : index + 2000 ])

        exit(0)

    client.run(config.DISCORD_TOKEN)


if __name__ == "__main__":
    main()
