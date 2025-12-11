import discord
from discord.ext import commands
import random
import asyncio
import datetime
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройки бота
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# ============ СОБЫТИЯ ============

@bot.event
async def on_ready():
    print(f'Бот {bot.user} успешно запущен!')
    print(f'ID: {bot.user.id}')
    print(f'Время запуска: {datetime.datetime.now()}')
    
    # Устанавливаем статус бота
    await bot.change_presence(
        activity=discord.Game(name="!help для помощи"),
        status=discord.Status.online
    )

@bot.event
async def on_member_join(member):
    """Приветствие новых участников"""
    channel = discord.utils.get(member.guild.text_channels, name="основной")
    if channel:
        embed = discord.Embed(
            title=f"Добро пожаловать, {member.name}! 🎉",
            description=f"Рады видеть тебя на сервере **{member.guild.name}**!",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="Участник №", value=member.guild.member_count)
        embed.set_footer(text=f"ID: {member.id}")
        await channel.send(embed=embed)

# ============ КОМАНДЫ ============

@bot.command()
async def help(ctx):
    """Показать список команд"""
    embed = discord.Embed(
        title="📚 Помощь по командам бота",
        description="Доступные команды:",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="🎮 Развлечения", value="`!roll` `!coin` `!rand` `!cat` `!meme`", inline=False)
    embed.add_field(name="🛠 Утилиты", value="`!ping` `!user` `!server` `!clear` `!poll`", inline=False)
    embed.add_field(name="🎵 Музыка", value="`!play` `!stop` `!pause` `!resume`", inline=False)
    embed.add_field(name="⚙️ Модерация", value="`!kick` `!ban` `!mute` `!unmute`", inline=False)
    
    embed.set_footer(text=f"Запросил: {ctx.author.name}")
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    """Проверить задержку бота"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Понг! Задержка: {latency}мс')

@bot.command()
async def roll(ctx, dice: str = "1d6"):
    """Бросить кости (формат: 1d6)"""
    try:
        count, sides = map(int, dice.split('d'))
        if count > 20 or sides > 100:
            await ctx.send("⚠ Максимум: 20d100")
            return
        
        results = [random.randint(1, sides) for _ in range(count)]
        total = sum(results)
        
        embed = discord.Embed(
            title="🎲 Бросок костей",
            color=discord.Color.purple()
        )
        embed.add_field(name="Формат", value=dice, inline=True)
        embed.add_field(name="Результаты", value=', '.join(map(str, results)), inline=True)
        embed.add_field(name="Сумма", value=total, inline=True)
        embed.set_footer(text=f"Запросил: {ctx.author.name}")
        
        await ctx.send(embed=embed)
    except:
        await ctx.send("❌ Используй формат: `!roll 2d20`")

@bot.command()
async def coin(ctx):
    """Подбросить монетку"""
    result = random.choice(["Орёл", "Решка"])
    await ctx.send(f"🪙 Монетка подброшена: **{result}**")

@bot.command()
async def rand(ctx, min_num: int = 1, max_num: int = 100):
    """Случайное число в диапазоне"""
    if min_num > max_num:
        min_num, max_num = max_num, min_num
    
    number = random.randint(min_num, max_num)
    await ctx.send(f"🔢 Случайное число от {min_num} до {max_num}: **{number}**")

@bot.command()
async def user(ctx, member: discord.Member = None):
    """Информация о пользователе"""
    member = member or ctx.author
    
    embed = discord.Embed(
        title=f"👤 Информация о {member.name}",
        color=member.color
    )
    
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Никнейм", value=member.display_name, inline=True)
    embed.add_field(name="Бот", value="Да" if member.bot else "Нет", inline=True)
    
    join_date = member.joined_at.strftime("%d.%m.%Y %H:%M")
    created_date = member.created_at.strftime("%d.%m.%Y %H:%M")
    embed.add_field(name="На сервере с", value=join_date, inline=True)
    embed.add_field(name="Аккаунт создан", value=created_date, inline=True)
    
    roles = [role.mention for role in member.roles[1:]]
    if roles:
        embed.add_field(name="Роли", value=' '.join(roles[:5]), inline=False)
    
    embed.set_footer(text=f"Запросил: {ctx.author.name}")
    await ctx.send(embed=embed)

@bot.command()
async def server(ctx):
    """Информация о сервере"""
    guild = ctx.guild
    
    embed = discord.Embed(
        title=f"📊 Информация о сервере",
        description=guild.description or "Нет описания",
        color=discord.Color.gold()
    )
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    embed.add_field(name="Владелец", value=guild.owner.mention, inline=True)
    embed.add_field(name="ID сервера", value=guild.id, inline=True)
    embed.add_field(name="Участников", value=guild.member_count, inline=True)
    embed.add_field(name="Каналов", value=len(guild.channels), inline=True)
    embed.add_field(name="Ролей", value=len(guild.roles), inline=True)
    embed.add_field(name="Бустов", value=guild.premium_subscription_count, inline=True)
    
    created_date = guild.created_at.strftime("%d.%m.%Y %H:%M")
    embed.add_field(name="Создан", value=created_date, inline=True)
    
    if guild.banner:
        embed.set_image(url=guild.banner.url)
    
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    """Очистить сообщения (только для модераторов)"""
    if amount > 100:
        await ctx.send("❌ Можно удалить не более 100 сообщений за раз")
        return
    
    deleted = await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"✅ Удалено {len(deleted) - 1} сообщений")
    await asyncio.sleep(3)
    await msg.delete()

@bot.command()
async def poll(ctx, question, *options):
    """Создать опрос"""
    if len(options) > 10:
        await ctx.send("❌ Максимум 10 вариантов ответа")
        return
    
    if len(options) < 2:
        await ctx.send("❌ Нужно хотя бы 2 варианта ответа")
        return
    
    emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    
    embed = discord.Embed(
        title=f"📊 Опрос: {question}",
        color=discord.Color.orange()
    )
    
    for i, option in enumerate(options):
        embed.add_field(name=f"{emojis[i]} {option}", value="\u200b", inline=False)
    
    embed.set_footer(text=f"Создал: {ctx.author.name}")
    
    message = await ctx.send(embed=embed)
    
    for i in range(len(options)):
        await message.add_reaction(emojis[i])

# ============ МОДЕРАЦИЯ ============

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Не указана"):
    """Кикнуть участника"""
    try:
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="👢 Пользователь кикнут",
            description=f"{member.mention} был исключен с сервера",
            color=discord.Color.red()
        )
        embed.add_field(name="Причина", value=reason)
        embed.add_field(name="Модератор", value=ctx.author.mention)
        await ctx.send(embed=embed)
    except:
        await ctx.send("❌ Не удалось кикнуть пользователя")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Не указана"):
    """Забанить участника"""
    try:
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="🔨 Пользователь забанен",
            description=f"{member.mention} был забанен на сервере",
            color=discord.Color.dark_red()
        )
        embed.add_field(name="Причина", value=reason)
        embed.add_field(name="Модератор", value=ctx.author.mention)
        await ctx.send(embed=embed)
    except:
        await ctx.send("❌ Не удалось забанить пользователя")

# ============ МУЗЫКА ============

music_queue = []

@bot.command()
async def play(ctx, *, query):
    """Воспроизвести музыку (базовая реализация)"""
    if not ctx.author.voice:
        await ctx.send("❌ Подключитесь к голосовому каналу!")
        return
    
    voice_channel = ctx.author.voice.channel
    voice_client = ctx.voice_client
    
    if voice_client is None:
        voice_client = await voice_channel.connect()
    
    music_queue.append(query)
    
    embed = discord.Embed(
        title="🎵 Добавлено в очередь",
        description=f"**{query}**",
        color=discord.Color.green()
    )
    embed.add_field(name="Позиция в очереди", value=len(music_queue))
    embed.set_footer(text=f"Добавил: {ctx.author.name}")
    
    await ctx.send(embed=embed)

@bot.command()
async def stop(ctx):
    """Остановить музыку"""
    voice_client = ctx.voice_client
    if voice_client:
        await voice_client.disconnect()
        await ctx.send("⏹ Музыка остановлена")
    else:
        await ctx.send("❌ Бот не в голосовом канале")

# ============ ОБРАБОТКА ОШИБОК ============

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Команда не найдена. Используй `!help`")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ У вас недостаточно прав для этой команды")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Неправильное использование команды. Проверьте `!help`")

# ============ ЗАПУСК БОТА ============

# Получаем токен из переменных окружения или запрашиваем
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    print("⚠ Внимание! Токен не найден в переменных окружения.")
    TOKEN = input("Введите токен вашего Discord бота: ")

if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ Ошибка: Неверный токен бота!")
    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")