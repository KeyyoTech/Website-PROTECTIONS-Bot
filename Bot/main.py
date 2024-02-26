import nextcord
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents = nextcord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Adding some common bad words
bad_words = [
    "fuck",
    "shit",
    "asshole",
    "bitch",
    "bastard",
    "cunt",
    "dick",
    "piss",
    "motherfucker",
    "nigga",
    "mf",
    "pis",
    "dck",
    "niggers",
    "niga",
    "your mom",
    "tf",
    "t fuck",
    "the fuck",  # Added "nigga" to the list
    # Add more bad words as needed
]

# Dictionary to store warnings for each user
warnings = {}

logging = True
logschannel = 1211241581961814046
warn_limit = 5  # Set the number of warnings after which the user should be banned or kicked
auto_role_id = 1208430350683082752  # Set the ID of the auto role

@bot.event
async def on_ready():
    print(f"{bot.user.name} Is Ready!")

@bot.event
async def on_member_join(member):
    # Assign the auto role to the member
    auto_role = member.guild.get_role(auto_role_id)
    if auto_role:
        await member.add_roles(auto_role)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Prevent the bot from replying to its own messages

    if not message.author.bot:
        for word in bad_words:
            if word in message.content.lower():
                # Increment the user's warnings count
                warnings[message.author.id] = warnings.get(message.author.id, 0) + 1
                
                await message.delete()
                await message.channel.send(f"{message.author.mention}, Please refrain from using inappropriate language. Warning {warnings[message.author.id]}")
                if logging and warnings[message.author.id] >= warn_limit:
                    log_channel = bot.get_channel(logschannel)
                    await log_channel.send(f"{message.author.mention} was banned for reaching {warn_limit} warnings.")
                    await message.author.ban(reason="Reached warning limit for using bad language")
                break  # Stop checking for bad words once one is found
        if message.content.lower().startswith("botwho"):
            await message.channel.send("Developer of this bot is @chriss_j")

    await bot.process_commands(message)

@bot.slash_command()
async def kick(interaction: nextcord.Interaction, user: nextcord.Member, reason: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You are not authorized to run this command.", ephemeral=True)
    else:
        await interaction.response.send_message(f"Kicked {user.mention}", ephemeral=True)
        if logging:
            log_channel = bot.get_channel(logschannel)
            await log_channel.send(f"{user.mention} was kicked by {interaction.user.mention} for {reason}")
        await user.kick(reason=reason)

@bot.slash_command()
async def ban(interaction: nextcord.Interaction, user: nextcord.Member, reason: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You are not authorized to run this command.", ephemeral=True)
    else:
        await interaction.response.send_message(f"Banned {user.mention}", ephemeral=True)
        if logging:
            log_channel = bot.get_channel(logschannel)
            await log_channel.send(f"{user.mention} was banned by {interaction.user.mention} for **{reason}**")
        await user.ban(reason=reason)

@bot.slash_command()
async def unban(interaction: nextcord.Interaction, user: nextcord.Member):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You are not authorized to run this command.", ephemeral=True)
    else:
        await interaction.response.send_message(f"Unbanned {user.mention}", ephemeral=True)
        if logging:
            log_channel = bot.get_channel(logschannel)
            await log_channel.send(f"{user.mention} was unbanned by {interaction.user.mention}")
        await interaction.guild.unban(user)

bot.run("MTIxMTIxODc0NzIwNjEzOTk1NQ.G71hMV.uOyKKG19_OL8qLSl6e9R7oEUJL080GThHpoG4k")
