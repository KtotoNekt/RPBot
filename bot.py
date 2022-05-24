import discord
from discord.ext import commands
import sqlite3
import random
from threading import Thread
import aiohttp

import weather as wh
from config import info


bot = commands.Bot(command_prefix=info["prefix"], intents=discord.Intents.all())
bot.remove_command("help")

db = sqlite3.connect("server.db")
cursor = db.cursor()


def create_initial_inventory(count):
    empty_elements = ' ' + ", " * (count - 1)
    initial_inventory = [el for el in empty_elements.split(",")]
    count_initial_slot = list(map(int, list("0" * count)))
    for el in count_initial_slot:
        initial_inventory.append(el)

    return initial_inventory


initial_inventory = create_initial_inventory(25)


@bot.event
async def on_ready():
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        name TEXT,
        guild INT,
        id INT,
        capacity INT,
        thing1 TEXT,
        thing2 TEXT,
        thing3 TEXT,
        thing4 TEXT,
        thing5 TEXT,
        thing6 TEXT,
        thing7 TEXT,
        thing8 TEXT,
        thing9 TEXT,
        thing10 TEXT,
        thing11 TEXT,
        thing12 TEXT,
        thing13 TEXT,
        thing14 TEXT,
        thing15 TEXT,
        thing16 TEXT,
        thing17 TEXT,
        thing18 TEXT,
        thing19 TEXT,
        thing20 TEXT,
        thing21 TEXT,
        thing22 TEXT,
        thing23 TEXT,
        thing24 TEXT,
        thing25 TEXT,
        count1 INT,
        count2 INT,
        count3 INT,
        count4 INT,
        count5 INT,
        count6 INT,
        count7 INT,
        count8 INT,
        count9 INT,
        count10 INT,
        count11 INT,
        count12 INT,
        count13 INT,
        count14 INT,
        count15 INT,
        count16 INT,
        count17 INT,
        count18 INT,
        count19 INT,
        count20 INT,
        count21 INT,
        count22 INT,
        count23 INT,
        count24 INT,
        count25 INT
    )""")

    for guild in bot.guilds:
        for member in guild.members:
            append_to_list_user(member)

    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f"{bot.command_prefix}help"))



def append_to_list_user(member):
    if cursor.execute(f"SELECT id FROM users WHERE id = {member.id} AND guild = {member.guild.id}").fetchone() is None and member.bot == False:
        cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.guild.id}, {member.id}, 5, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", initial_inventory)
        db.commit()


@bot.event
async def on_member_join(member):
    append_to_list_user(member)


@bot.event
async def on_guild_join(guild):
    for member in guild.members:
        append_to_list_user(member)


@bot.command(aliases=["help", "hlp", "sos"])
async def __help(ctx, command=None, *, hlam=None):
    if command == None:
        embed = discord.Embed(title="Помощь по командам", color=0x00FF00)
        embed.add_field(name="Команды", value=f"""
`{bot.command_prefix}inventory` - вывод вашего инвентаря
`{bot.command_prefix}add_inventory [номер слота] [кол-во предметов] [название предмета]` - добавление предмета в инвентарь в определенный слот в определенном кол-ве
`{bot.command_prefix}del_inventory [номер слота] [кол-во предметов]` - удаление предмета из инвентаря по определенному слоту в определенном кол-ве
`{bot.command_prefix}edit_slot [уровень инвентаря(1-5)]` - добавление слотов в инвентарь
`{bot.command_prefix}roll [каждое действие через запятую]` - рандом
`{bot.command_prefix}help [команда(необязательно)]` - помощь по командам(-е)
""")
        embed.add_field(name="Команды для админов", value=f"""
**__1. {bot.command_prefix}admin__**
`{bot.command_prefix}admin @пользователь#6666 del 2 5` - удаление предмета из инвентаря @пользователь#6666
`{bot.command_prefix}admin @пользователь#6666 add 3 3 Овощи` - добавление предмета в инвентарь @пользователь#6666
`{bot.command_prefix}admin @пользователь#6666 edit_slot 2` - добавдение слотов в инвентарь @пользователь#6666
`{bot.command_prefix}admin @пользователь#6666 inv` - инвентарь @пользователь#6666

