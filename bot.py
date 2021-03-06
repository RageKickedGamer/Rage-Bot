#A Mod Bot My RageKickedGamer Youtube

import discord
import random
from random import randint
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import time
import datetime
import youtube_dl
import os

bot = commands.Bot(command_prefix = 'r.')
tu = datetime.datetime.now()

@bot.event
async def on_ready():
    print("===================================")
    print("Logged in as")
    print("Username: %s"%bot.user.name)
    print("ID: %s"%bot.user.id)
    print('Server count:', str(len(bot.servers)))
    print('User Count:',len(set(bot.get_all_members())))
    print("Py Lib Version: %s"%discord.__version__)
    print("===================================")
    server = len(bot.servers)
    users = sum(1 for _ in bot.get_all_members())
    while 1==1:
        await bot.change_presence(game=discord.Game(name='with {} servers'.format(server)))
        await asyncio.sleep(10)
        await bot.change_presence(game=discord.Game(name='with {} users'.format(users)))
        await asyncio.sleep(10)                         
        await bot.change_presence(game=discord.Game(name='PREFIX = r.'))
        await asyncio.sleep(10)
        await bot.change_presence(game=discord.Game(name='r.help'))
        await asyncio.sleep(25)

@bot.command(pass_context=True)
async def ping(ctx):
    """See The Bots Ping Time"""
    t1 = time.perf_counter()
    await bot.send_typing(ctx.message.channel)
    t2 = time.perf_counter()
    thedata = (":ping_pong: **Pong.**\nTime: " + str(round((t2 - t1) * 1000)) + "ms")
    color = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
    color = int(color, 16)
    data = discord.Embed(description=thedata, colour=discord.Colour(value=color))

    await bot.say(embed=data)

@bot.command(pass_context=True)
async def lockdown(ctx):
    """Locks Down The Channel.Admin Only Chat"""
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await bot.say("**You Do Not Have The Permissions To Do This!**")
    pass

    try:
        overwrites_everyone = ctx.message.channel.overwrites_for(ctx.message.server.default_role)
        if overwrites_everyone.send_messages == False:
            await bot.say("Channel is already locked down. Use `r.unlock` to unlock.")
            return
        overwrites_everyone.send_messages = False
        await bot.edit_channel_permissions(ctx.message.channel, ctx.message.server.default_role, overwrites_everyone)
        await bot.say("Channel Is :lock: . Only Admins May Speak. Do Not Talk about It In Other Channels!")
    except discord.errors.Forbidden:
        await bot.say("**I Don't Have 'Permission' To Do This.**")

@bot.command(pass_context=True)
async def unlock(ctx):
    """Unlocks Lockdown. Everyone Can Chat"""
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await bot.say("**You Do Not Have The Permissions To Do This!**")
    pass

    try:
        overwrites_everyone = ctx.message.channel.overwrites_for(ctx.message.server.default_role)
        overwrites_staff = ctx.message.channel.overwrites_for(discord.utils.get(ctx.message.server.roles, name="Admin"))
        if overwrites_everyone.send_messages == None:
            await bot.say("Channel is already unlocked.")
            return
        overwrites_everyone.send_messages = None
        overwrites_staff.send_messages = True
        await bot.edit_channel_permissions(ctx.message.channel, ctx.message.server.default_role, overwrites_everyone)
        await bot.edit_channel_permissions(ctx.message.channel, discord.utils.get(ctx.message.server.roles, name="Admin"), overwrites_staff)
        await bot.say("Channel unlocked.")
    except discord.errors.Forbidden:
        await bot.say("**I Don't Have 'Permission' To Do This.**")

@bot.command(pass_context=True)
async def feedback(ctx, *, message : str):
    """Send Feedback To ME!!!"""
    owner = discord.utils.get(bot.get_all_members(), id="342853951353520128")
    server = ctx.message.server
    author = ctx.message.author
    footer = "User ID: " + author.id + " | Server ID: " + server.id
    source = "From {}".format(server)

    colour = discord.Colour.green()

    description = "Sent by {} {}".format(author, source)

    msg = discord.Embed(colour=colour, description=message)
    msg.set_author(name=description)
    msg.set_footer(text=footer)

    await bot.send_message(owner, embed=msg)

@bot.command()
async def userinfo(member : discord.Member):
    """Says when a member joined."""
    em = discord.Embed(color=0x00FFF0) #0xea7938 is the color code
    em.set_thumbnail(url=member.avatar_url)
    em.set_footer(text="Rage Bot v1.0")
    em.add_field(name="Name:", value=member.name)
    em.add_field(name="Discriminator:", value='#{}'.format(member.discriminator))
    em.add_field(name="Nickname:", value=member.nick)
    em.add_field(name="ID:", value=member.id)
    em.add_field(name="Status:", value=member.status)
    em.add_field(name="Game:", value=member.game)
    em.add_field(name='In Voice', value=member.voice_channel)
    em.add_field(name="Account was created at:", value=member.created_at)
    em.add_field(name="Joined this server at:", value=member.joined_at)
    em.add_field(name="Roles:", value='Coming Soon')
    em.add_field(name='Highest Role', value=member.top_role.name)
    await bot.say(embed=em, delete_after = 60)

@bot.command(pass_context = True)
async def kick(ctx, *, member : discord.Member = None):
    '''Kicks A User From The Server'''
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await bot.say("**You Dont Have Permissions To Do That!**")
    pass

    if not ctx.message.author.server_permissions.administrator:
        return
 
    if not member:
        return await bot.say(ctx.message.author.mention + "Specify A User To Kick")
 
    embed = discord.Embed(description = "**%s** has been kicked."%member.name, color = 0xF00000)
    embed.set_footer(text="BasicDiscord Bot v1.0")
    await bot.kick(member)
    await bot.say(embed = embed)

@bot.command(pass_context = True)
async def mute(ctx, *, member : discord.Member):
    '''Mutes A Memeber'''
    if not ctx.message.author.server_permissions.administrator:
        return
    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = False
    await bot.edit_channel_permissions(ctx.message.channel, member, overwrite)

    await bot.say("**%s** is now Muted! Wait For an Unmute.."%member.mention)

@bot.command(pass_context = True)
async def unmute(ctx, *, member : discord.Member):
    '''Unmutes The Muted Memeber'''
    if not ctx.message.author.server_permissions.administrator:
        return
    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = True
    await bot.edit_channel_permissions(ctx.message.channel, member, overwrite)

    await bot.say("**%s** Times up...You are Unmuted!"%member.mention)

@bot.command(pass_context=True)
async def serverinfo(ctx):
    """Shows information about the server"""
    server = ctx.message.server
    online = len([m.status for m in server.members
                    if m.status == discord.Status.online or
                    m.status == discord.Status.idle])
    total_users = len(server.members)
    text_channels = len([x for x in server.channels
                            if x.type == discord.ChannelType.text])
    voice_channels = len(server.channels) - text_channels
    passed = (ctx.message.timestamp - server.created_at).days
    created_at = ("Since {}. That's over {} days ago!"
                    "".format(server.created_at.strftime("%d %b %Y %H:%M"), passed))

    colour = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
    colour = int(colour, 16)
    data = discord.Embed(description=created_at, colour=discord.Colour(value=colour))
    data.add_field(name="Region", value=str(server.region))
    data.add_field(name="Users Online", value="{}/{}".format(online, total_users))
    data.add_field(name="Text Channels", value=text_channels)
    data.add_field(name="Voice Channels", value=voice_channels)
    data.add_field(name="Roles", value=len(server.roles))
    data.add_field(name="Owner", value=str(server.owner))
    data.set_footer(text="Server ID: " + server.id)
    data.add_field(name = "AFK Timeout", value = "{} minutes".format(server.afk_timeout/60).replace(".0", ""))
    data.add_field(name = "AFK Channel", value = str(server.afk_channel))
    data.add_field(name = "Verification Level", value = str(server.verification_level))

    if server.icon_url:
        data.set_author(name=server.name, url=server.icon_url)
        data.set_thumbnail(url=server.icon_url)
    else:
        data.set_author(name=server.name)

    await bot.say(embed=data)