**__2. {bot.command_prefix}webhook_time__**
`{bot.command_prefix}webhook_time create [имя канала]` - создание временного вебхука в каком либо канале
`{bot.command_prefix}webhook_time start` - запуск временного вебхука
`{bot.command_prefix}webhook_time stop` - остановка временного вебхука
`{bot.command_prefix}webhook_time clear` - удаление временного вебхука
`{bot.command_prefix}webhook_time setting` - настройки временного вебхука
""")
        embed.add_field(name="Псевдонимы для команд", value=f"""
`{bot.command_prefix}inventory: {bot.command_prefix}inv`
`{bot.command_prefix}add_inventory: {bot.command_prefix}add_inv, {bot.command_prefix}add`
`{bot.command_prefix}del_inventory: {bot.command_prefix}del_inv, {bot.command_prefix}del`
`{bot.command_prefix}edit_slot: {bot.command_prefix}slot, {bot.command_prefix}ed_slot`
`{bot.command_prefix}roll: {bot.command_prefix}random`
`{bot.command_prefix}help: {bot.command_prefix}hlp, {bot.command_prefix}sos`
`{bot.command_prefix}webhook_time: {bot.command_prefix}hook_time, {bot.command_prefix}web_time`
`{bot.command_prefix}webhook_time setting: {bot.command_prefix}webhook_time settings, {bot.command_prefix}webhook_time set`
""")
    elif command in ["add", "add_inv", "add_inventory"]:
        embed = discord.Embed(title=f"Помощь по команде {bot.command_prefix}{command}", color=0x00FF00)
        embed.description = f"""**Пример**:
`{bot.command_prefix}{command} 1 4 Консервы`
Где:
  1 - номер слота куда нужно положить
  4 - кол-во предметов
  Консервы - название предмета"""
    elif command in ["del", "del_inv", "del_inventory"]:
        embed = discord.Embed(title=f"Помощь по команде {bot.command_prefix}{command}", color=0x00FF00)
        embed.description = f"""**Пример**:
`{bot.command_prefix}{command} 1 2`
Где:
  1 - номер слота из которого удалится предмет
  2 - кол-во предметов которое нужно удалить"""
    elif command in ["ed_slot", "slot", "edit_slot"]:
        embed = discord.Embed(title=f"Помощь по команде {bot.command_prefix}{command}", color=0x00FF00)
        embed.description = f"""**Пример**:
`{bot.command_prefix}{command} 2`
Где:
  2 - уровень инвентаря(максимум 3)

```
1 уровень - 5 слотов
2 уровень - 10 слотов
3 уровень - 15 слотов
4 уровень - 20 слотов
5 уровень - 25 слотов
```"""
    elif command in ["roll", "random"]:
        embed = discord.Embed(title=f"Помощь по команде {bot.command_prefix}{command}", color=0x00FF00)
        embed.description = f"""**Пример**:
`{bot.command_prefix}{command} идти, бежать, прыгать`
Где:
  идти, бежать, прыгать - действие которое случайным образом выподет

```
Примечание!:
  Каждое действие отделяйте запятой!!!
  Действий может быть безграничное кол-во
```"""
    elif command in ["admin"]:
        embed = discord.Embed(title=f"Помощь по команде {bot.command_prefix}{command}", color=0x00FF00)
        embed.description = f"""**Пример**:
`{bot.command_prefix}{command} @пользователь#6666 del 3 5`
Где:
  @пользователь#6666 - пинг пользователя
  del 3 5 - команда и ее аргументы

```
Примечание!:
  Команда может быть использована только пользователем, имеющий роль с правами администратора!
```"""
    else:
        embed = discord.Embed(title="??????", color=0xFF0000)
        embed.description = f"""Данной команды не существует или команда максимально проста, что не имеет никакой дополнительной информации