@bot.command(pass_context = True)
async def echo(ctx, *,echo: str):
    '''Makes The Bot Repeat What You Say (Comming Soon)'''
    if ctx.message.author.id == ("342853951353520128"):
        await bot.delete_message(ctx.message)
        await bot.say(echo)

@bot.command(pass_context = True)
async def kill(ctx, member: discord.Member = None, seconds: int=5):
    """Kills a member"""
    if member is None:
        await bot.say(ctx.message.author.mention + ": I can't kill someone unless you give me a name.")
        return
           
    if member.id == bot.user.id:
        await bot.say(ctx.message.author.mention + ": I Just Fucked Your Mom, So That makes me GOD And i Cant DIE!!")
    elif member.id == ctx.message.author.id:
        await bot.say(ctx.message.author.mention + ": Why do you want to die?")
    else:
        await bot.say(ctx.message.author.mention + " is Killing " + member.mention)
        await asyncio.sleep(seconds)
        await bot.say(member.mention + " Is Now Dead! :smiling_imp:")

@bot.command(pass_context = True)
async def restart(ctx):
    '''Turns Bot Offline (Dev. Command Only)'''
    author = ("342853951353520128")
    if author == ctx.message.author.id:
            await bot.say("**Im Temporarily Offline**")
            await bot.logout()
            exit()

@bot.command(pass_context=True)
async def botclear(ctx):
    '''Clears Bot Only Merssages'''
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await bot.say("**You Do Not Have Permissions To Do That!**")
    pass

    def is_bot_message(msg):
        return msg.author == bot.user
    await bot.purge_from(ctx.message.channel, limit=99999, check=is_bot_message)

@bot.command(pass_context=True)       
async def clear(ctx, number):
    '''Clears The Chat 2-100'''
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await bot.say("**You Do Not Have Permissions To Do That!**")
    mgs = []
    number = int(number)
    async for x in bot.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await bot.delete_messages(mgs)

@bot.command(pass_context=True)
async def embed(ctx, *, content : str=""):
    """Embeds the chosen message"""
    message = ctx.message
    if content == "":
        await bot.say("```md\n[ Command failed to execute ][ ArgumentError ]\n< Required argument was not defined >\n```")
    else:
        try:
            data = discord.Embed(colour=discord.Colour.purple())
            data.add_field(name=message.author.display_name + "#" + message.author.discriminator + " Embeded", value=str(content))
            await bot.delete_message(message)
            await bot.say(embed=data)
        except:
            await bot.edit_message(message, "```md\n[ Command failed to execute ][ PermissionsError ]\n< We do not have the embed links permission so we cannot perform the task >\n```")

@bot.command()
async def uptime():
    """Check bot uptime."""
    global tu
    await bot.say(timedelta_str(datetime.datetime.now() - tu))

#Convert uptime to a string.
def timedelta_str(dt):
    days = dt.days
    hours, r = divmod(dt.seconds, 3600)
    minutes, sec = divmod(r, 60)

    if minutes == 1 and sec == 1:
        return '{0} days, {1} hours, {2} minute and {3} second.'.format(days,hours,minutes,sec)
    elif minutes > 1 and sec == 1:
        return '{0} days, {1} hours, {2} minutes and {3} second.'.format(days,hours,minutes,sec)
    elif minutes == 1 and sec > 1:
        return '{0} days, {1} hours, {2} minute and {3} seconds.'.format(days,hours,minutes,sec)
    else:
        return '{0} days, {1} hours, {2} minutes and {3} seconds.'.format(days,hours,minutes,sec)

@bot.command(pass_context = True, no_pm = True)
async def announce(ctx, *, announcement: str):
    """Sends an Embed Titled Announcement"""
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await bot.say("**You Do Not Have Permissions To Do That!**")
    pass

    embed=discord.Embed(title = "__Announcement__", description= announcement, color = 0xFF0000)
    await bot.delete_message(ctx.message)
    await bot.say(embed = embed)

@bot.command(pass_context=True)
async def rr(ctx):
    """Russian Roulette."""
    bullet = random.randint(1, 6)
    await bot.say(':gun: The chambers have been spun.')
    await asyncio.sleep(2)
    pulltrig = 'You pull the trigger, and...\n'
    if bullet == 1:
        await bot.say(pulltrig + ':tada: BANG!\nA bullet went straight into your head. lol')
    else:
        await bot.say(pulltrig + '*Click*\nYou live. At least for now.')

@bot.command(pass_context=True)
async def avatar(ctx):
    """Get Your Avatar"""
    author = ctx.message.author
    em = discord.Embed(color=author.color)
    em.add_field(name="{}'s Avatar".format(author), value=("{}'s Avatar".format(author.mention)))
    em.add_field(name="\a", value=(":globe_with_meridians: Download avatar [here!]({})".format(author.avatar_url)))
    em.set_thumbnail(url=author.avatar_url)
    await bot.say(embed=em)
    
@bot.command(no_pm=True, pass_context=True)
async def addrole(ctx, rolename, user: discord.Member=None):
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await bot.say("**You Do Not Have Permissions To Do That!**")
    pass

    author = ctx.message.author
    channel = ctx.message.channel
    server = ctx.message.server
    role = discord.utils.find(lambda r: r.name.lower() == rolename.lower(), ctx.message.server.roles)
    if user is None:
        user = author

    if role is None:
        await bot.say('That role cannot be found.')
        return

    if not channel.permissions_for(server.me).manage_roles:
        await bot.say('I don\'t have manage_roles.')
        return

    await bot.add_roles(user, role)
    await bot.say('Added role {} to {}'.format(role.name, user.name))

@bot.command(no_pm=True, pass_context=True)
async def remrole(ctx, rolename, user: discord.Member=None):
    """Removes a Role From a Specified Person"""
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await bot.say("You don't have permission -OR- You dont have the role Admin")
    pass

    author = ctx.message.author
    channel = ctx.message.channel
    server = ctx.message.server
    role = discord.utils.find(lambda r: r.name.lower() == rolename.lower(), ctx.message.server.roles)
    if user is None:
        user = author

    if role is None:
        await bot.say('That role cannot be found.')
        return

    if not channel.permissions_for(server.me).manage_roles:
        await bot.say('I don\'t have manage_roles.')
        return
    if discord.errors.Forbidden is True:
        await bot.say("Missing Permissions Bitch :smiling_imp: ")

    await bot.remove_roles(user, role)
    await bot.say('Removed Role {} From {}'.format(role.name, user.name))

@bot.command(pass_context=True)
async def setstat(ctx, status=None, *, game=None):
    """Sets The Bots Stats"""
    if ctx.message.author.id == ("342853951353520128"):
        statuses = {
            "online": discord.Status.online,
            "idle": discord.Status.idle,
            "dnd": discord.Status.dnd,
            "invis": discord.Status.invisible
            }

    current_game = ctx.message.server.me.game if ctx.message.server is not None else None
        
    if status is not None and game is None:
            s = statuses.get(status.lower(), None)
            if s:
                    await bot.change_presence(status=s, game=current_game)
                    await bot.say("Successfully changed the status to `{}`".format(status))
                    