||Или создатель поленился сделать справку данной команде :)||"""

    if hlam != None:
        embed.set_footer(text=hlam)

    await ctx.send(embed=embed)


@bot.command(aliases=["inventory", "inv"])
async def __inventory(ctx: commands.context.Context, *, hlam=None, change=False, id=None, user=None):
    text = ""
    
    if not change:
        user_id = ctx.author.id
        title = "Ваш инвентарь"
    else:
        user_id = id
        title = f"Инвентарь {user}"

    embed = discord.Embed(title=title, color=0x00FF00)

    for i in range(1, cursor.execute(f"SELECT capacity FROM users WHERE id = {user_id} AND guild = {ctx.guild.id}").fetchone()[0] + 1):
        thing = cursor.execute(f"SELECT thing{i} FROM users WHERE id = {user_id} AND guild = {ctx.guild.id}").fetchone()[0]
        count = cursor.execute(f"SELECT count{i} FROM users WHERE id = {user_id} AND guild = {ctx.guild.id}").fetchone()[0]
        if count != 0:
            text += f"{i}. {thing} {count} шт\n"
        else:
            text += f"{i}. \n"

    embed.description = text

    await ctx.send(embed=embed)


async def change_capacity_inventory(ctx, index, capacity):
    for i in range(index, capacity + 1):
        count = cursor.execute(f"SELECT count{i} FROM users WHERE id = {ctx.author.id} AND guild = {ctx.guild.id}").fetchone()[0]
        await __del_inv(ctx=ctx, index=i, count=count, error=False)


def round_number(n):
    n_list = list(str(n))
    if len(n_list) > 3:
        for i in range(len(n_list) - 3):
            del n_list[-1]

    return float("".join(n_list))


@bot.command(aliases=["ed_slot", "slot", "edit_slot"])
async def __edit_slot(ctx: commands.context.Context, level=None, *, hlam=None, change=False, user=None):
    if level != None:

        if not change:
            user_id = ctx.author.id
        else:
            user_id =user.id

        level = int(level)
        capacity = cursor.execute(f"SELECT capacity FROM users WHERE id = {user_id} AND guild = {ctx.guild.id}").fetchone()[0]

        if level == 1:
            await change_capacity_inventory(ctx, 5, capacity)
            cursor.execute(f"UPDATE users SET capacity = 5 WHERE id = {user_id} AND guild = {ctx.guild.id}")
        elif level == 2:
            await change_capacity_inventory(ctx, 10, capacity)
            cursor.execute(f"UPDATE users SET capacity = 10 WHERE id = {user_id} AND guild = {ctx.guild.id}")
        elif level == 3:
            await change_capacity_inventory(ctx, 15, capacity)
            cursor.execute(f"UPDATE users SET capacity = 15 WHERE id = {user_id} AND guild = {ctx.guild.id}")
        elif level == 4:
            await change_capacity_inventory(ctx, 20, capacity)
            cursor.execute(f"UPDATE users SET capacity = 20 WHERE id = {user_id} AND guild = {ctx.guild.id}")
        elif level == 5:
            await change_capacity_inventory(ctx, 25, capacity)
            cursor.execute(f"UPDATE users SET capacity = 25 WHERE id = {user_id} AND guild = {ctx.guild.id}")
        else:
            await ctx.message.add_reaction("❌")
            await ctx.send("Такого уровня слотов нету")

        if level in [1, 2, 3, 4, 5]:
            db.commit()
            await ctx.message.add_reaction("✅")
    else:
        await ctx.message.add_reaction("❌")
        await ctx.send("Укажите уровень инвентаря")


@bot.command(aliases=["add_inv", "add_inventory", "add"])
async def __add_inv(ctx: commands.context.Context, index=None, count=None, *, thing: str=None, change=False, user=None):
    if index != None:
        index = int(index)
        if thing != None:
            count = int(count)
            if count > 0:
                if not change:
                    user_id = ctx.author.id
                    text_description = f"Вы подобрали {thing.lower()} в колличестве {count} шт"
                else:
                    user_id = user.id
                    text_description = f"Вы добавили {thing.lower()}в количестве {count} шт в инвентарь <@{user_id}>"
                    

                capacity = cursor.execute(f"SELECT capacity FROM users WHERE id = {user_id} AND guild = {ctx.guild.id}").fetchone()[0]
                if index <= capacity and index > 0:
                    predmet = cursor.execute(f"SELECT thing{index} FROM users WHERE id = {user_id} AND guild = {ctx.guild.id}").fetchone()[0]

                    if predmet != " ":
                        if predmet.lower() == thing.lower():
                            cursor.execute(f"UPDATE users SET count{index} = count{index} + {count} WHERE id = {user_id} AND guild = {ctx.guild.id}")
                            await ctx.message.add_reaction("✅")
                            msg = text_description
                        else:
                            await ctx.message.add_reaction("❌")
                            msg = "Данный слот занят"
                    else:
                        cursor.execute(f"UPDATE users SET thing{index} = '{thing}' WHERE id = {user_id} AND guild = {ctx.guild.id}")
                        cursor.execute(f"UPDATE users SET count{index} = {count} WHERE id = {user_id} AND guild = {ctx.guild.id}")
                        
                        msg = text_description
                        await ctx.message.add_reaction("✅")

                    db.commit()
                    await ctx.send(msg)
                else:
                    await ctx.message.add_reaction("❌")
                    await ctx.send("Данного слота не существует")
            else:
                await ctx.message.add_reaction("❌")
                await ctx.send("Вы ничего не подобрали")
        else:
            await ctx.message.add_reaction("❌")
            await ctx.send("Укажите предмет")
    else:
        await ctx.message.add_reaction("❌")
        await ctx.send("Укажите номер слота")


@bot.command(aliases=["del_inv", "del_inventory", "del", "dell"])
async def __del_inv(ctx: commands.context.Context, index=None, count=None, *, hlam=None, error=True, change=False, user=None):
    if index in ["all", "a"]:
        if not change:
            user_id = ctx.author.id
            text_send = f"Вы очистили свой инвентарь"
        else:
            user_id = user.id
            text_send = f"Вы очистили инвентарь <@{user_id}>"

        for i in range(1, cursor.execute(f"SELECT capacity FROM users WHERE id = {user_id} AND guild = {ctx.guild.id}").fetchone()[0] + 1):
            cursor.execute(f"UPDATE users SET thing{i} = ' ' WHERE id = {user_id} AND guild = {ctx.guild.id}")
            cursor.execute(f"UPDATE users SET count{i} = 0 WHERE id = {user_id} AND guild = {ctx.guild.id}")

        db.commit()

        await ctx.message.add_reaction("✅")
        await ctx.send(text_send)
    elif index != None:
        index = int(index)
        capacity = cursor.execute(f"SELECT capacity FROM users WHERE id = {ctx.author.id} AND guild = {ctx.guild.id}").fetchone()[0]
        if index <= capacity and index > 0:
                if not change:
                    user_id = ctx.author.id
                    text_description = f"Вы потратили(выкинули)"
                else:
                    user_id = user.id

                thing = cursor.execute(f"SELECT thing{index} FROM users WHERE id = {user_id} AND guild = {ctx.guild.id}").fetchone()[0]

                if thing != " ":
                    if count == None:
                        cursor.execute(f"UPDATE users SET thing{index} = ' ' WHERE id = {user_id} AND guild = {ctx.guild.id}")
                        cursor.execute(f"UPDATE users SET count{index} = 0 WHERE id = {user_id} AND guild = {ctx.guild.id}")
                        db.commit()
                        await ctx.message.add_reaction("✅")
                        if not change:
                            await ctx.send(f"Вы потратили(выкинули) {thing.lower()}")
                        else:
                            await ctx.send(f"Вы удалили {thing.lower()} из инвентаря <@{user_id}>")
                    elif float(count) > 0:
                        count = int(count)
                        num = cursor.execute(f"SELECT count{index} FROM users WHERE id = {user_id} AND guild = {ctx.guild.id}").fetchone()[0]
                        if count > num:
                            await ctx.message.add_reaction("❌")
                            await ctx.send("У вас нету такого кол-ва предметов")
                        else:
                            cursor.execute(f"UPDATE users SET count{index} = count{index} - {count} WHERE id = {user_id} AND guild = {ctx.guild.id}")

                            num = cursor.execute(f"SELECT count{index} FROM users WHERE id = {user_id} AND guild = {ctx.guild.id}").fetchone()[0]
                            pr = cursor.execute(f"SELECT thing{index} FROM users WHERE id = {user_id} AND guild = {ctx.guild.id}").fetchone()[0]

                            await ctx.message.add_reaction("✅")

                            if num <= 0:
                                if change:
                                    text_description = f"Вы удалили {thing.lower()} из инвентаря <@{user_id}>" 
                                cursor.execute(f"UPDATE users SET thing{index} = ' ' WHERE id = {user_id} AND guild = {ctx.guild.id}")
                                await ctx.send(f"{text_description} {thing.lower()}")
                            else:
                                if change:
                                    text_description = f"Вы удалили {thing.lower()} в количестве {count} шт из инвентаря <@{user_id}>" 
                                cursor.execute(f"UPDATE users SET thing{index} = '{pr}' WHERE id = {user_id} AND guild = {ctx.guild.id}")
                                await ctx.send(f"{text_description} {thing.lower()} в количестве {count} шт")

                            db.commit()
                        
                else:
                    if error:
                        await ctx.message.add_reaction("❌")
                        await ctx.send("Данный слот пустой")
        else:
            await ctx.message.add_reaction("❌")
            await ctx.send("Данного слота не существует")
    else:
        await ctx.message.add_reaction("❌")
        await ctx.send("Укажите номер слота")


@bot.command(aliases=["roll", "random"])
async def __roll(ctx, *, message: str=None):
    if message == None:
        message = [i for i in range(1, 100)]
    else:
        message = message.split(",")

    result = random.choice(message)
    await ctx.send(result)


@bot.command(aliases=["admin"])
@commands.has_permissions(administrator=True)
async def __admin(ctx, user: discord.Member, *, command):
    command = command.split()
    if command[0] in ["inv", "inventory"]:
        await __inventory(ctx, change=True, id=user.id, user=user.display_name)
    elif command[0] in ["del_inv", "del_inventroy", "del"]:
        if command[1] in ["all", "a"] or len(command) == 2:
            await __del_inv(ctx, command[1], change=True, user=user)
        else:
            await __del_inv(ctx, command[1], command[2], change=True, user=user)
    elif command[0] in ["add_inv", "add_inventroy", "add"]:
        thing = ""
        for i in range(3, len(command)):
            thing += command[i] + " "
        await __add_inv(ctx=ctx, index=command[1], count=command[2], thing=thing, change=True, user=user)
    elif command[0] in ["edit_slot", "ed_slot", "slot"]:
        await __edit_slot(ctx=ctx, level=command[1], change=True, user=user)
    else:
        await ctx.send("Команда не найдена")


@bot.command(aliases=["webhook_time", "web_time", "hook_time"])
@commands.has_permissions(administrator=True)
async def __webhook_time(ctx, *, command):
    command = command.split()
    if command[0] == "create":
        channel: discord.TextChannel = discord.utils.get(ctx.guild.channels, name=command[1])
        webhook = await channel.create_webhook(name="Бог времени")
        b = wh.create(ctx.guild.id, webhook.url)
        if not b:
            await ctx.send("У вас уже есть временной вебхук!")
    elif command[0] == "start":
        wh.run_change(ctx.guild.id, 1)
        timert_check = Thread(target=wh.start, args=[ctx.guild.id])
        timert_check.start()
        await ctx.send("Вебхук запущен")
    elif command[0] == "stop":
        wh.run_change(ctx.guild.id, 0)
        await ctx.send("Вебхук остановлен")
    elif command[0] == "clear":
        url = wh.clear(ctx.guild.id)
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url, adapter=discord.AsyncWebhookAdapter(session))
            await webhook.delete()
        
        await ctx.message.add_reaction("✅")
    elif command[0] in ["setting", "settings", "set"]:
        if len(command) == 1:
            embed = discord.Embed(title="Настройка временного вебхука", color=0x00FF00)
            embed.description = f"""