@bot.command(pass_context=True)
async def poll(ctx,*, message: str):
    embed = discord.Embed(color = ctx.message.author.color, timestamp = datetime.datetime.utcnow())
    embed.set_author(name = "Poll", icon_url = ctx.message.author.avatar_url)
    embed.description = (message)
    embed.set_footer(text = ctx.message.author.name)
    x = await bot.say(embed = embed)
    await bot.add_reaction(x, "👍")
    await bot.add_reaction(x, "\U0001f937")
    await bot.add_reaction(x, "👎")
    
@bot.command()
async def botinfo():
    """Get Info About The Bot"""
    em = discord.Embed(color=0xea7938) #0xea7938 is the color code
    em.add_field(name='Bot Info', value="This bot was created with the library Discord.py\n If you need any help or questions, join the [devs' server](https://discord.gg/km9Yudr)")
    em.add_field(name='Total Commands', value=(len(bot.commands)))
    em.add_field(name = 'Add Me On Steam', value = '[Steam](http://steamcommunity.com/id/RageKickedGamer/)')
    em.add_field(name = 'Invite Me!', value = '[Click Here](https://discordbots.org/bot/386637469438836738)')
    em.set_footer(text="Rage Bot v1.0")
    await bot.say(embed = em)

@bot.command(pass_context = True)
async def gbans(ctx):
    '''Gets A List Of Users Who Are No Longer With us'''
    x = await bot.get_bans(ctx.message.server)
    x = '\n'.join([y.name for y in x])
    embed = discord.Embed(title = "List of The Banned Idiots", description = x, color = 0xFFFFF)
    embed.set_footer(text="Rage Bot v1.0")
    return await bot.say(embed = embed)

@bot.command(pass_context=True)
async def count(ctx):
    """The Amout of users/servers"""
    users = len(set(bot.get_all_members()))
    servers = len(bot.servers)
    await bot.say("**I'm in {} Servers and with {} Members and counting!** You Can Add Me By Typing 'r.botinfo'".format(servers, users))
    
@bot.command(pass_context=True)
async def guess(ctx):
    """Allows user to guess a "randomly" generated 1 to 10 digit."""
    author = ctx.message.author

    await bot.say(
        ('<@{}> Guess a number between 1 to 10 (Answer within 20 seconds)' +
         ' [Make sure to mention me!]')
        .format(author.id))

    start_string = '<@{}>'.format(str(bot.user.id))
    start_string2 = '<@!{}>'.format(str(bot.user.id))

    def format_response(m):
        m = m.strip(' ')
        if m.startswith(start_string):
            m = m[len(start_string):].strip(' ')
        else:
             m = m[len(start_string2):].strip(' ')
        return m

    def guess_check(m):
        m = m.content.strip(' ')
        print("Checking Guess...")
        if m.startswith(start_string) or m.startswith(start_string2):
            print("Startswith...")
            m = format_response(m)
            return m.isdigit()
        else:
            return False

    guess = await bot.wait_for_message(timeout=20.0, author=author,
                                          check=guess_check)

    answer = random.randint(1, 10)
    if guess is None:
        fmt = ('Sorry <@{}> , you took too long. It was {}.'
               .format(str(author.id), answer))
        await bot.say(fmt)
        return

    guess_text = format_response(guess.content)
    if int(guess_text) == answer:
        fmt = ('You are right, <@{}>!').format(str(author.id))
        await bot.say(fmt)
    else:
        fmt = ('Sorry, <@{}>. It is actually {}.'
               .format(str(author.id), answer))
        await bot.say(fmt)

@bot.command(pass_context=True)
async def purge(ctx):
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" not in user_roles:
        return await bot.say("**You Dont Have Permissions To Do That!**")
    pass

    await bot.say("Are you sure you want to clear the channel's history, yes or no?")
    response = await bot.wait_for_message(timeout=10, author=ctx.message.author, channel=ctx.message.channel)
    response = response.content.lower()
    if response == "yes" or response == "y":
        await bot.purge_from(ctx.message.channel, limit=99999)