`{bot.command_prefix}webhook_time setting year [число]` - изменение года
`{bot.command_prefix}webhook_time setting month [номер месяца]` - изменение месяца
`{bot.command_prefix}webhook_time setting day [число до 30]` - изменение дня
`{bot.command_prefix}webhook_time setting realtime [время в минутах]` - через сколько произойдет повторный вывод информации о времени
`{bot.command_prefix}webhook_time setting timeout [число]` - сколько пройдет часов при завершении realtime"""

            await ctx.send(embed=embed)
        else:
            res = wh.arguments_change(ctx.guild.id, command)
            if res:
                await ctx.send(f"Поле {command[1]} успешно измененно!")
            else:
                await ctx.send(f"Не удалось найти данного аргумента")


@__del_inv.error
@__add_inv.error
@__roll.error
@__edit_slot.error
@__help.error
@__webhook_time.error
@__admin.error
async def commands_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="Ошибка", color=0xFF0000)
        embed.description = "У вас недостаточно прав для использования данной команды!"
    elif isinstance(error, Exception):
        embed = discord.Embed(title="Ошибка", color=0xFF0000)
        embed.description = "Ошибка в синтаксисе команды!"
        embed.set_footer(text=f"Используйте {bot.command_prefix}help [команда] чтобы узнать больше информации о команде")
        
    await ctx.send(embed=embed)
            

bot.run(info["token"])