@bot.command(pass_context=True)
async def roleinfo(ctx, *,role: discord.Role):
    embed = discord.Embed(color = role.color)
    embed.set_author(name = "The role info")
    embed.add_field(name = "Role Name", value = format(role.name))
    embed.add_field(name = "Role ID", value = format(role.id))
    embed.add_field(name = "For Server", value = format(role.server))
    embed.add_field(name = "Hoist", value = format(role.hoist))
    embed.add_field(name = "Role Position", value = format(role.position))
    embed.add_field(name = "Mentionable Role", value = format(role.mentionable))
    embed.add_field(name = "Role Created At", value = format(role.created_at))
    embed.set_footer(text="Rage Bot v1.0")
    await bot.say(embed = embed)
    
@bot.command(pass_context = True)
async def warn(ctx, user : discord.Member = None, *, reason = ""):
    '''Warns a USer With a reason (Admin Only)'''
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" in user_roles:
        if user is None:
            return await ctx.send(":x: | Please specify a **member** to **__warn__**")
        if reason is None:
            return await ctx.send(":x: | You must have a **reason** specified")
        else:
            embed=discord.Embed(title="Log - Warning")
            embed.add_field(name="User:", value=user, inline=False)
            embed.add_field(name="UserID:", value=user.id, inline=False)
            embed.add_field(name="Reason:", value=reason, inline=False)
            embed.add_field(name="ModeratorID:", value=ctx.message.author.id, inline=False)
            embed.add_field(name="Moderator:", value=ctx.message.author, inline=False)
            embed.set_footer(text="Rage BOT  | Made by the RageKickedGamer#2406")
            await bot.send_message(discord.utils.get(ctx.message.server.channels, name="logs"), embed = embed)
            await bot.say(":white_check_mark:  | Warned `{}`!".format(user))
            embed=discord.Embed(title="Warning!")
            embed.add_field(name="User:", value=user, inline=False)
            embed.add_field(name="UserID:", value=user.id, inline=False)
            embed.add_field(name="Reason:", value=reason, inline=False)
            embed.add_field(name="ModeratorID:", value=ctx.message.author.id, inline=False)
            embed.add_field(name="Moderator:", value=ctx.message.author, inline=False)
            embed.set_footer(text="Rage BOT  | Made by the RageKickedGamer#2406")
            await bot.say(embed=embed)
    else:
        msg = ':eyes: | {} Tried to use warn | ID: {}'.format(ctx.message.author, ctx.message.author.id)
        await bot.send_message(discord.utils.get(ctx.message.server.channels, name="logs"), msg)
        await bot.say(":x: | Admin Only! | Action has been logged!")

@bot.command(pass_context = True)
async def msg(ctx, user : discord.Member = None, *, message : str = None):
    '''Send a user a Msg (Admin Only)'''
    user_roles = [r.name.lower() for r in ctx.message.author.roles]

    if "admin" in user_roles:
        if user is None:
            return await bot.say(":x: | Please specify a **member** to **__message__**")
        if message is None:
            return await bot.say(":x: | You must have a **message**")
        else:
            embed=discord.Embed(title="Moderator Message", description="Do not reply we will not recieve the message")
            embed.set_author(name="A Message From The Admin")
            embed.add_field(name="Message:", value=message, inline=False)
            embed.set_footer(text="Rage BOT  | Made by the RageKickedGamer#2406")
            await bot.send_message(user, embed=embed)
            await bot.say(":white_check_mark: | User Has Been Msg'd")
    else:
        msg = ':eyes: | {} Tried to use msg | ID: {}'.format(ctx.message.author, ctx.message.author.id)
        await bot.send_message(discord.utils.get(ctx.message.server.channels, name="logs"), msg)
        await bot.say(":x: | Admin Only! | Action has been logged!")
        
if not os.environ.get('TOKEN'):
        print("No token found REEEE!")
bot.run(os.environ.get('TOKEN').strip('\"'))

                       
